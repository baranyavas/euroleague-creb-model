"""Paths, seasons and the settlement definition.

Settlement target (do not change):
    c-reb = total-row T - team-row T
i.e. player-credited offensive + defensive rebounds only.
Team rebounds are context data and never part of c-reb.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROC = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"

API = "https://api-live.euroleague.net/v1"

# 2025-26 is the historical baseline, 2026-27 is the live season.
SEASONS = ["E2025", "E2026"]
LIVE_SEASON = "E2026"
BASE_SEASON = "E2025"

# Regular season only. Results XML also contains play-in / playoffs.
REGULAR_SEASON_ONLY = True

# Market reference, measured on the 19 recorded 2026-27 forecasts.
# The provider posts c-reb but posts it high: line - forecast averaged +5.63.
MARKET_SHADE = 5.63
MARKET_SHADE_SD = 2.43

# Parlay (combo) rule: legs may only be joined when their tip-offs are within
# this many minutes of the first leg's tip. A line opens 60 minutes before its
# own tip, so anything wider than this cannot be bet as one ticket.
COMBO_WINDOW_MIN = 45

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)

# Registry ids used in data/decision_registry.md, keyed by the club code in
# the results XML. Most official codes already match; these differ.
#   PRS = Paris Basketball   -> PAR (the registry's Paris id)
#   PAR = Partizan Belgrade  -> PTZ
#   RED = Crvena Zvezda      -> ZVE
#   TEL = Maccabi Tel Aviv   -> MAC
#   BES = Besiktas           -> BJK
CLUB_ID = {
    "IST": "EFE",
    "MAD": "RMA",
    "HTA": "HAP",
    "PAM": "VAL",
    "ULK": "FEN",
    "MUN": "BAY",
    "PRS": "PAR",
    "PAR": "PTZ",
    "RED": "ZVE",
    "TEL": "MAC",
    "BES": "BJK",
    "MCO": "MCO",
}


def club_id(code: str) -> str:
    return CLUB_ID.get(code, code)


# --------------------------------------------------------------------------
# display codes (reading only — every CSV keeps the registry ids above)
# --------------------------------------------------------------------------

# The user asked (2026-11-22) for the three-letter codes he actually uses.
# Both the API codes and the registry ids map onto the same display code, so
# `short()` accepts either. Files are untouched: `decision_registry.md`,
# `decisions_2026_27.csv` and the forecast CLI keep the registry ids.
TEAM_NAME = {
    "BAR": "Barcelona",
    "OLY": "Olympiacos",
    "FEN": "Fenerbahçe",
    "EFE": "Anadolu Efes",
    "RMA": "Real Madrid",
    "BAY": "Bayern München",
    "MCO": "Monaco",
    "PRS": "Paris",
    "PRT": "Partizan",
    "CZV": "Crvena zvezda",
    "MAC": "Maccabi Tel Aviv",
    "BJK": "Beşiktaş",
    "HAP": "Hapoel Tel Aviv",
    "VAL": "Valencia",
    "PAN": "Panathinaikos",
    "ASV": "ASVEL",
    "MIL": "Olimpia Milano",
    "BAS": "Baskonia",
    "VIR": "Virtus Bologna",
    "DUB": "Dubai",
}

DISPLAY = {
    # API code -> display code
    "ULK": "FEN",
    "IST": "EFE",
    "MAD": "RMA",
    "MUN": "BAY",
    "PRS": "PRS",
    "PAR": "PRT",
    "RED": "CZV",
    "TEL": "MAC",
    "BES": "BJK",
    "HTA": "HAP",
    "PAM": "VAL",
    "ZVE": "CZV",
    "PTZ": "PRT",
}


def short(code: str) -> str:
    """Readable three-letter code for either an API code or a registry id."""
    return DISPLAY.get(code, code)


def label(home: str, away: str) -> str:
    return f"{short(home)}-{short(away)}"
