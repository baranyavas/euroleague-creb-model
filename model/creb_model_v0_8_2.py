"""
euroleague c-reb model v0.8.2

Research extension to v0.8: current-vs-h2h regime similarity.

The signal measures how similar the current-season matchup environment is to
the previous-season h2h environment. It is deliberately exposed as a
standalone diagnostic / weighting signal first; it does not automatically
change the forecast until the W1-W3 sample is tested out of sample.
"""

from __future__ import annotations

from math import exp
from typing import Mapping, Optional, Sequence


DEFAULT_WEIGHTS = {
    "c_reb": 0.30,
    "missed_fg": 0.25,
    "reboppr_t": 0.15,
    "reboppr_o": 0.10,
    "reboppr_d": 0.10,
    "opportunity": 0.10,
}


def _relative_distance(current: float, h2h: float, scale: float) -> float:
    """Absolute difference normalized by a supplied feature scale."""
    if scale <= 0:
        raise ValueError("scale must be positive")
    return abs(float(current) - float(h2h)) / scale


def current_vs_h2h_similarity(
    current: Mapping[str, float],
    h2h: Mapping[str, float],
    scales: Optional[Mapping[str, float]] = None,
    weights: Optional[Mapping[str, float]] = None,
) -> float:
    """
    Return a 0-1 regime-similarity score.

    1.0 means the current environment is identical to the h2h reference.
    Values closer to 0 indicate a larger regime change.

    Features may include:
      c_reb, missed_fg, reboppr_t, reboppr_o, reboppr_d, opportunity

    Missing features are ignored and the remaining weights are renormalized.
    The score is diagnostic at v0.8.2; no forecast coefficient is hard-coded.
    """
    if scales is None:
        scales = {
            "c_reb": 8.0,
            "missed_fg": 8.0,
            "reboppr_t": 0.08,
            "reboppr_o": 0.08,
            "reboppr_d": 0.08,
            "opportunity": 10.0,
        }
    if weights is None:
        weights = DEFAULT_WEIGHTS

    usable = []
    for feature, weight in weights.items():
        if feature not in current or feature not in h2h or feature not in scales:
            continue
        usable.append(
            (
                float(weight),
                _relative_distance(current[feature], h2h[feature], scales[feature]),
            )
        )

    if not usable:
        return 0.0

    total_weight = sum(weight for weight, _ in usable)
    weighted_distance = sum(weight * distance for weight, distance in usable) / total_weight

    # Smoothly maps normalized distance to [0, 1].
    return float(exp(-weighted_distance))


def h2h_weight_multiplier(similarity: float, minimum: float = 0.50) -> float:
    """
    Convert regime similarity into a conservative h2h-weight multiplier.

    This is intentionally bounded. A changed regime can shrink h2h influence,
    while even a highly similar regime cannot make h2h dominate the model.
    """
    similarity = max(0.0, min(1.0, float(similarity)))
    minimum = max(0.0, min(1.0, float(minimum)))
    return minimum + (1.0 - minimum) * similarity


if __name__ == "__main__":
    print("euroleague c-reb model v0.8.2 h2h-regime similarity loaded")
