# euroleague c-reb model

a data-driven research model for euroleague credit-rebound markets.

## settlement definition

**c-reb = total-row T - team-row T.**

The bottom `total` rebound number in the EuroLeague box score already includes the rebounds shown on the separate `team` row. Therefore, do **not** calculate settled c-reb by adding the bottom total-row O + D.

Equivalent interpretation: c-reb is the player-credited offensive rebounds + player-credited defensive rebounds. Team rebounds are excluded from the settlement target.

The separate team-rebound amount is retained as explanatory/context data and must never be added to c-reb.

This settlement rule was re-checked after the 2026-10-02 games. Example: Besiktas showed 40 total rebounds and 1 team rebound, so its settled c-reb was 39; Barcelona showed 34 total and 5 team, so its settled c-reb was 29.

## model structure

1. team c-reb baseline
2. opponent c-reb baseline
3. h2h
4. possessions / pace
5. fga
6. missed fg
7. 3pa / 3p%
8. orb profile
9. opponent orb / drb profile
10. team rebounds (context only)
11. frontcourt continuity (low weight initially)
12. reboppr-t = total c-reb / total missed fg
13. reboppr-o = team orb / own missed fg
14. reboppr-d = team drb / opponent missed fg
15. rolling c-reb
16. pace-adjusted residual
17. current-season team identity signal (shrunk toward historical baseline)
18. h2h stability / closeness signal
19. adaptive residual calibration
20. current-vs-h2h regime similarity (v0.8.2 research layer)

## 2025-26 first findings

- 380 regular-season games
- mean c-reb: 62.01
- median: 61
- sd: 7.56
- mean missed fg: **67.53**
- 70+ c-reb: 55/380 (14.5%)
- 80+ c-reb: 5/380 (1.3%)
- c-reb vs missed fg correlation: 0.907
- missed-fg single-variable ols r²: 0.823

The historical missed-fg mean is an important baseline because missed shots are the main opportunity-generation mechanism for c-reb.

## 2026-27 early data

through round 3, **20 games** have been entered into the live tracking sample (round 2: 10 games; round 3: 10 games).

- w2 mean c-reb: 60.8
- w2 under rate vs recorded provider decision lines: 9/10 (90.0%)
- w3 day 1: 2/4 under (50.0%)
- w3 day 2: **5/6 under (83.3%)**
- w3 overall: **7/10 under (70.0%)**
- combined w2+w3: **16/20 unders (80.0%)**

This is an observation, not a validated market-edge estimate; the sample is still small.

Round 3 day 2 was especially useful because the model's six pregame forecasts averaged 63.83 c-reb while actuals averaged 65.33, an average residual of only **+1.50**. Provider lines averaged 69.5, versus 65.33 actual c-reb. This means the model was modestly low on average, while the market line sat materially higher than the realized c-reb average.

The day-2 forecasts and outcomes were:

| matchup | model | line | actual c-reb | residual | result |
|---|---:|---:|---:|---:|---|
| besiktas–barcelona | 59 | 66.5 | 68 | +9 | over |
| fenerbahce–dubai | 67 | 69.5 | 64 | -3 | under |
| bayern–partizan | 61 | 66.5 | 63 | +2 | under |
| asvel–valencia | 64 | 71.5 | 69 | +5 | under |
| panathinaikos–maccabi | 67 | 70.5 | 66 | -1 | under |
| baskonia–milano | 65 | 72.5 | 62 | -3 | under |

The practical decision process also showed that the largest model-to-line gaps were the games receiving the most attention, while forecasts remained locked before lines were considered. On this card, the three-leg selection of ASVEL U71.5, Bayern U66.5 and Baskonia U72.5 went 3/3; adding Fenerbahce U69.5 would have made 4/4. Besiktas U66.5 was the only loss among those five selected directions.

## h2h principle

h2h is not just a generic average. the model explicitly tracks the previous season's first and second regular-season meetings.

when **h2h-1 c-reb and h2h-2 c-reb are close to each other**, that stability is treated as evidence that the matchup may have a repeatable rebound environment. the h2h average can then receive more weight than it would receive when the two meetings are far apart.

when the two h2h results are materially different, the h2h signal is shrunk toward the broader historical/current-season evidence. playoffs are excluded from this anchor.

h2h also tracks the opportunity environment and orb/drb profile where data are available. the goal is to identify matchup-specific structure without hard-coding a direction such as under or over.

### new w4 h2h variable: current-vs-h2h similarity

v0.8.2 adds a standalone **current-vs-h2h regime-similarity signal**. The first implementation is deliberately a research/diagnostic layer; it does not automatically change live forecasts until it is tested on the frozen W1-W3 sample and then out of sample.

For each matchup with usable previous-season meetings, compare the current-season matchup environment with the previous-season h2h environment across:

- c-reb
- missed fg
- reboppr-t
- where available, reboppr-o and reboppr-d
- opportunity / shot-volume environment
- orb/drb profile where available

The question is: **does this year's version of the matchup still look statistically like last year's matchup?**

If the current environment is close to the h2h environment, the h2h signal can retain more weight. If it has materially changed, the h2h contribution should be shrunk toward broader historical and current-season evidence.

The implementation lives in `model/creb_model_v0_8_2.py` and returns a 0-1 regime-similarity score plus a conservative h2h-weight multiplier. The feature uses normalized distances and renormalizes weights when some inputs are unavailable.

This is a **time-stability / regime-similarity variable**, not a manual preference for h2h. A Fenerbahce–Dubai-style case should therefore be evaluated by comparing last season's two meetings with the current-season meeting rather than looking only at the old h2h average.

## team rebounds and stochasticity

Team rebounds are excluded from settled c-reb, but they are now explicitly tracked as a context variable.

The 2026-10-02 six-game card had team-rebound totals of:

**6, 6, 3, 8, 9, 3**

Examples:

- beşiktaş: 40 total-row rebounds = **39 c-reb + 1 team rebound**
- barcelona: 34 total-row rebounds = **29 c-reb + 5 team rebounds**
- panathinaikos: 43 total-row rebounds = **37 c-reb + 6 team rebounds**
- maccabi: 41 total-row rebounds = **38 c-reb + 3 team rebounds**

The main hypothesis is that whether a missed shot becomes a player-credited rebound or a team rebound contains a substantial stochastic component from a pregame perspective. A specific loose ball, out-of-bounds deflection, team-control sequence, or other box-score classification cannot generally be predicted for an individual possession.

Therefore:

- team rebounds must not contaminate the c-reb target
- team rebounds should be retained for descriptive diagnostics
- team rebounds should only become a predictive feature if the larger sample demonstrates stable incremental information

## forecasting philosophy

the primary objective is **pregame forecasting**, not postgame storytelling.

c-reb contains genuine stochastic variation. the model is expected to explain the systematic component of the rebound environment, while residual variation remains explicit.

current-season g1/g2/g3 information is added gradually and shrunk toward the historical baseline because two or three games are still a small sample. the identity signal captures a team's current c-reb shift versus its historical baseline, but the effect is deliberately capped and low-weight until out-of-sample validation supports a stronger adjustment.

the main opportunity rule is:

**high fga OR low fg%.**

the combination of both conditions is treated as an extreme subgroup rather than the normal filter.

reboppr is a normalization index used for forecasting and diagnostics. it is not a literal probability and may exceed 1.

## adaptive learning / shrinkage

the model is allowed to learn from its own historical forecast errors without manually imposing an under or over bias.

for each completed game:

`residual = actual c-reb - pregame forecast`

- positive residual -> the model was too low
- negative residual -> the model was too high

v0.8 adds an empirical-Bayes style residual correction. the observed residual mean is shrunk toward zero using a prior sample size, and the correction is capped. therefore a short streak cannot suddenly move every future forecast by a large amount.

this creates the desired behavior: the model can gradually move a forecast upward or downward when the data repeatedly show that it is miscalibrated, while remaining neutral when the evidence is weak.

provider lines are never used to create this correction. market bias and model bias remain separate.

## regression layer

`model/creb_model_v0_7.py` contains the main forecasting framework and game-level `statsmodels` ols utility.

`model/creb_model_v0_8.py` adds the adaptive residual-calibration layer.

`model/creb_model_v0_8_2.py` adds the current-vs-h2h regime-similarity diagnostic layer.

regression fitting must use game-level rows and is intentionally separate from provider lines. the existing 2025-26 single-variable relationship is retained as the historical fallback anchor:

`c-reb = 3.126 + 0.8719 * missed_fg`

no new multivariable coefficient is treated as validated until it is fit on game-level data and checked out of sample.

## forecast vs line

the provider line is a separate market input. it does not determine the model forecast.

we record the line available when the forecast/betting decision is made. historical forecasts are never rewritten after the fact.

the workflow is:

**data -> pregame forecast -> provider line -> gap -> decision/pass -> actual result -> residual analysis -> calibrated next forecast**

The 2026-10-02 card also reinforced an execution rule: provider lines appeared around one hour before tip, and the decision was made at approximately 20:50 after the relevant lines were available. This timing is an execution observation, not a forecasting feature.

The day-2 card also suggested that **model-to-line gap deserves explicit out-of-sample testing**: the model's largest-gap games were the most attractive candidates on the card, but the sample is too small to conclude that gap magnitude itself is predictive.

## decision registry

`data/decision_registry.md` is the chronological experiment ledger. every tracked game should preserve:

- date / round
- three-letter team ids
- pregame model forecast
- provider decision line
- model-to-line gap
- actual c-reb
- actual-minus-model residual
- under / over / push against the decision line
- whether the game was used in a combo
- postgame diagnostic notes

missing pregame forecasts are recorded as `not recorded` rather than reconstructed after the game. this prevents hindsight leakage.

## w4 review plan

No new EuroLeague games are scheduled for the next five days after Round 3. The model is frozen during this gap.

Before the next active round, perform one complete W1-W3 review and test:

1. calibration and residual structure
2. adaptive shrinkage performance
3. h2h stability / closeness
4. reboppr-o vs reboppr-d
5. **current-vs-h2h regime similarity**
6. team-rebound context signal
7. whether model-to-line gaps remain informative out of sample
8. whether line proximity changes the reliability of the betting decision

Only after these tests should v0.9 changes be considered.

## current experiment rules

- settlement target is fixed: player-credited orb + player-credited drb; team rebounds excluded.
- operationally, settled c-reb is `total-row T - team-row T`.
- team rebounds remain a separate explanatory variable.
- no manual under bias is allowed.
- current-season identity adjustments must be shrunk and validated.
- h2h stability is a shrinkage mechanism, not a betting preference.
- current-vs-h2h similarity is evaluated separately from raw h2h closeness.
- provider lines are recorded after forecasts and never fed backward into the forecast.
- use stable three-letter team ids and never reuse an id.
- do not change the model during the frozen W1-W3 evaluation window.
