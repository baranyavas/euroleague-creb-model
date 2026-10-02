"""
euroleague c-reb model v0.8

v0.8 adds an adaptive calibration layer to v0.7.

The model may move its forecast up or down when the accumulated residuals show
that it is systematically too low or too high. The correction is empirical-
Bayes/shrinkage based: small samples are pulled strongly toward zero correction,
while larger samples are allowed to speak for themselves.

Provider lines are never used to create this calibration correction.
"""

from __future__ import annotations

from typing import Optional, Sequence

import numpy as np

from creb_model_v0_7 import base_forecast


def shrunk_residual_mean(
    residuals: Sequence[float],
    prior_mean: float = 0.0,
    prior_games: float = 20.0,
) -> float:
    """Empirical-Bayes shrinkage of the observed residual mean toward zero."""
    x = np.asarray(list(residuals), dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n == 0:
        return prior_mean
    sample_mean = float(np.mean(x))
    weight = n / (n + prior_games)
    return (1.0 - weight) * prior_mean + weight * sample_mean


def adaptive_forecast(
    raw_forecast: float,
    historical_residuals: Sequence[float],
    max_adjustment: float = 4.0,
    prior_games: float = 20.0,
) -> float:
    """
    Move the raw forecast up/down based on accumulated model residuals.

    residual = actual C-REB - forecast.
    Positive residuals mean the model has been systematically too low, so the
    next forecast is nudged upward. Negative residuals do the opposite.

    The correction is capped to prevent a short hot/cold streak from becoming
    a permanent bias.
    """
    correction = shrunk_residual_mean(
        historical_residuals,
        prior_mean=0.0,
        prior_games=prior_games,
    )
    correction = float(np.clip(correction, -max_adjustment, max_adjustment))
    return raw_forecast + correction


def forecast_with_learning(
    raw_forecast: float,
    prior_residuals: Optional[Sequence[float]] = None,
    max_adjustment: float = 4.0,
    prior_games: float = 20.0,
) -> float:
    """Convenience wrapper for the self-updating forecast layer."""
    return adaptive_forecast(
        raw_forecast,
        [] if prior_residuals is None else prior_residuals,
        max_adjustment=max_adjustment,
        prior_games=prior_games,
    )


if __name__ == "__main__":
    print("euroleague c-reb model v0.8 adaptive calibration loaded")
