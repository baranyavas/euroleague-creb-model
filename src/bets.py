"""Stake ledger: what was actually bet, and what it returned.

    python -m src.bets

Reads data/bets_2026_27.csv. Unknown odds or stakes are reported, never
guessed; the totals only use the rows where the numbers are known.
"""

from __future__ import annotations

import csv
from collections import defaultdict

from . import config

PATH = config.ROOT / "data" / "bets_2026_27.csv"


def _num(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def rows() -> list[dict]:
    with PATH.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pnl(row: dict) -> float | None:
    stake = _num(row.get("stake_usd"))
    odds = _num(row.get("odds"))
    if stake is None:
        return None
    if row["result"] == "lost":
        return -stake
    if row["result"] == "won":
        return None if odds is None else stake * (odds - 1)
    return 0.0


def main() -> None:
    data = rows()
    print(f"{'date':11} {'kind':7} {'odds':>6} {'stake':>7} {'result':>8} {'P&L':>9}  legs")
    total_known = 0.0
    staked_known = 0.0
    missing: list[str] = []

    for r in data:
        stake = _num(r["stake_usd"])
        odds = _num(r["odds"])
        value = pnl(r)
        pnl_txt = f"{value:+.0f}" if value is not None else "?"
        print(
            f"{r['date']:11} {r['kind']:7} "
            f"{(f'{odds:.2f}' if odds is not None else '?'):>6} "
            f"{(f'{stake:.0f}' if stake is not None else '?'):>7} "
            f"{r['result']:>8} {pnl_txt:>9}  {r['legs']}"
        )
        if value is None:
            missing.append(r["bet_id"])
        else:
            total_known += value
            staked_known += stake or 0.0

    print()
    if staked_known:
        print(
            f"known: staked {staked_known:.0f}, net {total_known:+.0f}, "
            f"ROI {100 * total_known / staked_known:+.1f}%, n {len(data)}"
        )
    if missing:
        print(f"unresolved (odds or stake missing): {', '.join(missing)}")
        print("add the missing numbers to data/bets_2026_27.csv and re-run.")

    by_date: dict[str, list[float]] = defaultdict(list)
    for r in data:
        value = pnl(r)
        if value is not None:
            by_date[r["date"]].append(value)
    if by_date:
        print("\nby date:")
        running = 0.0
        for day in sorted(by_date):
            net = sum(by_date[day])
            running += net
            print(f"  {day}  n{len(by_date[day]):>2}  {net:+8.0f}   cumulative {running:+8.0f}")


if __name__ == "__main__":
    main()
