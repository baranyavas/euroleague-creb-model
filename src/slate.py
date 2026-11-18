"""Print the pre-line card for a slate, like the NBA model's card.

    ./.venv/bin/python -m src.slate                 # today
    ./.venv/bin/python -m src.slate --date 2026-11-17 --write

The model never sees a line here. It prints a fair number per game, the line
the provider normally posts (model + 5.63), the line at which each side
becomes playable, and the **combo sessions**: groups of games whose tip-offs
are close enough together that their lines are open at the same time.

Combo rule (see STATE.md): legs may only be joined when their tip-offs are
within COMBO_WINDOW_MIN (45) of the first leg's tip. A line opens 60 minutes
before its own tip, so a 21:00 game and a 22:30 game can never share a ticket:
the 22:30 line opens at 21:30, when the 21:00 game is already live.
"""

from __future__ import annotations

import argparse
import csv
import math
import statistics
from datetime import date as _date, datetime, timedelta

from . import config, el_api, forecast as F

EDGE_PLAY = 3.0   # minimum |forecast - line| to be a bet candidate
EDGE_STRONG = 5.0
DEFAULT_SD = 8.26  # backtest RMSE, used if the report is missing

MARKET_SHADE = config.MARKET_SHADE
MODEL_BIAS = 0.85  # backtest bias -0.85 -> the forecast runs 0.85 high
LEG_P = 0.72       # planning win rate per under leg (22/27 recorded)
ODDS = 1.85


def residual_sd() -> float:
    path = config.REPORTS / "backtest_2026_27.csv"
    if not path.exists():
        return DEFAULT_SD
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        return DEFAULT_SD
    r = [float(x["residual"]) for x in rows]
    return statistics.pstdev(r)


def max_game_code() -> int:
    codes = [
        int(g["gamecode"])
        for g in F.load_games().values()
        if g["season"] == config.LIVE_SEASON and g["gamecode"].isdigit()
    ]
    return max(codes)


def slate_games(target: str) -> list[dict]:
    """Future games are not in /results; probe the sequential game codes."""
    games = []
    misses = 0
    for code in range(max_game_code() + 1, max_game_code() + 80):
        try:
            box = el_api.parse_game(el_api.game_xml(config.LIVE_SEASON, str(code)))
        except Exception:
            misses += 1
            if misses >= 6:
                break
            continue
        misses = 0
        dt = box.get("datetime") or ""
        if dt[:10] == target:
            games.append({"code": str(code), **box})
    return sorted(games, key=lambda g: g["datetime"])


def tr_time(cet: str) -> str:
    """CET (UTC+1) -> Turkey (UTC+3)."""
    try:
        return (datetime.fromisoformat(cet) + timedelta(hours=2)).strftime("%H:%M")
    except ValueError:
        return "?"


def expected_line(model: float) -> float:
    """What the provider normally posts: model + 5.63, rounded to a .5 line."""
    return round((model + MARKET_SHADE) * 2) / 2


def _up(x: float) -> float:
    return math.ceil(x * 2) / 2


def _down(x: float) -> float:
    return math.floor(x * 2) / 2


def under_prob(line: float, model: float, sd: float) -> float:
    """Normal approximation, with the measured -0.85 forecast bias applied."""
    z = (line - model + MODEL_BIAS) / sd
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def expected_miss(profile: dict) -> float:
    return profile["fga"] * (1 - profile["fg_pct"])


def game_sd(miss: float, base_sd: float, base_miss: float) -> float:
    """Residual sd scaled by the game's expected miss volume."""
    if base_miss <= 0:
        return base_sd
    return base_sd * math.sqrt(miss / base_miss)


def sessions(slate: list[dict], window: int = config.COMBO_WINDOW_MIN) -> list[list[dict]]:
    """Group games whose tip is within `window` minutes of the group's first tip."""
    groups: list[list[dict]] = []
    for g in slate:
        t = datetime.fromisoformat(g["datetime"])
        if groups:
            first = datetime.fromisoformat(groups[-1][0]["datetime"])
            if (t - first) <= timedelta(minutes=window):
                groups[-1].append(g)
                continue
        groups.append([g])
    return groups


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=_date.today().isoformat())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    target = args.date
    rows = F.load_team_games()
    idx = F.team_index(rows)
    games = F.load_games()
    decisions = F.load_decisions()
    sd = residual_sd()
    half = 1.2816 * sd

    slate = slate_games(target)
    if not slate:
        print(f"no games found for {target}")
        return

    priced = []
    for g in slate:
        home = config.club_id(g["home"]["code"])
        away = config.club_id(g["away"]["code"])
        res = F.forecast_game(idx, games, decisions, home, away, target)
        priced.append(
            {
                "game": f"{home}-{away}",
                "tip": tr_time(g["datetime"]),
                "datetime": g["datetime"],
                "model": res["forecast"],
                "h2h": res["h2h_avg"],
                "line": expected_line(res["forecast"]),
                "p": under_prob(expected_line(res["forecast"]), res["forecast"], sd),
                "home_profile": res["home_profile"],
                "away_profile": res["away_profile"],
            }
        )

    lines = [
        f"# Card — {target}",
        "",
        f"Model frozen pre-line. Residual sd {sd:.2f}; 80% interval ±{half:.1f}.",
        f"Play when |model − line| ≥ {EDGE_PLAY:.1f}; strong at ≥ {EDGE_STRONG:.1f}.",
        f"Market reference (19 recorded decisions): **line ≈ model + {MARKET_SHADE:.1f}**, "
        f"sd {config.MARKET_SHADE_SD:.2f}.",
        "",
        "| tip | game | model | likely line | under ≥ | over ≤ | h2h |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for p in priced:
        h2h = "—" if p["h2h"] is None else f"{p['h2h']:.0f}"
        lines.append(
            f"| {p['tip']} | {p['game']} | **{p['model']:.1f}** | {p['line']:.1f} "
            f"| {p['model'] + EDGE_PLAY:.1f} | {p['model'] - EDGE_PLAY:.1f} | {h2h} |"
        )

    lines += [
        "",
        "`likely line` = model + 5.6, the provider's usual shade. "
        "`under ≥` = model + 3; `over ≤` = model − 3. "
        "A posted line between the two is a pass.",
        "",
        "## Line bands (what to do where the line lands)",
        "",
        "| game | model | over ≤ | pass | thin | normal | strong ≥ | exp miss | sd |",
        "|---|---:|---:|---|---|---|---:|---:|---:|",
    ]

    live_miss = [
        int(g["missed_fg_total"]) for g in games.values()
        if g["season"] == config.LIVE_SEASON and g.get("missed_fg_total")
    ]
    base_miss = statistics.mean(live_miss) if live_miss else 69.4
    for p in priced:
        miss = expected_miss(p["home_profile"]) + expected_miss(p["away_profile"])
        p["sd"] = game_sd(miss, sd, base_miss)
        p["miss"] = miss
        lines.append(
            f"| {p['game']} | {p['model']:.1f} | {_down(p['model'] - 3):.1f} "
            f"| {_down(p['model'] - 3) + 0.5:.1f}–{_up(p['model'] + 3) - 0.5:.1f} "
            f"| {_up(p['model'] + 3):.1f}–{_up(p['model'] + 5) - 0.5:.1f} "
            f"| {_up(p['model'] + 5):.1f}–{_up(p['model'] + 7) - 0.5:.1f} "
            f"| {_up(p['model'] + 7):.1f} | {miss:.0f} | {p['sd']:.2f} |"
        )

    lines += [
        "",
        "| game | thin | likely | strong |",
        "|---|---|---|---|",
    ]
    for p in priced:
        thin = _up(p["model"] + 3)
        strong = _up(p["model"] + 7)
        lines.append(
            f"| {p['game']} | {thin:.1f} → {100 * under_prob(thin, p['model'], p['sd']):.0f}% "
            f"| {p['line']:.1f} → {100 * under_prob(p['line'], p['model'], p['sd']):.0f}% "
            f"| {strong:.1f} → {100 * under_prob(strong, p['model'], p['sd']):.0f}% |"
        )

    lines += [
        "",
        "`thin` = single only, never a combo leg. `normal` = combo leg. "
        "`strong` = combo leg and a single if wanted. Below `pass` it is a no-bet; "
        "below `over` the side flips.",
        "",
        "## Combo sessions (45-minute rule)",
        "",
        "Legs can only be joined if tips are ≤45 min apart, because each line "
        "opens 60 min before its own tip. Sessions are separated by a blank line.",
        "",
    ]

    groups = sessions(slate)
    by_name = {p["game"]: p for p in priced}
    for i, group in enumerate(groups, 1):
        names = [f"{config.club_id(g['home']['code'])}-{config.club_id(g['away']['code'])}" for g in group]
        tip = tr_time(group[0]["datetime"])
        kind = "single" if len(group) == 1 else f"{len(group)} legs"
        lines.append(f"**S{i} — {tip} ({kind})**")
        lines.append("")
        for name in names:
            p = by_name[name]
            lines.append(
                f"- {name}: model {p['model']:.1f}, likely line {p['line']:.1f}, "
                f"under ≥ {p['model'] + EDGE_PLAY:.1f}"
            )
        lines.append("")

    # Combos per session, 2..n legs. Payout 1.85^n, planning P = 0.72^n.
    lines += [
        "| combo | legs | payout | P(win) | EV per 1u |",
        "|---|---:|---:|---:|---:|",
    ]
    for i, group in enumerate(groups, 1):
        names = [f"{config.club_id(g['home']['code'])}-{config.club_id(g['away']['code'])}" for g in group]
        for n in range(2, len(names) + 1):
            payout = ODDS ** n
            prob = LEG_P ** n
            lines.append(
                f"| S{i} {n}-fold | {', '.join(names[:n])} | {payout:.2f} "
                f"| {prob:.2f} | {payout * prob - 1:+.2f} |"
            )

    lines += [
        "",
        f"Planning P per leg is {LEG_P:.2f} (recorded: 22/27 = 0.81, shrunk down). "
        "EV assumes every leg is an under at the likely line.",
        "**Risk:** legs in one session share the night's shooting environment. "
        "A high-missed-FG night can take all of them at once, so the 5-fold is "
        "not five independent bets.",
        "",
        "## Team form (2026-27, pre-game)",
        "",
        "| team | g | FGA | FG% | REBOPPR-O | REBOPPR-D |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    seen = set()
    for p in priced:
        for team, prof in (
            (p["game"].split("-")[0], p["home_profile"]),
            (p["game"].split("-")[1], p["away_profile"]),
        ):
            if team in seen:
                continue
            seen.add(team)
            lines.append(
                f"| {team} | {prof['current_games']} | {prof['fga']:.1f} "
                f"| {100 * prof['fg_pct']:.1f} | {prof['reboppr_o']:.3f} "
                f"| {prof['reboppr_d']:.3f} |"
            )

    text = "\n".join(lines)
    print(text)
    if args.write:
        config.REPORTS.mkdir(parents=True, exist_ok=True)
        (config.REPORTS / f"card_{target}.md").write_text(text + "\n", encoding="utf-8")
        print(f"\nwrote reports/card_{target}.md")


if __name__ == "__main__":
    main()
