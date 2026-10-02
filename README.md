# euroleague c-reb model

a data-driven research model for euroleague credit-rebound markets.

## settlement definition

**c-reb = player offensive rebounds + player defensive rebounds.**

team rebounds are excluded from the settlement target.

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

## 2025-26 first findings

- 380 regular-season games
- mean c-reb: 62.01
- median: 61
- sd: 7.56
- 70+ c-reb: 55/380 (14.5%)
- 80+ c-reb: 5/380 (1.3%)
- c-reb vs missed fg correlation: 0.907
- missed-fg single-variable ols r²: 0.823

## 2026-27 early data

through round 3, 14 games have been entered into the live tracking sample (round 2: 10 games; round 3: 4 games).

- w2 mean c-reb: 60.8
- w2 under rate vs recorded provider decision lines: 9/10 (90.0%)
- w3 mean c-reb: 77.5
- w3 under rate vs recorded provider decision lines: 2/4 (50.0%)
- combined w2+w3: **11/14 unders (78.6%)**
- this is an observation, not a validated market-edge estimate; the sample is still very small.

w3 also demonstrated why the model cannot simply impose a permanent low-rebound bias. the four w3 games showed elevated rebound realization, with reboppr-t at or above 1.000 in the tracked calculations. high rebound realization materially changed realized totals.

## h2h principle

h2h is not just a generic average. the model explicitly tracks the previous season's first and second regular-season meetings.

when **h2h-1 c-reb and h2h-2 c-reb are close to each other**, that stability is treated as evidence that the matchup may have a repeatable rebound environment. the h2h average can then receive more weight than it would receive when the two meetings are far apart.

when the two h2h results are materially different, the h2h signal is shrunk toward the broader historical/current-season evidence. playoffs are excluded from this anchor.

h2h also tracks the opportunity environment and orb/drb profile where data are available. the goal is to identify matchup-specific structure without hard-coding a direction such as under or over.

## team identity and abbreviations

team identity is allowed to emerge from the data rather than being manually assigned as a bias. current-season c-reb is shrunk toward the historical baseline and the effect is capped/low-weight until validation supports stronger use.

for compact tracking, teams use stable three-letter ids:

| team | id |
|---|---|
| Anadolu Efes | EFE |
| ASVEL | ASV |
| Barcelona | BAR |
| Baskonia | BAS |
| Bayern Munich | BAY |
| Besiktas | BJK |
| Crvena Zvezda | ZVE |
| Dubai Basketball | DUB |
| Fenerbahce | FEN |
| Hapoel Tel Aviv | HAP |
| Maccabi Tel Aviv | MAC |
| Milano | MIL |
| Olympiacos | OLY |
| Panathinaikos | PAN |
| Paris Basketball | PAR |
| Partizan | PTZ |
| Real Madrid | RMA |
| Valencia Basket | VAL |
| Virtus Bologna | VIR |
| Zalgiris Kaunas | ZAL |

these ids are bookkeeping labels only. they do not encode a prior belief about a team's rebound strength.

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

regression fitting must use game-level rows and is intentionally separate from provider lines. the existing 2025-26 single-variable relationship is retained as the historical fallback anchor:

`c-reb = 3.126 + 0.8719 * missed_fg`

no new multivariable coefficient is treated as validated until it is fit on game-level data and checked out of sample.

## forecast vs line

the provider line is a separate market input. it does not determine the model forecast.

we record the line available when the forecast/betting decision is made. historical forecasts are never rewritten after the fact.

the workflow is:

**data -> pregame forecast -> provider line -> gap -> decision/pass -> actual result -> residual analysis -> calibrated next forecast**

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

## code

- `model/creb_model_v0_4.py` — first executable model skeleton
- `model/creb_model_v0_7.py` — forecasting framework, identity signal, h2h stability and regression utility
- `model/creb_model_v0_8.py` — adaptive empirical-Bayes residual calibration

## data source

ivo villanueva / euroleague boxscore player-game data:

https://github.com/IvoVillanueva/EUROLEAGUE-BOXSCORE
