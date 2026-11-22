"""Which nights can carry a 4-leg ticket?

    python -m src.nights                    # every remaining regular-season night
    python -m src.nights --from 2026-11-24  # from a given date
    python -m src.nights --round 14         # one round
    python -m src.nights --write            # also write the report

The 45-minute rule says a ticket may only join legs that tip within 45 minutes
of its first leg, because each line opens 60 minutes before its own tip-off.
So a 4-fold needs **four games inside one 45-minute window**, and most nights
cannot supply that. This reads the official v2 schedule (all 380 regular-season
games with tip-off times) and lists the nights where four legs are possible,
so the 4-fold can be planned instead of discovered at 21:00.

Schedule XML is cached under data/raw/E2026/schedule.xml.
"""

from __future__ import annotations

import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta

from . import config

SCHEDULE = config.DATA_RAW / config.LIVE_SEASON / "schedule.xml"
REPORT = config.REPORTS / "four_leg_nights_2026_27.md"
URL = (
    f"https://api-live.euroleague.net/v2/competitions/E/seasons/"
    f"{config.LIVE_SEASON}/games"
)


def schedule_xml(refresh: bool = False) -> bytes:
    if SCHEDULE.exists() and not refresh:
        return SCHEDULE.read_bytes()
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": config.USER_AGENT, "Accept": "application/xml"},
    )
    data = urllib.request.urlopen(req, timeout=45).read()
    SCHEDULE.parent.mkdir(parents=True, exist_ok=True)
    SCHEDULE.write_bytes(data)
    return data


def _club(game: ET.Element, side: str) -> str:
    club = game.find(f"{side}/Club")
    if club is None:
        return "?"
    return club.findtext("Code") or "?"


def _rows(raw: bytes) -> list[dict]:
    """The endpoint returns JSON or XML depending on how it feels; accept both."""
    if raw.lstrip().startswith(b"{"):
        payload = json.loads(raw)
        out = []
        for g in payload["data"]:
            out.append(
                {
                    "code": str(g["gameCode"]),
                    "round": int(g["round"]),
                    "utc": g["utcDate"],
                    "local": g["localDate"] or g["utcDate"],
                    "home": (g.get("local") or {}).get("club", {}).get("code", "?"),
                    "away": (g.get("road") or {}).get("club", {}).get("code", "?"),
                    "played": bool(g["played"]),
                    "status": g.get("gameStatus") or "",
                    "hour_confirmed": bool(g.get("confirmedHour")),
                }
            )
        return out

    root = ET.fromstring(raw)
    out = []
    for g in root.iter("GameDetailsModel"):
        utc = g.findtext("UtcDate")
        if not utc:
            continue
        out.append(
            {
                "code": g.findtext("GameCode"),
                "round": int(g.findtext("Round") or 0),
                "utc": utc,
                "local": g.findtext("LocalDate") or utc,
                "home": _club(g, "Local"),
                "away": _club(g, "Road"),
                "played": (g.findtext("Played") or "").lower() == "true",
                "status": g.findtext("GameStatus") or "",
                "hour_confirmed": (g.findtext("ConfirmedHour") or "").lower() == "true",
            }
        )
    return out


def games(refresh: bool = False) -> list[dict]:
    out: list[dict] = []
    for g in _rows(schedule_xml(refresh)):
        out.append(
            {
                **g,
                "utc": datetime.fromisoformat(g["utc"].replace("Z", "+00:00")),
                "date": date.fromisoformat(g["local"][:10]),
            }
        )
    return out


def nights(data: list[dict]) -> dict[date, list[dict]]:
    by: dict[date, list[dict]] = {}
    for g in data:
        by.setdefault(g["date"], []).append(g)
    for sub in by.values():
        sub.sort(key=lambda g: g["utc"])
    return dict(sorted(by.items()))


def widest_window(sub: list[dict], window: int = config.COMBO_WINDOW_MIN) -> list[dict]:
    """The largest legal window: games tipping within `window` of the first."""
    best: list[dict] = []
    for i, first in enumerate(sub):
        grp = [
            g
            for g in sub[i:]
            if g["utc"] - first["utc"] <= timedelta(minutes=window)
        ]
        if len(grp) > len(best):
            best = grp
    return best


def max_legs(sub: list[dict], window: int = config.COMBO_WINDOW_MIN) -> int:
    return len(widest_window(sub, window))


def _fmt(g: dict) -> str:
    return f"{g['utc']:%H:%M}Z {config.label(g['home'], g['away'])}"


def main(
    from_date: date | None = None,
    round_no: int | None = None,
    write: bool = False,
    refresh: bool = False,
) -> None:
    data = games(refresh)
    if not data:
        raise SystemExit("schedule is empty")

    sub = data
    if round_no is not None:
        sub = [g for g in sub if g["round"] == round_no]
    if from_date is not None:
        sub = [g for g in sub if g["date"] >= from_date]
    if not write and round_no is None and from_date is None:
        sub = [g for g in sub if not g["played"]]

    by = nights([g for g in sub if not g["played"]])
    lines: list[str] = []
    say = lines.append

    t0 = f"from {from_date}" if from_date else (
        f"round {round_no}" if round_no else "remaining regular season"
    )
    say(f"# 4-leg nights — {t0}")
    say("")
    say("A 4-fold needs four games inside one 45-minute window (each line opens")
    say("60 minutes before its own tip). `legs` is the widest legal window on")
    say("that night. Only nights with **4+** can carry a 4-fold; a 3 is a")
    say("3-fold night, not four legs squeezed.")
    say("")
    say("```")
    say(f"{'date':12} {'R':>3} {'legs':>4}  window")
    counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    four: list[tuple[date, list[dict]]] = []
    for day, games_that_night in by.items():
        if not games_that_night:
            continue
        win = widest_window(games_that_night)
        n = len(win)
        counts[min(n, 5)] = counts.get(min(n, 5), 0) + 1
        rnd = games_that_night[0]["round"]
        stamp = "***" if n >= 4 else "   "
        say(
            f"{day} {rnd:>3} {n:>4}  {stamp} "
            + (win[0]["utc"].strftime("%H:%M") + "Z: " if win else "")
            + ", ".join(config.label(g['home'], g['away']) for g in win)
        )
        if n >= 4:
            four.append((day, win))
    say("```")
    say("")

    total = sum(counts.values())
    say(f"- upcoming nights: **{total}**")
    say(f"- 4-leg nights: **{counts.get(4, 0) + counts.get(5, 0)}**")
    say(f"- 3-leg nights: **{counts.get(3, 0)}**")
    say(f"- 2-leg nights: **{counts.get(2, 0)}**")
    say(f"- 1-leg nights: **{counts.get(1, 0)}**")
    say("")

    if four:
        say("## The 4-fold candidates")
        say("")
        for day, win in four:
            say(f"### {day} — round {win[0]['round']}")
            say("")
            for g in win:
                say(f"- `{g['utc']:%H:%M}Z` {config.short(g['home'])} vs {config.short(g['away'])}")
            say("")
            say(f"Window: {win[0]['utc']:%H:%M}Z – {win[-1]['utc']:%H:%M}Z "
                f"({int((win[-1]['utc'] - win[0]['utc']).total_seconds() // 60)} min)")
            say("")

    text = "\n".join(lines)
    print(text)
    if write:
        REPORT.write_text(text, encoding="utf-8")
        print(f"wrote {REPORT.relative_to(config.ROOT)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    start = None
    rnd = None
    if "--from" in args:
        start = date.fromisoformat(args[args.index("--from") + 1])
    if "--round" in args:
        rnd = int(args[args.index("--round") + 1])
    main(
        from_date=start,
        round_no=rnd,
        write="--write" in args,
        refresh="--refresh" in args,
    )
