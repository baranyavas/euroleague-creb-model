# Work log

One line per session: what was done, what it produced, why.

- 2026-11-20 — fixed the v0.7 identity adjustment: it summed both teams' current c-reb against only the baselines that existed, so every BJK game (no 2025-26 row) was inflated by 0.20 x ~30 = +6. Now each team is compared against its own baseline and contributes nothing when it has none. Backtest 125 games: MAE 6.79 -> 6.65, bias -0.42 -> +0.06, RMSE 8.19 -> 8.05; BJK games bias -4.92 -> +0.62. PTZ-BJK tonight moves 70.4 -> 64.6.
- 2026-11-20 — logged round 13 (6 games, all lines captured): 5 under / 1 over, day bias −0.20, MAE 6.90. VAL-VIR went 89 c-reb on 93 missed FG — both season highs, 99.2nd percentile, the only 89 in 126 games; realisation 0.957 was ordinary (79th pct), so it was volume, not a team-rebound anomaly. The reference 3-fold (BAY-BAS + MIL-FEN + PAR-HAP) would have won all three legs. Added the stake ledger and settled it. No model change.

- 2026-11-18 — logged round 12 (first recorded round after the gap): 9 forecasts, 6 lines captured, 4 under / 2 over; day bias +3.41, MAE 5.49. Added the overtime flag to the dataset (`ot` from team `TimePlayed`) and an overtime section to the season report: 7/119 games (5.9%), mean c-reb 65.86 vs 63.84 in regulation. Added `src/postgame.py` so a night is reviewed from the recorded forecasts, never a re-run. No model change.
- 2026-11-17 — rebuilt the data pipeline on the EuroLeague game center API; backfilled 83 games (round 1, rounds 5–11) as `nr`; parser reproduces the published 2025-26 baseline; retrospective backtest MAE 6.81, bias −0.08; documented the v0.7 `player_only` correction. Model itself unchanged.
- 2026-11-17 — added the pre-line card and the 45-minute combo rule (`src/slate.py`, `STATE.md`), stake ladder, 2-ticket cap.
- 2026-10-09 — W4 postgame diagnostics and settlement discrepancy note; the model then went offline until 2026-11-17.
