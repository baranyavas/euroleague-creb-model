"""EuroLeague public API: fetch + cache + parse.

Endpoints used (no key, no nba_api equivalent):
    /v1/results?seasonCode=E2026          -> every game of the season
    /v1/games?seasonCode=E2026&gameCode=N -> one box score

Raw XML is cached under data/raw/<season>/ so re-runs are offline.
"""

from __future__ import annotations

import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

from . import config


# --------------------------------------------------------------------------
# fetch
# --------------------------------------------------------------------------

def _get(url: str, dest, refresh: bool = False) -> bytes:
    if dest.exists() and not refresh:
        return dest.read_bytes()

    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        headers={"User-Agent": config.USER_AGENT, "Accept": "application/xml"},
    )
    last_error = None
    for attempt in range(3):
        try:
            data = urllib.request.urlopen(req, timeout=45).read()
            dest.write_bytes(data)
            return data
        except Exception as exc:  # network hiccup
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"could not fetch {url}: {last_error}")


def results_xml(season: str, refresh: bool = False) -> bytes:
    return _get(
        f"{config.API}/results?seasonCode={season}",
        config.DATA_RAW / season / "results.xml",
        refresh=refresh,
    )


def game_xml(season: str, code: str, refresh: bool = False) -> bytes:
    return _get(
        f"{config.API}/games?seasonCode={season}&gameCode={code}",
        config.DATA_RAW / season / "games" / f"{code}.xml",
        refresh=refresh,
    )


# --------------------------------------------------------------------------
# parse helpers
# --------------------------------------------------------------------------

def _int(el, tag: str, default: int = 0) -> int:
    if el is None:
        return default
    value = el.findtext(tag)
    if value is None or value == "":
        return default
    try:
        return int(float(value))
    except ValueError:
        return default


def _date(iso: str) -> str:
    """'Sep 29, 2026' -> '2026-09-29'."""
    return datetime.strptime(iso.strip(), "%b %d, %Y").date().isoformat()


def parse_results(data: bytes) -> list[dict]:
    root = ET.fromstring(data)
    games = []
    for g in root.findall("game"):
        if g.findtext("played") != "true":
            continue
        games.append(
            {
                "season": g.findtext("gamecode", "").split("_")[0],
                "code": g.findtext("gamecode", "").split("_")[-1],
                "phase": g.findtext("round"),
                "group": g.findtext("group"),
                "gameday": int(g.findtext("gameday") or 0),
                "date": _date(g.findtext("date")),
                "time": g.findtext("time"),
                "home_code": g.findtext("homecode"),
                "away_code": g.findtext("awaycode"),
                "home_name": g.findtext("hometeam"),
                "away_name": g.findtext("awayteam"),
                "home_score": int(g.findtext("homescore") or 0),
                "away_score": int(g.findtext("awayscore") or 0),
            }
        )
    return games


def _side(club) -> dict:
    """One team's box score -> c-reb and context."""
    totals = club.find("totals")
    total = totals[0] if totals is not None and len(totals) else None
    players = club.find("playerstats")
    players = list(players) if players is not None else []

    # The box score carries a pseudo-player called "Team" that holds the
    # team rebounds. It is the 'team row' of the settlement rule.
    team_rows = [
        p for p in players
        if (p.findtext("PlayerName") or "").strip().lower() == "team"
    ]
    real_players = [p for p in players if p not in team_rows]

    team_reb = _int(team_rows[0], "TotalRebounds") if team_rows else None
    player_reb = sum(_int(p, "TotalRebounds") for p in real_players)

    total_reb = _int(total, "TotalRebounds")
    if team_reb is None:
        # Fallback: what is left once every player is accounted for.
        team_reb = max(0, total_reb - player_reb)

    creb = total_reb - team_reb
    fga = _int(total, "FieldGoalsAttemptedTotal")
    fgm = _int(total, "FieldGoalsMadeTotal")
    fta = _int(total, "FreeThrowsAttempted")
    ftm = _int(total, "FreeThrowsMade")
    tov = _int(total, "Turnovers")

    # The totals row's O+D includes the team-rebound bucket, so the raw split
    # cannot be used as a player-only rebound profile. Subtract the team row.
    oreb_total = _int(total, "OffensiveRebounds")
    dreb_total = _int(total, "DefensiveRebounds")
    team_oreb = _int(team_rows[0], "OffensiveRebounds") if team_rows else 0
    team_dreb = _int(team_rows[0], "DefensiveRebounds") if team_rows else 0
    oreb = max(0, oreb_total - team_oreb)
    dreb = max(0, dreb_total - team_dreb)

    return {
        "code": club.get("code"),
        "name": (club.get("name") or "").strip(),
        "score": _int(club, "score") if club.get("score") is None else int(club.get("score") or 0),
        "total_reb": total_reb,
        "team_reb": team_reb,
        "creb": creb,
        "player_reb_sum": player_reb,
        "oreb": oreb,
        "dreb": dreb,
        "oreb_total": oreb_total,
        "dreb_total": dreb_total,
        "fga": fga,
        "fgm": fgm,
        "fta": fta,
        "ftm": ftm,
        "tov": tov,
        "missed_fg": fga - fgm,
        # standard possession estimate (team OREB keeps the possession alive)
        "poss": fga + 0.44 * fta - oreb_total + tov,
        "players": len(real_players),
    }


def parse_game(data: bytes) -> dict:
    root = ET.fromstring(data)
    home = _side(root.find("localclub"))
    away = _side(root.find("roadclub"))
    return {
        "season": root.get("seasoncode"),
        "phase": root.get("phasetypecode"),
        "gameday": int(root.get("number") or 0),
        "datetime": root.get("cetdate"),
        "home": home,
        "away": away,
    }
