# Model v0.4 notes

## Philosophy
C-REB is an irregular count process. Not every missed field goal becomes a player rebound: the ball may go out, be recovered by a player, fall into an empty area and become a team rebound, or produce other official scoring outcomes.

Therefore the model is intentionally not expected to explain 100% of variance.

## Opportunity layer
Pace -> FGA / FG% -> Missed FG -> rebound opportunity.

Missed FG is currently the strongest single game-level explanatory variable in the historical sample.

## Rebound realization
Expected C-REB is adjusted using rebound profiles and REBOPPR.

REBOPPR is a normalization metric, not a probability:
- REBOPPR-T = total player C-REB / total missed FG
- REBOPPR-O = team ORB / own missed FG
- REBOPPR-D = team DRB / opponent missed FG

## Provider line
The provider line is recorded at decision time and is not overwritten by later model updates. Opening/decision-time/closing lines may be stored separately if available.

## Manual intervention
Manual adjustments are allowed only as documented context, e.g. roster changes, new teams, unusual frontcourt situations, or clearly identified data-quality issues. The original model projection must remain preserved.

## Current 2026-27 workflow
G1/G2 are added as new-season evidence. Historical 2025-26 data remains the base until the rolling/current-season weighting is explicitly changed.

## 2026-11-17 — revival note (v0.7 player-only mode)

Not a new model. One correction, documented here so the record is complete:

- The EuroLeague totals row includes the team-rebound bucket inside O+D. The box
  score also carries a `Team` pseudo-player row that holds it.
- `matchup_reboppr_o/d` blended the own rate with the opponent's complement,
  which forces ORB + DRB = 1.0 and turns the two-stage forecast into
  "total missed FG". That is the total-rebound world, not the c-reb world.
- `base_forecast(..., player_only=True)` keeps the settled player-only rates.
  Pricing uses this mode. The default is unchanged for backward compatibility.
- Effect, 109 games of 2026-27, rolling pre-game profiles:
  default blend MAE 8.45 / bias -6.20; player-only MAE 6.81 / bias -0.08.
- No weights were changed. v0.8 shrinkage, v0.8.2 similarity and the settlement
  rule are untouched.

Provider lines still never enter the forecast.
