# 2026-27 retrospective backtest

Model: v0.7 base forecast (player-only) + v0.8 residual calibration, fed with
rolling pre-game profiles. Retrospective diagnostic only — the live
decision record stays in `data/decision_registry.md`.

| round | games | MAE | bias | mean forecast | mean actual |
|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 4.97 | -0.05 | 63.8 | 63.8 |
| 10 | 10 | 7.33 | +0.83 | 64.4 | 65.2 |
| 11 | 10 | 5.23 | -2.58 | 64.7 | 62.1 |
| 12 | 10 | 6.63 | +4.70 | 64.3 | 69.0 |
| 13 | 10 | 5.85 | -1.09 | 65.3 | 64.2 |
| 14 | 10 | 4.81 | -1.46 | 65.1 | 63.6 |
| 2 | 10 | 7.99 | -3.08 | 63.7 | 60.6 |
| 3 | 10 | 7.29 | +5.56 | 61.9 | 67.5 |
| 4 | 10 | 5.99 | +1.25 | 64.4 | 65.7 |
| 5 | 10 | 6.38 | -3.06 | 64.8 | 61.7 |
| 6 | 10 | 5.94 | +0.26 | 64.4 | 64.7 |
| 7 | 10 | 6.20 | -0.51 | 64.6 | 64.1 |
| 8 | 10 | 5.69 | -1.38 | 64.7 | 63.3 |
| 9 | 10 | 6.27 | -2.96 | 64.8 | 61.8 |

**All 139 games: MAE 6.19, RMSE 7.69, bias -0.26.**

Bias > 0 means the model was too low.
