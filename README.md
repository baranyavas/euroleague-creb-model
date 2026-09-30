# EuroLeague C-REB Model

A data-driven research model for EuroLeague credit-rebound markets.

## Settlement definition
**C-REB = player Offensive Rebounds + player Defensive Rebounds.**
Team Rebounds are excluded from the target because the market settles strictly on individual player rebound credits.

## Model structure
1. Team C-REB baseline
2. Opponent C-REB baseline
3. H2H
4. Possessions / Pace
5. FGA
6. Missed FG
7. 3PA / 3P%
8. ORB profile
9. Opponent ORB / DRB profile
10. Team Rebounds (context only)
11. Frontcourt continuity (low weight initially)
12. REBOPPR-T = Total C-REB / total missed FG
13. REBOPPR-O = Team ORB / own missed FG
14. REBOPPR-D = Team DRB / opponent missed FG
15. Rolling C-REB
16. Pace-adjusted residual

## 2025-26 first findings
- 380 regular-season games
- Mean C-REB: 62.01
- Median: 61
- SD: 7.56
- 70+ C-REB: 55/380 (14.5%)
- 80+ C-REB: 5/380 (1.3%)
- C-REB vs Missed FG correlation: 0.907
- Missed-FG single-variable OLS R²: 0.823

## Research principle
The model does not attempt to explain every rebound event. Basketball rebounds contain stochastic variation. The goal is to explain the systematic component and leave the residual as an explicit uncertainty term.

Historical lines, live decision-time lines, model projections and actual C-REB results are tracked separately. The provider line is treated as fixed once opened.

## Data source
IvoVillanueva/EUROLEAGUE-BOXSCORE player-game data:
https://github.com/IvoVillanueva/EUROLEAGUE-BOXSCORE
