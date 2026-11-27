"""Forecast c-reb with the existing model — v0.7 base + v0.8 calibration.

This does NOT introduce a new model. It feeds the repository's own model
files with rolling pre-game profiles built from data/processed/team_games.csv.

    python -m src.forecast BAR BJK --date 2026-11-18 --line 71.5
    python -m src.forecast --backtest

The provider line is only used for the gap. It never enters the forecast.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

from . import config

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "model"))

import creb_model_v0_7 as v07  # noqa: E402
import creb_model_v0_8 as v08  # noqa: E402
import creb_model_v0_8_2 as v082  # noqa: E402


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def load_team_games() -> list[dict]:
    with (config.DATA_PROC / "team_games.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        for k in ("creb", "oreb", "dreb", "fga", "fgm", "fta", "ftm",
                  "missed_fg", "opp_missed_fg", "opp_creb", "home"):
            r[k] = int(r[k])
    return rows


def load_decisions() -> list[dict]:
    path = ROOT / "data" / "decisions_2026_27.csv"
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for r in rows:
        r["forecast"] = float(r["forecast"]) if r["forecast"] else None
        r["line"] = float(r["line"]) if r["line"] else None
    return rows


def load_games() -> dict[tuple[str, str], dict]:
    with (config.DATA_PROC / "games.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {(r["gamecode"], r["season"]): r for r in rows}


def _profile(rows: list[dict]) -> dict:
    n = len(rows)
    fga = sum(r["fga"] for r in rows)
    fgm = sum(r["fgm"] for r in rows)
    oreb = sum(r["oreb"] for r in rows)
    dreb = sum(r["dreb"] for r in rows)
    missed = sum(r["missed_fg"] for r in rows)
    opp_missed = sum(r["opp_missed_fg"] for r in rows)
    return {
        "games": n,
        "fga": fga / n,
        "fg_pct": fgm / fga if fga else None,
        "oreb": oreb / n,
        "dreb": dreb / n,
        "reboppr_o": oreb / missed if missed else None,
        "reboppr_d": dreb / opp_missed if opp_missed else None,
        "creb": sum(r["creb"] for r in rows) / n,
        "missed_fg": missed / n,
        "opp_missed_fg": opp_missed / n,
    }


def team_index(rows: list[dict]) -> dict[tuple[str, str], list[dict]]:
    idx: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        idx[(r["team_id"], r["season"])].append(r)
    return idx


# v0.7.1: pseudo-games pulling the direct missed-FG average toward the league
# mean. Tested 4/6/8/12; the differences were small and 8 sat in the middle of
# the flat region while doing best on games that carry a provider line.
MISS_PRIOR_GAMES = 8.0
LEAGUE_MISS_FALLBACK = 34.9


def league_missed_fg(idx, as_of: str) -> float:
    """League mean missed FG per team-game, using only games before as_of."""
    total = 0.0
    n = 0
    for (team, season), rows in idx.items():
        if season != config.LIVE_SEASON:
            continue
        for r in rows:
            if r["date"] < as_of:
                total += r["missed_fg"]
                n += 1
    if not n:
        return LEAGUE_MISS_FALLBACK
    return total / n


def shrunk_missed_fg(cur_rows: list[dict], league_miss: float) -> float:
    """Direct missed-FG average, shrunk toward the league mean."""
    n = len(cur_rows)
    if not n:
        return league_miss
    obs = sum(r["missed_fg"] for r in cur_rows) / n
    return (n * obs + MISS_PRIOR_GAMES * league_miss) / (n + MISS_PRIOR_GAMES)


def profiles_as_of(idx, as_of: str) -> dict[str, dict]:
    """Pre-game profile per team: current season before as_of, 2025-26 base."""
    teams = {team for team, _ in idx}
    out = {}
    league_miss = league_missed_fg(idx, as_of)
    for team in teams:
        hist_rows = idx.get((team, config.BASE_SEASON), [])
        cur_rows = [r for r in idx.get((team, config.LIVE_SEASON), []) if r["date"] < as_of]
        hist = _profile(hist_rows) if hist_rows else None
        cur = _profile(cur_rows) if cur_rows else None
        base = cur or hist
        if base is None:
            continue
        out[team] = {
            "fga": base["fga"],
            "fg_pct": base["fg_pct"],
            "reboppr_o": base["reboppr_o"],
            "reboppr_d": base["reboppr_d"],
            "current_c_reb": cur["creb"] if cur else None,
            "current_games": cur["games"] if cur else 0,
            "historical_c_reb": hist["creb"] if hist else None,
            "missed_fg": shrunk_missed_fg(cur_rows, league_miss),
        }
    return out


def h2h(idx, a: str, b: str) -> tuple[float | None, float | None]:
    """Previous-season regular-season meetings of a matchup (total c-reb)."""
    games = []
    for r in idx.get((a, config.BASE_SEASON), []):
        if r["opp_id"] == b:
            games.append((r["date"], r["creb"] + r["opp_creb"]))
    games.sort()
    if not games:
        return None, None
    values = [v for _, v in games]
    avg = sum(values) / len(values)
    gap = max(values) - min(values) if len(values) > 1 else None
    return avg, gap


def recorded_residuals(decisions, games, before: str) -> list[float]:
    """(actual - forecast) for recorded decisions strictly before a date."""
    out = []
    for d in decisions:
        if d["forecast"] is None or d["date"] >= before:
            continue
        game = find_game(games, d["date"], d["team_a"], d["team_b"])
        if game is None:
            continue
        out.append(int(game["creb_total"]) - d["forecast"])
    return out


def find_game(games, date: str, a: str, b: str):
    for g in games.values():
        if g["date"] == date and {g["away_id"], g["home_id"]} == {a, b}:
            return g
    return None


# --------------------------------------------------------------------------
# forecast
# --------------------------------------------------------------------------

def forecast_game(idx, games, decisions, home: str, away: str, as_of: str):
    prof = profiles_as_of(idx, as_of)
    if home not in prof or away not in prof:
        raise SystemExit(f"no profile for {home if home not in prof else away}")

    h2h_avg, h2h_gap = h2h(idx, home, away)
    matchup = v07.MatchupInput(
        home=v07.TeamProfile(name=home, **prof[home]),
        away=v07.TeamProfile(name=away, **prof[away]),
        h2h_avg=h2h_avg,
        h2h_gap=h2h_gap,
    )
    raw = v07.base_forecast(matchup, player_only=True)
    residuals = recorded_residuals(decisions, games, as_of)
    final = v08.forecast_with_learning(raw, residuals)

    return {
        "raw": raw,
        "forecast": final,
        "correction": final - raw,
        "residuals": len(residuals),
        "h2h_avg": h2h_avg,
        "h2h_gap": h2h_gap,
        "home_profile": prof[home],
        "away_profile": prof[away],
    }


# --------------------------------------------------------------------------
# backtest (retrospective diagnostic, not a decision record)
# --------------------------------------------------------------------------

def backtest(idx, games, decisions) -> list[dict]:
    live = sorted(
        (g for g in games.values() if g["season"] == config.LIVE_SEASON),
        key=lambda g: (g["date"], g["gamecode"]),
    )
    out = []
    for g in live:
        try:
            res = forecast_game(
                idx, games, decisions, g["home_id"], g["away_id"], g["date"]
            )
        except SystemExit:
            continue
        out.append(
            {
                "date": g["date"],
                "round": g["gameday"],
                "game": f"{g['away_id']}-{g['home_id']}",
                "forecast": round(res["forecast"], 2),
                "actual": int(g["creb_total"]),
                "residual": round(int(g["creb_total"]) - res["forecast"], 2),
                "missed_fg": int(g["missed_fg_total"]),
            }
        )
    return out


def write_backtest(rows: list[dict]) -> None:
    if not rows:
        print("backtest: no rows")
        return
    config.REPORTS.mkdir(parents=True, exist_ok=True)
    csv_path = config.REPORTS / "backtest_2026_27.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    by_round: dict[int, list[dict]] = defaultdict(list)
    for r in rows:
        by_round[r["round"]].append(r)

    lines = [
        "# 2026-27 retrospective backtest",
        "",
        "Model: v0.7 base forecast (player-only) + v0.8 residual calibration, fed with",
        "rolling pre-game profiles. Retrospective diagnostic only — the live",
        "decision record stays in `data/decision_registry.md`.",
        "",
        "| round | games | MAE | bias | mean forecast | mean actual |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for rnd in sorted(by_round):
        rs = by_round[rnd]
        n = len(rs)
        mae = sum(abs(r["residual"]) for r in rs) / n
        bias = sum(r["residual"] for r in rs) / n
        mf = sum(r["forecast"] for r in rs) / n
        ma = sum(r["actual"] for r in rs) / n
        lines.append(f"| {rnd} | {n} | {mae:.2f} | {bias:+.2f} | {mf:.1f} | {ma:.1f} |")

    n = len(rows)
    mae = sum(abs(r["residual"]) for r in rows) / n
    bias = sum(r["residual"] for r in rows) / n
    rmse = (sum(r["residual"] ** 2 for r in rows) / n) ** 0.5
    lines += [
        "",
        f"**All {n} games: MAE {mae:.2f}, RMSE {rmse:.2f}, bias {bias:+.2f}.**",
        "",
        "Bias > 0 means the model was too low.",
        "",
    ]
    (config.REPORTS / "backtest_2026_27.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"backtest: {n} games, MAE {mae:.2f}, bias {bias:+.2f} -> reports/backtest_2026_27.md")


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("home", nargs="?", help="home team id, e.g. BAR")
    parser.add_argument("away", nargs="?", help="away team id, e.g. BJK")
    parser.add_argument("--date", default=None, help="as-of date (default: today)")
    parser.add_argument("--line", type=float, default=None, help="provider line")
    parser.add_argument("--backtest", action="store_true")
    args = parser.parse_args()

    rows = load_team_games()
    idx = team_index(rows)
    games = load_games()
    decisions = load_decisions()

    if args.backtest:
        write_backtest(backtest(idx, games, decisions))
        return

    if not args.home or not args.away:
        parser.error("give HOME AWAY or --backtest")

    from datetime import date as _date
    as_of = args.date or _date.today().isoformat()
    res = forecast_game(idx, games, decisions, args.home.upper(), args.away.upper(), as_of)

    print(f"{args.home.upper()} (home) vs {args.away.upper()} (away)   as of {as_of}")
    print(f"  forecast : {res['forecast']:.2f} c-reb")
    print(f"  raw v0.7 : {res['raw']:.2f}   calibration {res['correction']:+.2f} "
          f"({res['residuals']} recorded residuals)")
    if res["h2h_avg"] is not None:
        gap = "" if res["h2h_gap"] is None else f", gap {res['h2h_gap']:.0f}"
        print(f"  h2h 2025-26: {res['h2h_avg']:.1f}{gap}")
    hp, ap = res["home_profile"], res["away_profile"]
    for tag, p in ((args.home.upper(), hp), (args.away.upper(), ap)):
        print(f"  {tag}: {p['current_games']} games this season, "
              f"fga {p['fga']:.1f}, fg% {100 * p['fg_pct']:.1f}, "
              f"reboppr-o {p['reboppr_o']:.3f}, reboppr-d {p['reboppr_d']:.3f}")
    if args.line is not None:
        gap = res["forecast"] - args.line
        side = "OVER" if gap > 0 else "UNDER"
        print(f"  line {args.line:.1f} -> gap {gap:+.2f} -> lean {side}")


if __name__ == "__main__":
    main()
