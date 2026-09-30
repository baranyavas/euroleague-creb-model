"""
euroleague c-reb model v0.4

target:
    c-reb = player-credited offensive rebounds + player-credited defensive rebounds

team rebounds are excluded from the settlement target.

the model is designed for pregame forecasting. postgame residual analysis is
diagnostic only and must not be used to leak information into an old forecast.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class team_profile:
    c_reb: float
    orb: float
    drb: float
    fga: float
    missed_fg: float
    reboppr_o: Optional[float] = None
    reboppr_d: Optional[float] = None


@dataclass
class matchup_input:
    home: team_profile
    away: team_profile
    pace: float
    h2h_c_reb: Optional[float] = None
    current_weight: float = 0.10
    h2h_weight: float = 0.10


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def expected_team_missed_fg(profile: team_profile) -> float:
    return profile.missed_fg


def rebound_realization_factor(profile: team_profile) -> float:
    """
    use the team's recent/historical rebound conversion when available.

    reboppr-o is team orb / own missed fg.
    reboppr-d is team drb / opponent missed fg.

    for the first implementation, a neutral factor of 1.0 is used when the
    relevant split is unavailable. this keeps the forecast conservative rather
    than inventing a value.
    """
    values = [x for x in (profile.reboppr_o, profile.reboppr_d) if x is not None]
    return sum(values) / len(values) if values else 1.0


def base_matchup_forecast(matchup: matchup_input) -> float:
    """
    baseline forecast before current-season shrinkage and h2h adjustment.

    missed fg is the strongest direct opportunity variable in the 2025-26
    sample. the historical one-variable relationship was approximately:

        c_reb = 3.126 + 0.8719 * missed_fg

    the matchup forecast averages the two teams' missed-fg opportunity and
    applies a conservative rebound-realization adjustment.
    """
    total_missed_fg = (
        expected_team_missed_fg(matchup.home)
        + expected_team_missed_fg(matchup.away)
    )

    opportunity_projection = 3.126 + 0.8719 * total_missed_fg

    realization = (
        rebound_realization_factor(matchup.home)
        + rebound_realization_factor(matchup.away)
    ) / 2.0

    # keep early versions conservative; reboppr is an adjustment, not a
    # literal probability.
    realization_adj = clamp(realization, 0.90, 1.05)

    return opportunity_projection * realization_adj


def forecast_c_reb(matchup: matchup_input,
                   current_season_projection: Optional[float] = None) -> float:
    """
    produce a pregame forecast.

    current-season data is shrunk toward the historical model because g1/g2 are
    very small samples. current_weight should increase as the season grows.

    provider lines are not inputs to the forecast. they are compared against
    the forecast only after the forecast is locked.
    """
    historical = base_matchup_forecast(matchup)

    forecast = historical

    if current_season_projection is not None:
        w = clamp(matchup.current_weight, 0.0, 1.0)
        forecast = (1.0 - w) * forecast + w * current_season_projection

    if matchup.h2h_c_reb is not None:
        w = clamp(matchup.h2h_weight, 0.0, 1.0)
        forecast = (1.0 - w) * forecast + w * matchup.h2h_c_reb

    return forecast


def line_gap(forecast: float, provider_line: float) -> float:
    """positive means forecast is above the line; negative means below."""
    return forecast - provider_line


def opportunity_flag(total_fga: float,
                     total_fg_pct: float,
                     high_fga_threshold: float = 134.0,
                     low_fg_pct_threshold: float = 0.4454) -> str:
    """
    primary opportunity rule:
        high fga OR low fg%.

    both conditions together are treated as an extreme subgroup, not the main
    filter.
    """
    high_fga = total_fga >= high_fga_threshold
    low_fg = total_fg_pct <= low_fg_pct_threshold

    if high_fga and low_fg:
        return "extreme_both"
    if high_fga or low_fg:
        return "high_opportunity"
    return "normal"


def decision(forecast: float,
             provider_line: float,
             minimum_gap: float = 1.0) -> str:
    """
    simple research-stage decision rule.

    under only:
      forecast + minimum_gap <=? no bet
      forecast sufficiently below line -> candidate under

    this function intentionally does not encode a final betting threshold;
    threshold calibration belongs to the validation stage.
    """
    if forecast <= provider_line - minimum_gap:
        return "under_candidate"
    return "pass"


if __name__ == "__main__":
    print("c-reb model v0.4 loaded")
