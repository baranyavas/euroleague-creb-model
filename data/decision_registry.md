# c-reb decision registry

chronological experiment ledger. this file preserves the information available at decision time and does not reconstruct missing forecasts after the game.

## settlement definition

settled c-reb is **total-row T - team-row T**. the bottom total-row O + D must not be used directly because team rebounds are embedded in the total-row defensive-rebound figure.

## summary

| sample | games | under | over | push | under rate |
|---|---:|---:|---:|---:|---:|
| w2 | 10 | 9 | 1 | 0 | 90.0% |
| w3 | 10 | 7 | 3 | 0 | 70.0% |
| w4 through 2026-10-08 | 7 | 6 | 1 | 0 | 85.7% |
| w2+w3+w4 | 27 | **22** | 5 | 0 | **81.5%** |

w3 day 1 was 2/4 under. w3 day 2 was 5/6 under.

## registry columns

- `model forecast`: locked pregame yavasian forecast
- `line`: provider decision line available when the decision was made
- `gap`: model forecast - provider line; negative means the model was below the market
- `actual`: settled c-reb = total-row T - team-row T
- `team rebounds`: team-row T, excluded from settled c-reb
- `result`: under / over / push against the decision line
- `model call`: directional call implied by forecast vs line
- `call correct`: whether the model call matched the settled result
- `notes`: combo usage and postgame diagnostics

`nr` means the numeric pregame forecast was not recorded. it is intentionally not reconstructed from postgame information.

## round 2 — 2026-09-29 / 2026-09-30

| date | round | teams | ids | model forecast | line | gap | actual | team rebounds | result | model call | call correct | notes |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 2026-09-29 | 2 | Efes–Real Madrid | EFE–RMA | nr | 69.5 | nr | 54 | nr | under | nr | nr | played; combo leg |
| 2026-09-29 | 2 | Paris–Partizan | PAR–PTZ | nr | 71.5 | nr | 56 | nr | under | nr | nr | played; combo leg |
| 2026-09-29 | 2 | Valencia–Baskonia | VAL–BAS | nr | 73.5 | nr | 70 | nr | under | nr | nr | played; combo leg |
| 2026-09-29 | 2 | Zvezda–Hapoel | ZVE–HAP | nr | 70.5 | nr | 82 | nr | over | nr | nr | postgame outlier; actual c-reb 82 |
| 2026-09-29 | 2 | Dubai–Barcelona | DUB–BAR | nr | 69.5 | nr | 53 | nr | under | nr | nr | actual c-reb 53 |
| 2026-09-29 | 2 | Fenerbahce–Bayern | FEN–BAY | nr | 69.5 | nr | 57 | nr | under | nr | nr | actual c-reb 57 |
| 2026-09-29 | 2 | Milano–Virtus | MIL–VIR | nr | 73.5 | nr | 71 | nr | under | nr | nr | actual c-reb 71 |
| 2026-09-29 | 2 | Zalgiris–Olympiacos | ZAL–OLY | nr | 73.5 | nr | 57 | nr | under | nr | nr | actual c-reb 57 |
| 2026-09-30 | 3 | Maccabi–Besiktas | MAC–BJK | 66 | 66.5 | -0.5 | 47 | nr | under | under | yes | played; decision line 66.5; later line 65.5 |
| 2026-09-30 | 3 | Panathinaikos–ASVEL | PAN–ASV | 67 | 67.5 | -0.5 | 61 | nr | under | under | yes | played; decision line 67.5; later line 66.5 |

## round 3 — 2026-10-01

pregame forecasts below are the rough locked centers used before the games. they are retained as recorded rather than rewritten after the results.

| date | round | teams | ids | model forecast | line | gap | actual | team rebounds | result | model call | call correct | notes |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 2026-10-01 | 3 | Hapoel–Real Madrid | HAP–RMA | 63.5 | 71.5 | -8.0 | 59 | 9 | under | under | yes | 65 missed fg; Hapoel 26 + Real 33 c-reb; reboppr-t 0.908 |
| 2026-10-01 | 3 | Zvezda–Efes | ZVE–EFE | 65.5 | 71.5 | -6.0 | 84 | 5 | over | under | no | 84 missed fg; Zvezda 41 + Efes 43 c-reb; reboppr-t 1.000 |
| 2026-10-01 | 3 | Virtus–Olympiacos | VIR–OLY | 63.5 | 69.5 | -6.0 | 68 | 7 | under | under | yes | total-row T=75; team-row T=7; settled c-reb=68 |
| 2026-10-01 | 3 | Paris–Zalgiris | PAR–ZAL | 64.5 | 71.5 | -7.0 | 72 | 13 | over | under | no | 77 missed fg; Paris 36 + Zalgiris 36 c-reb; reboppr-t 0.935 |

## round 3 — 2026-10-02

| date | round | teams | ids | model forecast | line | gap | actual | team rebounds | result | model call | call correct | notes |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 2026-10-02 | 3 | Besiktas–Barcelona | BJK–BAR | 59 | 66.5 | -7.5 | 68 | 6 | over | under | no | actual total-row T=74; team-row T=6; settled c-reb=68 |
| 2026-10-02 | 3 | Fenerbahce–Dubai | FEN–DUB | 67 | 69.5 | -2.5 | 64 | 6 | under | under | yes | settled c-reb=64 |
| 2026-10-02 | 3 | Bayern–Partizan | BAY–PTZ | 61 | 66.5 | -5.5 | 63 | 3 | under | under | yes | settled c-reb=63 |
| 2026-10-02 | 3 | ASVEL–Valencia | ASV–VAL | 64 | 71.5 | -7.5 | 69 | 8 | under | under | yes | settled c-reb=69 |
| 2026-10-02 | 3 | Panathinaikos–Maccabi | PAN–MAC | 67 | 70.5 | -3.5 | 66 | 9 | under | under | yes | settled c-reb=66 |
| 2026-10-02 | 3 | Baskonia–Milano | BAS–MIL | 65 | 72.5 | -7.5 | 62 | 3 | under | under | yes | settled c-reb=62 |

## round 3 postgame diagnostic

w3 finished **7/10 under**.

### 2026-10-01

- HAP–RMA: 59 c-reb / 65 missed fg; reboppr-t 0.908
- ZVE–EFE: 84 c-reb / 84 missed fg; reboppr-t 1.000
- VIR–OLY: 68 c-reb / 75 missed fg; total-row T=75; team-row T=7; reboppr-t 0.907
- PAR–ZAL: 72 c-reb / 77 missed fg; reboppr-t 0.935

### 2026-10-02

- BJK–BAR: 68 c-reb; total-row T=74; team-row T=6
- FEN–DUB: 64 c-reb; team-row T=6
- BAY–PTZ: 63 c-reb; team-row T=3
- ASV–VAL: 69 c-reb; team-row T=8
- PAN–MAC: 66 c-reb; team-row T=9
- BAS–MIL: 62 c-reb; team-row T=3

Day 2 model average = 63.83; actual average = 65.33; average residual = +1.50. Provider lines averaged 69.5.

The six day-2 games demonstrate why c-reb must be separated from team rebounds. For example, Besiktas had 40 total-row rebounds but only 1 team rebound, giving 39 c-reb; Barcelona had 34 total-row rebounds and 5 team rebounds, giving 29 c-reb.


## round 4 — 2026-10-07 / 2026-10-08

W4 decision-time forecasts were locked before the provider lines were considered. Settled c-reb is always total-row T minus team-row T.

| date | round | teams | ids | model forecast | line | gap | actual | team rebounds | result | model call | call correct | notes |
|---|---:|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| 2026-10-07 | 4 | Paris–ASVEL | PAR–ASV | 64 | 73.5 | -9.5 | 64 | 8 | under | under | yes | Paris 30 + ASVEL 34 c-reb; box-score total 72 |
| 2026-10-08 | 4 | Dubai–Zvezda | DUB–ZVE | 68 | 71.5 | -3.5 | 70 | 4 | under | under | yes | Dubai 32 + Zvezda 38 c-reb; box-score total 74; displayed provider result was lost because it appears to have settled total rebounds rather than c-reb |
| 2026-10-08 | 4 | Maccabi–Milano | MAC–MIL | 63 | 68.5 | -5.5 | 57 | 6 | under | under | yes | Maccabi 25 + Milano 32 c-reb; box-score total 63 |
| 2026-10-08 | 4 | Bayern–Virtus | BAY–VIR | 63.5 | 69.5 | -6.0 | 66 | 15 | under | under | yes | Bayern 33 + Virtus 33 c-reb; box-score total 81 |
| 2026-10-08 | 4 | Panathinaikos–Fenerbahce | PAN–FEN | 65.5 | 72.5 | -7.0 | 67 | 1 | under | under | yes | Panathinaikos 34 + Fenerbahce 33 c-reb; box-score total 68 |
| 2026-10-08 | 4 | Valencia–Hapoel | VAL–HAP | 66.5 | 74.5 | -8.0 | 73 | 8 | under | under | yes | Valencia 35 + Hapoel 38 c-reb; box-score total 81 |
| 2026-10-08 | 4 | Real Madrid–Partizan | RMA–PTZ | 63 | 68.5 | -5.5 | 72 | 11 | over | under | no | Real 38 + Partizan 34 c-reb; box-score total 83; not used in the combo |

### W4 postgame diagnostic

- Paris–ASVEL: 64 c-reb / 66 missed fg / reboppr-t 0.970
- Dubai–Zvezda: 70 c-reb / 78 missed fg / reboppr-t 0.897
- Maccabi–Milano: 57 c-reb / 60 missed fg / reboppr-t 0.950
- Bayern–Virtus: 66 c-reb / 77 missed fg / reboppr-t 0.857
- Panathinaikos–Fenerbahce: 67 c-reb / 67 missed fg / reboppr-t 1.000
- Valencia–Hapoel: 73 c-reb / 75 missed fg / reboppr-t 0.973
- Real Madrid–Partizan: 72 c-reb / 78 missed fg / reboppr-t 0.923

W4 overall: **6/7 under (85.7%)** against the recorded decision lines. The five selected W4 under bets all settled under on the c-reb target; Paris–ASVEL was also an under, while Real–Partizan was the only over and was not used.

Across W2-W4: **22/27 under (81.5%)**.

The six 2026-10-08 games averaged **64.92 model forecast vs 67.50 actual c-reb**, an average residual of **+2.58**. Provider lines averaged **70.83**, so the market sat about **3.33 rebounds above actual c-reb on average** for the six-game card.

The Real–Partizan miss is diagnostically important. The pregame model ranked it last at about 63 because current c-reb was only 59.3 and the estimated missed-fg opportunity was relatively low (~64). The game actually produced **78 missed fg** and 72 c-reb. Its reboppr-t was 0.923, close to the historical league center, so the main failure was the **opportunity stage (missed-fg volume), not an abnormal rebound-realization rate**. This supports keeping the two-stage structure but flags FGA/FG% forecasting as an area for the W4 review.

For the five selected 2026-10-08 unders, the c-reb outcomes were 70, 57, 66, 67, 73. Their provider lines averaged 71.3.

The first W4 two-leg ticket was displayed as lost by the provider, but the settled c-reb calculations are Dubai–Zvezda 70 (under 71.5) and Maccabi–Milano 57 (under 68.5). The research ledger therefore records both as wins on the c-reb target; the provider settlement should be treated as a settlement-definition discrepancy, not a model loss.

## h2h tracking rule

for every matchup with previous-season regular-season meetings, record:

1. h2h-1 c-reb
2. h2h-2 c-reb
3. h2h average
4. h2h gap = h2h-2 - h2h-1
5. a continuous closeness/stability measure
6. h2h opportunity environment where available
7. h2h orb/drb profile where available
8. current-vs-h2h regime similarity for w4 review

when h2h-1 and h2h-2 are close, the matchup-specific signal is allowed to retain more weight. when they are far apart, the signal is shrunk toward the broader historical/current-season evidence.

The new W4 variable asks whether the current-season version of the matchup still resembles last season's h2h environment across c-reb, missed fg, reboppr, opportunity and orb/drb profile. This is a time-stability test, not a manual h2h preference.

## current experiment rules

1. never rewrite a pregame forecast after the game.
2. never use the provider line to generate the model forecast.
3. record the decision-time line separately from later line movement.
4. calculate settled c-reb as total-row T minus team-row T.
5. team rebounds are explanatory/context data only; they are excluded from settled c-reb.
6. current-season team identity can create a data-driven adjustment, but the model does not receive a manually imposed team bias.
7. use stable three-letter ids for teams and never reuse an id.
8. keep missing data as `nr` instead of filling it with hindsight.
9. after the W1-W3 frozen sample, evaluate calibration, residuals, h2h similarity, reboppr-o/d, team-rebound context and line gaps before changing weights.
10. no model-feature or weight changes are made during the five-day post-Round-3 freeze.


## round 4 betting-selection diagnostic — 2026-10-08

The six Round-4 games on 2026-10-08 produced **5 selected unders and all 5 settled under on the c-reb target**. Real Madrid–Partizan was intentionally not selected; it was the only over of the six-game card.

Selected:
- Dubai–Zvezda U71.5: actual **70 c-reb** — under
- Maccabi–Milano U68.5: actual **57 c-reb** — under
- Bayern–Virtus U69.5: actual **66 c-reb** — under
- Panathinaikos–Fenerbahce U72.5: actual **67 c-reb** — under
- Valencia–Hapoel U74.5: actual **73 c-reb** — under

Paris–ASVEL on 2026-10-07 was also an under: **64 c-reb vs 73.5 line**, with the model forecast exactly **64**.

Real–Partizan was forecast at **63 c-reb vs 68.5 line**, but settled at **72 c-reb**. The miss is diagnostically useful rather than evidence of a rebound-realization failure: actual missed-fg opportunity was **78**, versus the pregame estimate of roughly **64**. Actual shooting was worse than the pregame opportunity estimate for both teams, creating substantially more missed shots. Final REBOPPR-T was **0.923**, close to the league center, so the main miss was in the **opportunity stage**, not an abnormal conversion/realization stage.

Round-4 REBOPPR-T values:
- Paris–ASVEL: **0.970**
- Dubai–Zvezda: **0.897**
- Maccabi–Milano: **0.950**
- Bayern–Virtus: **0.857**
- Panathinaikos–Fenerbahce: **1.000**
- Valencia–Hapoel: **0.973**
- Real–Partizan: **0.923**

For the six 2026-10-08 games, model average was **64.92 c-reb**, actual average **67.50**, average residual **+2.58**. Provider lines averaged **70.83**, so actual c-reb remained **3.33 below the average decision line**. The selected five unders averaged a **71.3** line and all five won on the c-reb target.

The first Dubai–Zvezda + Maccabi–Milano two-leg ticket was displayed by the provider as lost, but both legs settled under on the research target: **70 < 71.5** and **57 < 68.5**. This is recorded as a **settlement-definition discrepancy** and should not be counted as a model loss.

**Critical settlement rule remains unchanged:** settled c-reb = bottom Total-row T minus Team-row T. Team-row rebounds are never included in c-reb.
