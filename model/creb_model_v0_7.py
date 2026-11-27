"""
euroleague c-reb model v0.7

pregame forecasting model:
1) opportunity layer: fga + fg% -> expected missed fg
   (v0.7.1: blended with a shrunk direct missed-FG average, see below)
2) rebound realization: reboppr-o / reboppr-d
3) team identity: shrunk current-vs-historical c-reb signal
4) h2h: separate, stability-weighted anchor
5) regression: fit only on game-level data; never use provider line as a predictor

settlement target:
    c-reb = player-credited orb + player-credited drb
team rebounds are excluded.

v0.7.1 (2026-11-26) — opportunity layer
----------------------------------------
fga * (1 - fg%) is two noisy estimates multiplied together. A team that is
shooting 45% over 13 games is not a 45% team, and the product extrapolates
that noise. Measured on the 139 live games, the miss volume was the dominant
error source: mean absolute contribution 6.17 against 3.37 for the rebound
realisation, and the miss estimate itself had MAE 6.68.

Replacing it with a shrunk direct average of observed missed FG per game
(prior = league mean, 8 pseudo-games) cuts forecast MAE from 6.38 to 6.08 and
improves every cut of the sample: first 70 games 6.78 -> 6.22, last 50 6.07 ->
5.97, games with a recorded line 6.49 -> 6.26. The blend keeps 25% of the
structural estimate so the pace/accuracy decomposition still speaks.

Rejected after testing, for the record: blending in the opponent's defensive
FG% (bias +1.6 to +3.7), conceding-based miss estimates (MAE 6.52-7.06),
shrinking the rebound rates (MAE 6.17-6.23), and a global spread recalibration
(the fitted slope was 0.48 on H1 and 0.93 on H2, i.e. not stable).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd


HIST_CREB_INTERCEPT = 3.126
HIST_CREB_MISSED_FG_BETA = 0.8719

# v0.7.1 opportunity-layer blend. 0 = pure fga * (1 - fg%), 1 = pure shrunk
# direct missed-FG average. 0.75 was the best of the tested grid and is the
# more robust choice on the games that actually carry a provider line.
MISS_DIRECT_WEIGHT = 0.75


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


def blended_missed_fg(
    profile: TeamProfile,
    direct_weight: float = MISS_DIRECT_WEIGHT,
) -> Optional[float]:
    """
    v0.7.1 opportunity layer: structural misses blended with the shrunk direct
    average of observed missed FG per game.

    fga * (1 - fg%) multiplies two small-sample estimates. The direct average
    is already shrunk toward the league mean upstream, so it is the more
    stable of the two early in a season; keeping a quarter of the structural
    estimate preserves the pace/accuracy decomposition.
    """
    structural = None
    if profile.fga is not None and profile.fg_pct is not None:
        structural = expected_missed_fg(profile.fga, profile.fg_pct)

    direct = profile.missed_fg
    if direct is None:
        return structural
    if structural is None:
        return direct
    return (1.0 - direct_weight) * structural + direct_weight * direct


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

    # v0.7.1: shrunk direct missed-FG average, already pulled toward the league
    # mean by src/forecast.py. When present it is blended into the opportunity
    # layer; when absent the model falls back to fga * (1 - fg%) alone.
    missed_fg: Optional[float] = None

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


def base_forecast(matchup: MatchupInput, player_only: bool = False) -> float:
    """
    Main two-stage forecast.

    Stage 1: expected misses from each team's own FGA/FG%.
    Stage 2: expected ORB + expected DRB for each team.

    Missing rebound-split inputs fall back to the historical missed-FG OLS
    rather than inventing a team-specific rate.

    player_only=True keeps the rebound rates at their settled (player-only)
    level. The default blend uses the complement of the opponent rate, which
    forces ORB+DRB to 1.0 and therefore re-includes the team-rebound bucket
    that the c-reb settlement rule excludes. Use player_only=True for a
    forecast on the c-reb scale.
    """
    h, a = matchup.home, matchup.away

    if (
        h.fga is not None and h.fg_pct is not None
        and a.fga is not None and a.fg_pct is not None
        and h.reboppr_o is not None and h.reboppr_d is not None
        and a.reboppr_o is not None and a.reboppr_d is not None
    ):
        h_miss = blended_missed_fg(h)
        a_miss = blended_missed_fg(a)

        if player_only:
            h_o, h_d = h.reboppr_o, h.reboppr_d
            a_o, a_d = a.reboppr_o, a.reboppr_d
        else:
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
            miss = blended_missed_fg(p)
            if miss is not None:
                total_miss += miss

        forecast = (
            HIST_CREB_INTERCEPT
            + HIST_CREB_MISSED_FG_BETA * total_miss
        )

    # Generic team-identity adjustment. The weight is intentionally small
    # until enough current-season games exist to validate it out of sample.
    #
    # Each team is compared against its own historical baseline. A team with
    # no previous season has no baseline, so it contributes to neither side of
    # the comparison. Summing two current identities against one baseline
    # invents a whole team's worth of rebounds: BJK has no 2025-26 row, and
    # that inflated every BJK forecast by 0.20 * ~30 = +6.
    identity_delta = 0.0
    for p in (h, a):
        adj = identity_adjusted_c_reb(p)
        if adj is None or p.historical_c_reb is None:
            continue
        identity_delta += adj - p.historical_c_reb

    forecast += 0.20 * identity_delta

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
