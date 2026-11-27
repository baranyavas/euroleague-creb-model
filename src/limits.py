"""Per-match profit limit — the only stake constraint the user actually has.

Each site gives each *match* a maximum profit, not a maximum stake. The figure
is not fixed: Duel and Empire differ and it moves from match to match, so it is
read off the site when the line opens. Nothing here assumes a number.

For a single selection:

    max_stake = limit / (odds - 1)

For a combo the same cap applies leg by leg, so the ticket can be staked at
most

    min over legs of  limit / (odds - 1)

With similar limits the **highest-odds leg is the binding one** and the others
add nothing: a 1.90 / 1.77 / 1.85 3-fold at a 90 limit allows
100.00 / 116.88 / 105.88, so the ticket takes 100.00. That is why ten legs can
be combined — the top price still sets the stake.

Spend a match's whole allowance in one ticket and it cannot go into another
ticket on the same site.

    python -m src.limits 1.90 1.77 1.85 --limit 90
    python -m src.limits 1.90:120 1.77:90        # per-leg limits
    python -m src.limits 1.90 --stake 65         # allowance a flat 65 needs
"""

from __future__ import annotations

import argparse
from decimal import ROUND_DOWN, Decimal


def max_stake(odds: float, limit: float) -> float:
    """Largest stake whose profit on this match stays inside the limit."""
    o = Decimal(str(odds))
    if o <= 1:
        raise ValueError("odds must be greater than 1")
    stake = Decimal(str(limit)) / (o - 1)
    return float(stake.quantize(Decimal("0.01"), rounding=ROUND_DOWN))


def needed_allowance(stake: float, odds: float) -> float:
    """Profit allowance a given stake consumes on this match."""
    return round(stake * (odds - 1), 2)


def ticket_max_stake(legs: list[tuple[float, float]]) -> tuple[float, int]:
    """(max stake, index of the binding leg). legs = [(odds, limit), ...]."""
    caps = [(max_stake(o, lim), i) for i, (o, lim) in enumerate(legs)]
    return min(caps)


def _parse(token: str, default_limit: float | None) -> tuple[float, float]:
    odds, _, limit = token.partition(":")
    if not limit:
        if default_limit is None:
            raise SystemExit(f"give a limit for {token} (odds:limit) or --limit")
        return float(odds), default_limit
    return float(odds), float(limit)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("legs", nargs="*", help="odds or odds:limit per leg")
    ap.add_argument("--limit", type=float, help="same limit for every leg listed")
    ap.add_argument("--stake", type=float, help="check the allowance a stake needs")
    args = ap.parse_args()

    if not args.legs:
        ap.error("give at least one leg: 1.90 or 1.90:120")

    if args.stake is not None:
        odds = [float(t.partition(":")[0]) for t in args.legs]
        print(f"a {args.stake:,.2f} stake on one match needs an allowance of")
        for o in odds:
            print(f"  {o:5.2f} -> {needed_allowance(args.stake, o):7,.2f} profit")
        return

    legs = [_parse(t, args.limit) for t in args.legs]

    print(f"{'odds':>5} {'limit':>7} {'max stake':>10} {'profit':>8}")
    for o, lim in legs:
        s = max_stake(o, lim)
        print(f"{o:5.2f} {lim:7,.2f} {s:10,.2f} {s * (o - 1):8,.2f}")

    stake, idx = ticket_max_stake(legs)
    o = legs[idx][0]
    if len(legs) > 1:
        print(f"\nticket {len(legs)} legs -> max stake {stake:,.2f}, "
              f"set by the {o:.2f} leg")


if __name__ == "__main__":
    main()
