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

## 2025-26 first findings

- 380 regular-season games
- mean c-reb: 62.01
- median: 61
- sd: 7.56
- 70+ c-reb: 55/380 (14.5%)
- 80+ c-reb: 5/380 (1.3%)
- c-reb vs missed fg correlation: 0.907
- missed-fg single-variable ols r²: 0.823

## forecasting philosophy

the primary objective is **pregame forecasting**, not postgame storytelling.

c-reb contains genuine stochastic variation. the model is expected to explain the systematic component of the rebound environment, while residual variation remains explicit.

current-season g1/g2 information is added gradually and shrunk toward the historical baseline because two games are a very small sample. the v0.7 identity signal captures a team's current c-reb shift versus its historical baseline, but the effect is deliberately capped and low-weight until out-of-sample validation supports a stronger adjustment.

h2h is a separate anchor from the full-season historical baseline. stable h2h is allowed to contribute modestly; unstable h2h is shrunk more heavily.

the main opportunity rule is:

**high fga OR low fg%.**

the combination of both conditions is treated as an extreme subgroup rather than the normal filter.

reboppr is a normalization index used for forecasting and diagnostics. it is not a literal probability and may exceed 1.

## v0.7 regression layer

`model/creb_model_v0_7.py` adds:

- two-stage opportunity -> rebound-realization structure
- matchup-adjusted reboppr-o / reboppr-d
- shrunk current-season team-identity signal
- stability-weighted h2h
- game-level `statsmodels` OLS fitting utility

regression fitting must use game-level rows and is intentionally separate from provider lines. the existing 2025-26 single-variable relationship is retained as the historical fallback anchor:

`c-reb = 3.126 + 0.8719 * missed_fg`

no new multivariable coefficient is treated as validated until it is fit on game-level data and checked out of sample.

## forecast vs line

the provider line is a separate market input. it does not determine the model forecast.

we record the line available when the forecast/betting decision is made. if the provider changes its line before that decision, the latest available line is the decision line. historical forecasts are never rewritten after the fact.

the workflow is:

**data -> pregame forecast -> provider line -> gap -> decision/pass -> actual result -> residual analysis**

## code

- `model/creb_model_v0_4.py` — first executable model skeleton
- `model/creb_model_v0_7.py` — current experimental forecasting framework and regression utility

## data source

ivo villanueva / euroleague boxscore player-game data:

https://github.com/IvoVillanueva/EUROLEAGUE-BOXSCORE
