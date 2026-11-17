"""Print the pre-line card for a slate, like the NBA model's card.

    ./.venv/bin/python -m src.slate                 # today
    ./.venv/bin/python -m src.slate --date 2026-11-17

The model never sees a line here. It prints a fair number per game and the
line at which a side becomes playable, so the 1-hour-before-tip line can be
priced instantly.
"""

from __future__ import annotations

import argparse
import csv
import statistics
from datetime import date as _date, datetime, timedelta

from . import config, el_api, forecast as F

EDGE_PLAY = 3.0   # minimum |forecast - line| to be a bet candidate
EDGE_STRONG = 5.0
DEFAULT_SD = 8.26  # backtest RMSE, used if the report is missing


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

    lines = [
        f"# Card — {target}",
        "",
        f"Model frozen pre-line. Residual sd {sd:.2f}; 80% interval ±{half:.1f}.",
        f"Play when |model − line| ≥ {EDGE_PLAY:.1f}; strong at ≥ {EDGE_STRONG:.1f}.",
        "",
        "| tip | game | model | 80% | UNDER playable if line ≥ | OVER playable if line ≤ | h2h |",
        "|---|---|---:|---|---:|---:|---|",
    ]
    profiles = []
    for g in slate:
        home, away = config.club_id(g["home"]["code"]), config.club_id(g["away"]["code"])
        res = F.forecast_game(idx, games, decisions, home, away, target)
        f = res["forecast"]
        h2h = "—" if res["h2h_avg"] is None else f"{res['h2h_avg']:.0f}"
        lines.append(
            f"| {tr_time(g['datetime'])} | {home}-{away} | **{f:.1f}** "
            f"| {f - half:.0f}–{f + half:.0f} | {f + EDGE_PLAY:.1f} "
            f"| {f - EDGE_PLAY:.1f} | {h2h} |"
        )
        profiles.append((home, res["home_profile"]))
        profiles.append((away, res["away_profile"]))

    lines += [
        "",
        "`UNDER playable` = model + 3; `OVER playable` = model − 3. "
        "If the posted line sits between them, pass.",
        "",
        "## Team form (2026-27, pre-game)",
        "",
        "| team | g | FGA | FG% | REBOPPR-O | REBOPPR-D |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    seen = set()
    for team, p in profiles:
        if team in seen:
            continue
        seen.add(team)
        lines.append(
            f"| {team} | {p['current_games']} | {p['fga']:.1f} "
            f"| {100 * p['fg_pct']:.1f} | {p['reboppr_o']:.3f} | {p['reboppr_d']:.3f} |"
        )

    text = "\n".join(lines)
    print(text)
    if args.write:
        config.REPORTS.mkdir(parents=True, exist_ok=True)
        (config.REPORTS / f"card_{target}.md").write_text(text + "\n", encoding="utf-8")
        print(f"\nwrote reports/card_{target}.md")


if __name__ == "__main__":
    main()
