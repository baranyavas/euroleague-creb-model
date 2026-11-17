# Work log

One line per session: what was done, what it produced, why.

- 2026-11-17 — rebuilt the data pipeline on the EuroLeague game center API; backfilled 83 games (round 1, rounds 5–11) as `nr`; parser reproduces the published 2025-26 baseline; retrospective backtest MAE 6.81, bias −0.08; documented the v0.7 `player_only` correction. Model itself unchanged.
- 2026-10-09 — W4 postgame diagnostics and settlement discrepancy note; the model then went offline until 2026-11-17.
