"""Stake ledger: every EuroLeague c-reb ticket, what went in and what came back.

    python -m src.bets

Reads data/bets_2026_27.csv (rebuilt from the bet-slip screenshots). Each row
carries the amount staked and the amount actually returned, so P&L never has
to be reconstructed from odds. Rows whose numbers were derived rather than
read off the slip say so in the note.
"""

from __future__ import annotations

import csv

from . import config

PATH = config.ROOT / "data" / "bets_2026_27.csv"


def rows() -> list[dict]:
    with PATH.open(newline="", encoding="utf-8") as fh:
        data = list(csv.DictReader(fh))
    return sorted(data, key=lambda r: (r["date"], r["time"], r["bet_id"]))


def _sum(data: list[dict], key: str) -> float:
    return sum(float(r[key]) for r in data)


def _line(label: str, data: list[dict]) -> str:
    staked = _sum(data, "stake_usd")
    ret = _sum(data, "return_usd")
    net = ret - staked
    won = sum(1 for r in data if r["result"] == "won")
    roi = 100 * net / staked if staked else 0.0
    return (
        f"{label:9} n{len(data):>2}  W{won:>2}/L{len(data)-won:<2}  "
        f"staked {staked:8,.2f}  returned {ret:9,.2f}  net {net:+9,.2f}  ROI {roi:+6.1f}%"
    )


def main() -> None:
    all_rows = rows()
    data = [r for r in all_rows if r["result"] != "open"]
    open_rows = [r for r in all_rows if r["result"] == "open"]

    print("date        time   site    kind      odds   stake  returned      net")
    for r in all_rows:
        stake = float(r["stake_usd"])
        ret = float(r["return_usd"])
        print(
            f"{r['date']}  {(r['time'] or '  -- '):5}  {r['site']:6}  {r['kind']:7} "
            f"{float(r['odds']):6.3f} {stake:7.2f}  {ret:8.2f}  {ret-stake:+8.2f}"
            + (f"   [{r['note']}]" if r["note"] else "")
        )

    print()
    print(_line("all", data))
    for site in sorted({r["site"] for r in data}):
        print(_line(site, [r for r in data if r["site"] == site]))
    for kind in ("single", "2-fold", "3-fold", "4-fold", "5-fold"):
        sub = [r for r in data if r["kind"] == kind]
        if sub:
            print(_line(kind, sub))

    print("\nby day:")
    days: dict[str, list[dict]] = {}
    for r in data:
        days.setdefault(r["date"], []).append(r)
    running = 0.0
    for day in sorted(days):
        sub = days[day]
        net = _sum(sub, "return_usd") - _sum(sub, "stake_usd")
        running += net
        print(
            f"  {day}  n{len(sub):>2}  staked {_sum(sub, 'stake_usd'):7,.2f}  "
            f"net {net:+8,.2f}   cumulative {running:+9,.2f}"
        )

    if open_rows:
        print("\nopen (not in the totals):")
        for r in open_rows:
            stake = float(r["stake_usd"])
            odds = float(r["odds"])
            print(f"  {r['bet_id']} {r['date']} {r['site']:6} {r['kind']:7} "
                  f"{odds:6.3f} stake {stake:7.2f} -> if won {stake*odds:8.2f}")

    flagged = [r for r in data if r["note"]]
    if flagged:
        print("\nflagged rows:")
        for r in flagged:
            print(f"  {r['date']} {r['site']:6} {r['kind']:7} {r['note']}")


if __name__ == "__main__":
    main()
