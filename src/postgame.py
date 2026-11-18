"""Post-game check for one date or one round.

    ./.venv/bin/python -m src.postgame                 # yesterday
    ./.venv/bin/python -m src.postgame --date 2026-11-17
    ./.venv/bin/python -m src.postgame --round 12

Reads the *recorded* pregame forecast from data/decisions_2026_27.csv. It never
re-runs the model: a forecast recomputed after the game is not a forecast.

Output: one row per game (model, line, gap, actual, residual, result, OT) plus
the day's bias, the direction record and the rolling round bias.
"""

from __future__ import annotations

import argparse
import csv
import statistics
from collections import defaultdict
from datetime import date as _date, timedelta

from . import config


def _rows(path):
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date")
    parser.add_argument("--round", type=int)
    args = parser.parse_args()

    games = [
        g for g in _rows(config.DATA_PROC / "games.csv")
        if g["season"] == config.LIVE_SEASON
    ]
    if args.round is not None:
        games = [g for g in games if int(g["gameday"]) == args.round]
    elif args.date:
        games = [g for g in games if g["date"] == args.date]
    else:
        y = (_date.today() - timedelta(days=1)).isoformat()
        games = [g for g in games if g["date"] == y]

    if not games:
        print("no games for that date/round")
        return

    decisions = _rows(config.ROOT / "data" / "decisions_2026_27.csv")
    index = {
        (d["date"], frozenset((d["team_a"], d["team_b"]))): d for d in decisions
    }

    games.sort(key=lambda g: g["gamecode"])
    print(f"{'game':10} {'model':>6} {'line':>6} {'gap':>6} {'actual':>6} "
          f"{'resid':>6} {'res':>6} {'ot':>3}")
    rows = []
    for g in games:
        key = (g["date"], frozenset((g["home_id"], g["away_id"])))
        d = index.get(key)
        actual = int(g["creb_total"])
        model = float(d["forecast"]) if d and d["forecast"] else None
        line = float(d["line"]) if d and d["line"] else None
        model_txt = f"{model:.1f}" if model is not None else "nr"
        line_txt = f"{line:.1f}" if line is not None else "nr"
        gap = f"{model - line:+.1f}" if (model is not None and line is not None) else "nr"
        resid = f"{actual - model:+.1f}" if model is not None else "nr"
        if line is None:
            result = "nr"
        else:
            result = "under" if actual < line else "over" if actual > line else "push"
        print(f"{g['home_id'] + '-' + g['away_id']:10} {model_txt:>6} {line_txt:>6} "
              f"{gap:>6} {actual:>6} {resid:>6} {result:>6} {g['ot']:>3}")
        rows.append((g, model, line, actual))

    preds = [(g, m, ln, a) for g, m, ln, a in rows if m is not None]
    if preds:
        residuals = [a - m for _, m, _, a in preds]
        print(
            f"\nbias {statistics.mean(residuals):+.2f} (model too low if positive), "
            f"MAE {statistics.mean(abs(v) for v in residuals):.2f}, "
            f"n {len(residuals)}, OT games {sum(int(g['ot']) for g, _, _, _ in preds)}"
        )
    with_line = [(ln, a) for _, _, ln, a in rows if ln is not None]
    if with_line:
        under = sum(1 for ln, a in with_line if a < ln)
        print(f"direction: {under} under / {len(with_line) - under} over "
              f"({len(with_line)} lines captured)")

    # Rolling round bias from the walk-forward backtest.
    bt_path = config.REPORTS / "backtest_2026_27.csv"
    if bt_path.exists():
        by_round = defaultdict(list)
        for r in _rows(bt_path):
            by_round[int(r["round"])].append(float(r["residual"]))
        print("\nround  bias   MAE")
        for rd in sorted(by_round)[-6:]:
            v = by_round[rd]
            print(f"{rd:>5}  {statistics.mean(v):+.2f}  "
                  f"{statistics.mean(abs(x) for x in v):5.2f}")


if __name__ == "__main__":
    main()
