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

# One canonical id scheme, everywhere: data files, model, cards, CLI.
# The EuroLeague API speaks different codes for eleven clubs, so `club_id`
# converts them **at the edge** (build, slate, nights). Nothing else should
# ever see an API code.
#
# The old two-scheme setup is gone. It made `PAR` mean Partizan in the API and
# Paris in the registry, which is exactly the kind of trap that silently prices
# the wrong game. Paris is PRS and Partizan is PRT in every file now.
CLUB_ID = {
    "IST": "EFE",   # Anadolu Efes
    "MAD": "RMA",   # Real Madrid
    "HTA": "HAP",   # Hapoel Tel Aviv
    "PAM": "VAL",   # Valencia (API says Pamesa)
    "ULK": "FEN",   # Fenerbahce (Ulker)
    "MUN": "BAY",   # Bayern Munich
    "PAR": "PRT",   # Partizan — the API's PAR is NOT Paris
    "RED": "CZV",   # Crvena zvezda
    "TEL": "MAC",   # Maccabi Tel Aviv
    "BES": "BJK",   # Besiktas
    "MCO": "MCO",
}


def club_id(code: str) -> str:
    """API code -> canonical id. A canonical id passes through unchanged."""
    return CLUB_ID.get(code, code)


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
    "ZAL": "Žalgiris Kaunas",
}


def short(code: str) -> str:
    """Canonical code, accepting either an API code or a canonical id."""
    return club_id(code)


def label(home: str, away: str) -> str:
    return f"{short(home)}-{short(away)}"
