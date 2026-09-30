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
