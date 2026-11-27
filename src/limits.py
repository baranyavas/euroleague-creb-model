"""Per-match profit limit — the only stake constraint the user actually has.

Every site gives a match a maximum *profit* rather than a maximum stake. So the
most that can be staked on one selection is

    max_stake = limit / (odds - 1)

At a 90 limit: 1.90 -> 100.00, 1.80 -> 112.50, 1.77 -> 116.88.

If a ticket uses up a match's allowance, that match cannot go into another
ticket on the same site. That is the whole rule: no ticket count, no session
leg cap, no ladder.

    python -m src.limits 1.90 1.85 1.77 --limit 90
    python -m src.limits --table --limit 90
"""

from __future__ import annotations

import argparse
from decimal import ROUND_DOWN, Decimal

DEFAULT_LIMIT = Decimal("90")


def max_stake(odds: float, limit: float = 90.0) -> float:
    """Largest stake whose profit stays inside the limit. Rounded down."""
    o = Decimal(str(odds))
    if o <= 1:
        raise ValueError("odds must be greater than 1")
    stake = Decimal(str(limit)) / (o - 1)
    return float(stake.quantize(Decimal("0.01"), rounding=ROUND_DOWN))


def profit(stake: float, odds: float) -> float:
    return round(stake * (odds - 1), 2)


def remaining(used: list[tuple[float, float]], odds: float, limit: float = 90.0) -> float:
    """How much profit is left on a match after the tickets already placed."""
    return round(limit - sum(profit(s, o) for s, o in used), 2)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("odds", nargs="*", type=float, help="leg odds")
    ap.add_argument("--limit", type=float, default=float(DEFAULT_LIMIT),
                    help="per-match profit limit in dollars (default 90)")
    ap.add_argument("--table", action="store_true", help="print a table of odds")
    args = ap.parse_args()

    if args.table:
        print(f"limit {args.limit:,.0f} profit per match")
        print(f"{'odds':>6} {'max stake':>10} {'profit':>8}")
        for i in range(160, 211, 5):
            o = i / 100
            s = max_stake(o, args.limit)
            print(f"{o:6.2f} {s:10,.2f} {profit(s, o):8,.2f}")
        return

    if not args.odds:
        ap.error("give at least one odds value, or --table")
    print(f"limit {args.limit:,.0f} profit per match")
    for o in args.odds:
        s = max_stake(o, args.limit)
        print(f"  {o:5.2f} -> stake {s:8,.2f}   profit {profit(s, o):7,.2f}")


if __name__ == "__main__":
    main()
