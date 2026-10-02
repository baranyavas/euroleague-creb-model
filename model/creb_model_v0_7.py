"""
euroleague c-reb model v0.7

pregame forecasting model:
1) opportunity layer: fga + fg% -> expected missed fg
2) rebound realization: reboppr-o / reboppr-d
3) team identity: shrunk current-vs-historical c-reb signal
4) h2h: separate, stability-weighted anchor
5) regression: fit only on game-level data; never use provider line as a predictor

settlement target:
    c-reb = player-credited orb + player-credited drb
team rebounds are excluded.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


HIST_CREB_INTERCEPT = 3.126
HIST_CREB_MISSED_FG_BETA = 0.8719


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def shrunk_current_weight(n_games: int, prior_games: float = 6.0) -> float:
    """Small-sample shrinkage: n/(n+prior_games)."""
    return n_games / (n_games + prior_games)


def team_identity_multiplier(
    current_c_reb: Optional[float],
    historical_c_reb: Optional[float],
    n_games: int,
    prior_games: float = 6.0,
    max_adjustment: float = 0.08,
) -> float:
    """
    Generic current-team-characteristic signal.

    A team's current C-REB average can indicate that its rebound identity has
    shifted from last season. With only G1/G2 this signal is heavily shrunk.
    It is capped so two games cannot dominate the forecast.
    """
    if current_c_reb is None or historical_c_reb in (None, 0):
        return 1.0

    raw_ratio = current_c_reb / historical_c_reb - 1.0
    w = shrunk_current_weight(n_games, prior_games)
    adjustment = clamp(w * raw_ratio, -max_adjustment, max_adjustment)
    return 1.0 + adjustment


def expected_missed_fg(fga: float, fg_pct: float) -> float:
    """Opportunity layer: expected missed field goals."""
    return max(0.0, fga * (1.0 - fg_pct))


def matchup_reboppr_o(
    team_reboppr_o: Optional[float],
    opponent_reboppr_d: Optional[float],
) -> float:
    """
    Matchup-adjusted offensive rebound realization.

    For a miss by this team, either the team gets the ORB or the opponent gets
    the DRB (ignoring the small team-rebound bucket). Blend the team's own ORB
    realization with the complement of the opponent's DRB rate.
    """
    own = team_reboppr_o if team_reboppr_o is not None else 0.0
    opp_d = opponent_reboppr_d if opponent_reboppr_d is not None else 0.0

    if own <= 0:
        return 0.0
    if opp_d <= 0:
        return own

    return clamp(0.50 * own + 0.50 * (1.0 - opp_d), 0.0, 0.50)


def matchup_reboppr_d(
    team_reboppr_d: Optional[float],
    opponent_reboppr_o: Optional[float],
) -> float:
    """
    Matchup-adjusted defensive rebound realization.

    For an opponent miss, either this team gets the DRB or the opponent gets
    the ORB. Blend our own DRB rate with the complement of the opponent's ORB.
    """
    own = team_reboppr_d if team_reboppr_d is not None else 0.0
    opp_o = opponent_reboppr_o if opponent_reboppr_o is not None else 0.0

    if own <= 0:
        return 0.0
    if opp_o <= 0:
        return own

    return clamp(0.50 * own + 0.50 * (1.0 - opp_o), 0.0, 0.95)


@dataclass
class TeamProfile:
    name: str

    historical_c_reb: Optional[float] = None
    current_c_reb: Optional[float] = None
    current_games: int = 0

    fga: Optional[float] = None
    fg_pct: Optional[float] = None
    pace: Optional[float] = None

    reboppr_o: Optional[float] = None
    reboppr_d: Optional[float] = None


@dataclass
class MatchupInput:
    home: TeamProfile
    away: TeamProfile

    # H2H is separate from the full-season historical baseline.
    h2h_avg: Optional[float] = None
    h2h_gap: Optional[float] = None


def identity_adjusted_c_reb(profile: TeamProfile) -> Optional[float]:
    if profile.current_c_reb is None and profile.historical_c_reb is None:
        return None

    if profile.historical_c_reb is None:
        return profile.current_c_reb

    if profile.current_c_reb is None or profile.current_games <= 0:
        return profile.historical_c_reb

    w = shrunk_current_weight(profile.current_games)
    return (
        (1.0 - w) * profile.historical_c_reb
        + w * profile.current_c_reb
    )


def base_forecast(matchup: MatchupInput) -> float:
    """
    Main two-stage forecast.

    Stage 1: expected misses from each team's own FGA/FG%.
    Stage 2: expected ORB + expected DRB for each team.

    Missing rebound-split inputs fall back to the historical missed-FG OLS
    rather than inventing a team-specific rate.
    """
    h, a = matchup.home, matchup.away

    if (
        h.fga is not None and h.fg_pct is not None
        and a.fga is not None and a.fg_pct is not None
        and h.reboppr_o is not None and h.reboppr_d is not None
        and a.reboppr_o is not None and a.reboppr_d is not None
    ):
        h_miss = expected_missed_fg(h.fga, h.fg_pct)
        a_miss = expected_missed_fg(a.fga, a.fg_pct)

        h_o = matchup_reboppr_o(h.reboppr_o, a.reboppr_d)
        h_d = matchup_reboppr_d(h.reboppr_d, a.reboppr_o)
        a_o = matchup_reboppr_o(a.reboppr_o, h.reboppr_d)
        a_d = matchup_reboppr_d(a.reboppr_d, h.reboppr_o)

        h_creb = h_miss * h_o + a_miss * h_d
        a_creb = a_miss * a_o + h_miss * a_d
        forecast = h_creb + a_creb
    else:
        total_miss = 0.0
        for p in (h, a):
            if p.fga is not None and p.fg_pct is not None:
                total_miss += expected_missed_fg(p.fga, p.fg_pct)

        forecast = (
            HIST_CREB_INTERCEPT
            + HIST_CREB_MISSED_FG_BETA * total_miss
        )

    # Generic team-identity adjustment. The weight is intentionally small
    # until enough current-season games exist to validate it out of sample.
    identity_values = []
    for p in (h, a):
        adj = identity_adjusted_c_reb(p)
        if adj is not None:
            identity_values.append(adj)

    if identity_values:
        identity_target = sum(identity_values)
        baseline_values = [
            p.historical_c_reb for p in (h, a)
            if p.historical_c_reb is not None
        ]
        if baseline_values:
            baseline_target = sum(baseline_values)
            forecast += 0.20 * (identity_target - baseline_target)

    # Stable H2H anchor; unstable H2H gets less influence.
    if matchup.h2h_avg is not None:
        h2h_weight = 0.10
        if matchup.h2h_gap is not None:
            stability = clamp(1.0 - abs(matchup.h2h_gap) / 20.0, 0.0, 1.0)
            h2h_weight *= stability
        forecast = (1.0 - h2h_weight) * forecast + h2h_weight * matchup.h2h_avg

    return forecast


def line_gap(forecast: float, provider_line: float) -> float:
    """Positive = forecast above line; negative = forecast below line."""
    return forecast - provider_line


def fit_game_level_ols(df: pd.DataFrame):
    """
    Fit the research regression on game-level rows.

    Required columns:
        c_reb, missed_fg

    Optional columns:
        possessions, fga, fg_pct

    The core regression starts with missed_fg because it had the strongest
    historical relationship with C-REB. Additional variables should be added
    only after out-of-sample validation.
    """
    import statsmodels.api as sm

    cols = ["missed_fg", "possessions", "fga", "fg_pct"]
    use = [c for c in cols if c in df.columns]

    if "c_reb" not in df.columns or "missed_fg" not in df.columns:
        raise ValueError("df must contain c_reb and missed_fg")

    work = df[["c_reb"] + use].dropna().copy()
    X = sm.add_constant(work[use])
    y = work["c_reb"]

    return sm.OLS(y, X).fit()


if __name__ == "__main__":
    print("euroleague c-reb model v0.7 loaded")
