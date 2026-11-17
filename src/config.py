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
