# 2026-27 retrospective backtest

Model: v0.7 base forecast (player-only) + v0.8 residual calibration, fed with
rolling pre-game profiles. Retrospective diagnostic only — the live
decision record stays in `data/decision_registry.md`.

| round | games | MAE | bias | mean forecast | mean actual |
|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 6.05 | +2.04 | 61.7 | 63.8 |
| 10 | 10 | 6.73 | +0.25 | 64.9 | 65.2 |
| 11 | 10 | 5.17 | -3.17 | 65.3 | 62.1 |
| 2 | 10 | 7.86 | -3.84 | 64.4 | 60.6 |
| 3 | 10 | 7.95 | +5.42 | 62.1 | 67.5 |
| 4 | 10 | 7.34 | +0.75 | 64.9 | 65.7 |
| 5 | 10 | 7.01 | -3.68 | 65.4 | 61.7 |
| 6 | 10 | 6.90 | -0.40 | 65.1 | 64.7 |
| 7 | 10 | 7.25 | -1.05 | 65.1 | 64.1 |
| 8 | 10 | 6.04 | -1.95 | 65.2 | 63.3 |
| 9 | 10 | 7.03 | -3.49 | 65.3 | 61.8 |

**All 109 games: MAE 6.86, RMSE 8.26, bias -0.85.**

Bias > 0 means the model was too low.
