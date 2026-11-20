# 2026-27 retrospective backtest

Model: v0.7 base forecast (player-only) + v0.8 residual calibration, fed with
rolling pre-game profiles. Retrospective diagnostic only — the live
decision record stays in `data/decision_registry.md`.

| round | games | MAE | bias | mean forecast | mean actual |
|---:|---:|---:|---:|---:|---:|
| 1 | 9 | 6.05 | +2.04 | 61.7 | 63.8 |
| 10 | 10 | 7.27 | +0.80 | 64.4 | 65.2 |
| 11 | 10 | 5.72 | -2.61 | 64.7 | 62.1 |
| 12 | 10 | 6.59 | +4.71 | 64.3 | 69.0 |
| 13 | 6 | 6.92 | -0.20 | 66.7 | 66.5 |
| 2 | 10 | 7.38 | -3.36 | 64.0 | 60.6 |
| 3 | 10 | 8.43 | +5.90 | 61.6 | 67.5 |
| 4 | 10 | 6.76 | +1.33 | 64.4 | 65.7 |
| 5 | 10 | 6.41 | -3.08 | 64.8 | 61.7 |
| 6 | 10 | 6.31 | +0.20 | 64.5 | 64.7 |
| 7 | 10 | 6.68 | -0.48 | 64.6 | 64.1 |
| 8 | 10 | 5.48 | -1.39 | 64.7 | 63.3 |
| 9 | 10 | 6.48 | -2.94 | 64.7 | 61.8 |

**All 125 games: MAE 6.65, RMSE 8.05, bias +0.06.**

Bias > 0 means the model was too low.
