"""Bankroll summary: totals, weeks and limit eras.

    python -m src.bankroll            # print
    python -m src.bankroll --write    # also write reports/bankroll_2026_27.md

All numbers come from data/bets_2026_27.csv, where each row carries the amount
staked and the amount actually returned.
"""

from __future__ import annotations

import csv
from datetime import date

from . import config

PATH = config.ROOT / "data" / "bets_2026_27.csv"
REPORT = config.ROOT / "reports" / "bankroll_2026_27.md"

SEASON_START = date(2026, 9, 24)

# Limit eras: what the sites let him put on a single ticket.
ERAS = [
    ("E1 — 20 $ limiti", None, date(2026, 10, 8)),
    ("E2 — 65 $ bandı", date(2026, 10, 9), date(2026, 11, 5)),
    ("E3 — Duel eklendi (~140 $)", date(2026, 11, 6), None),
]


def rows() -> list[dict]:
    with PATH.open(newline="", encoding="utf-8") as fh:
        data = list(csv.DictReader(fh))
    return sorted(data, key=lambda r: (r["date"], r["time"], r["bet_id"]))


def money(data: list[dict], key: str) -> float:
    return sum(float(r[key]) for r in data)


def totals(data: list[dict]) -> tuple[float, float, float]:
    staked = money(data, "stake_usd")
    ret = money(data, "return_usd")
    return staked, ret, ret - staked


def table(label: str, data: list[dict]) -> str:
    staked, ret, net = totals(data)
    won = sum(1 for r in data if r["result"] == "won")
    roi = 100 * net / staked if staked else 0.0
    return (
        f"{label:26} {len(data):>3}  {won:>2}/{len(data)-won:<2}  "
        f"{staked:>9,.2f} {ret:>9,.2f} {net:>+10,.2f} {roi:>+7.1f}%"
    )


HEAD = f"{'':26} {'n':>3}  {'W/L':<5} {'staked':>9} {'returned':>9} {'net':>10} {'ROI':>8}"


def main(write: bool = False) -> None:
    data = rows()
    staked, ret, net = totals(data)
    first = date.fromisoformat(data[0]["date"])
    last = date.fromisoformat(data[-1]["date"])
    cal_days = (last - first).days + 1
    bet_days = len({r["date"] for r in data})

    lines: list[str] = []
    say = lines.append

    say("# Bankroll — 2026-27")
    say("")
    say(f"Ledger: `data/bets_2026_27.csv` — {len(data)} tickets, "
        f"{data[0]['date']} → {data[-1]['date']}.")
    say("")
    say("| | |")
    say("|---|---:|")
    say(f"| tickets | **{len(data)}** |")
    say(f"| won / lost | {sum(1 for r in data if r['result']=='won')} / "
        f"{sum(1 for r in data if r['result']!='won')} |")
    say(f"| staked | **{staked:,.2f}** |")
    say(f"| returned | **{ret:,.2f}** |")
    say(f"| net | **{net:+,.2f}** |")
    say(f"| ROI | **{100*net/staked:+.1f}%** |")
    say(f"| calendar days (first → last ticket) | {cal_days} |")
    say(f"| betting days | {bet_days} |")
    say(f"| net per calendar day | {net/cal_days:+,.2f} |")
    say(f"| net per betting day | {net/bet_days:+,.2f} |")
    say(f"| net per day since season start ({SEASON_START}) | "
        f"{net/((last-SEASON_START).days+1):+,.2f} |")
    say("")

    say("## By site")
    say("")
    say("```")
    say(HEAD)
    for site in sorted({r["site"] for r in data}):
        say(table(site, [r for r in data if r["site"] == site]))
    say(table("all", data))
    say("```")
    say("")

    say("## By ticket type")
    say("")
    say("```")
    say(HEAD)
    for kind in ("single", "2-fold", "3-fold", "4-fold", "5-fold"):
        sub = [r for r in data if r["kind"] == kind]
        if sub:
            say(table(kind, sub))
    say("```")
    say("")

    say("## Weeks (W1 starts at the first ticket)")
    say("")
    say("```")
    say(f"{'week':10} {'dates':25} {'n':>3}  {'W/L':<5} {'staked':>9} {'net':>10} {'ROI':>8}")
    week = 1
    cur = first
    while cur <= last:
        hi = min(date.fromordinal(cur.toordinal() + 6), last)
        sub = [r for r in data if cur <= date.fromisoformat(r["date"]) <= hi]
        s, _, n = totals(sub)
        won = sum(1 for r in sub if r["result"] == "won")
        roi = 100 * n / s if s else 0.0
        say(f"W{week:<9} {cur} .. {hi}  {len(sub):>3}  {won:>2}/{len(sub)-won:<2}  "
            f"{s:>9,.2f} {n:>+10,.2f} {roi:>+7.1f}%")
        week += 1
        cur = date.fromordinal(hi.toordinal() + 1)
    say("```")
    say("")

    say("## Stake ladder (what the slips actually show)")
    say("")
    say("```")
    say(f"{'period':25} {'n':>3} {'median':>7} {'min':>7} {'max':>7}")
    ladder = [
        ("2026-09-28", "2026-09-30"),
        ("2026-10-01", "2026-10-08"),
        ("2026-10-09", "2026-11-05"),
        ("2026-11-06", "2026-11-20"),
    ]
    for lo, hi in ladder:
        sub = [r for r in data if lo <= r["date"] <= hi]
        if not sub:
            continue
        stakes = sorted(float(r["stake_usd"]) for r in sub)
        say(f"{lo} .. {hi}  {len(sub):>3} {stakes[len(stakes)//2]:>7.1f} "
            f"{min(stakes):>7.2f} {max(stakes):>7.2f}")
    say("```")
    say("")

    say("## Limit eras")
    say("")
    say("```")
    say(f"{'era':28} {'dates':25} {'n':>3} {'med stake':>9} {'max':>7} {'net':>10} {'ROI':>8} {'per day':>8}")
    for label, lo, hi in ERAS:
        sub = [
            r for r in data
            if (lo is None or date.fromisoformat(r["date"]) >= lo)
            and (hi is None or date.fromisoformat(r["date"]) <= hi)
        ]
        if not sub:
            continue
        s, _, n = totals(sub)
        stakes = sorted(float(r["stake_usd"]) for r in sub)
        med = stakes[len(stakes) // 2]
        a = date.fromisoformat(sub[0]["date"])
        b = date.fromisoformat(sub[-1]["date"])
        days = (b - a).days + 1
        say(f"{label:28} {sub[0]['date']} .. {sub[-1]['date']}  {len(sub):>3} "
            f"{med:>9.1f} {max(stakes):>7.2f} {n:>+10,.2f} {100*n/s:>+7.1f}% {n/days:>+8.2f}")
    say("```")
    say("")

    flagged = [r for r in data if r["note"]]
    say("## Flagged rows")
    say("")
    for r in flagged:
        say(f"- `{r['date']}` {r['site']} {r['kind']} — {r['note']}")
    say("")

    text = "\n".join(lines)
    print(text)
    if write:
        REPORT.write_text(text, encoding="utf-8")
        print(f"wrote {REPORT.relative_to(config.ROOT)}")


if __name__ == "__main__":
    import sys

    main(write="--write" in sys.argv)
