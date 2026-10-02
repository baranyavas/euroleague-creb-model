# c-reb decision registry

chronological experiment ledger. this file preserves the information available at decision time and does not reconstruct missing forecasts after the game.

## summary

| sample | games | under | over | push | under rate |
|---|---:|---:|---:|---:|---:|
| w2 | 10 | 9 | 1 | 0 | 90.0% |
| w3 | 4 | 1 | 3 | 0 | 25.0% |
| w2+w3 | 14 | 10 | 4 | 0 | 71.4% |

**important:** the 14-game sample is 10 unders, not 11. w2 was 9/10 and w3 was 1/4.

## registry columns

- `model forecast`: locked pregame yavasian forecast
- `line`: provider decision line available when the decision was made
- `gap`: model forecast - provider line; negative means the model was below the market
- `actual`: settled c-reb = player-credited orb + player-credited drb
- `result`: under / over / push against the decision line
- `model call`: directional call implied by forecast vs line
- `call correct`: whether the model call matched the settled result
- `notes`: combo usage and postgame diagnostics

`nr` means the numeric pregame forecast was not recorded. it is intentionally not reconstructed from postgame information.

## round 2 — 2026-09-29

| date | round | teams | ids | model forecast | line | gap | actual | result | model call | call correct | notes |
|---|---:|---|---|---:|---:|---:|---:|---|---|---|---|
| 2026-09-29 | 2 | Efes–Real Madrid | EFE–RMA | nr | 69.5 | nr | 54 | under | nr | nr | played; combo leg |
| 2026-09-29 | 2 | Paris–Partizan | PAR–PTZ | nr | 71.5 | nr | 56 | under | nr | nr | played; combo leg |
| 2026-09-29 | 2 | Valencia–Baskonia | VAL–BAS | nr | 73.5 | nr | 70 | under | nr | nr | played; combo leg |
| 2026-09-29 | 2 | Zvezda–Hapoel | ZVE–HAP | nr | 70.5 | nr | 82 | over | nr | nr | postgame outlier; actual c-reb 82 |
| 2026-09-29 | 2 | Dubai–Barcelona | DUB–BAR | nr | 69.5 | nr | 53 | under | nr | nr | actual c-reb 53 |
| 2026-09-29 | 2 | Fenerbahce–Bayern | FEN–BAY | nr | 69.5 | nr | 57 | under | nr | nr | actual c-reb 57 |
| 2026-09-29 | 2 | Milano–Virtus | MIL–VIR | nr | 73.5 | nr | 71 | under | nr | nr | actual c-reb 71 |
| 2026-09-29 | 2 | Zalgiris–Olympiacos | ZAL–OLY | nr | 73.5 | nr | 57 | under | nr | nr | actual c-reb 57 |
| 2026-09-30 | 3 | Maccabi–Besiktas | MAC–BJK | 66 | 66.5 | -0.5 | 47 | under | under | yes | played; decision line 66.5; later line 65.5 |
| 2026-09-30 | 3 | Panathinaikos–ASVEL | PAN–ASV | 67 | 67.5 | -0.5 | 61 | under | under | yes | played; decision line 67.5; later line 66.5 |

## round 3 — 2026-10-01

pregame forecasts below are the rough locked centers used before the games. they are retained as recorded rather than rewritten after the results.

| date | round | teams | ids | model forecast | line | gap | actual | result | model call | call correct | notes |
|---|---:|---|---|---:|---:|---:|---:|---|---|---|---|
| 2026-10-01 | 3 | Hapoel–Real Madrid | HAP–RMA | 63.5 | 71.5 | -8.0 | 68 | under | under | yes | actual: 68 c-reb; 65 missed fg; reboppr-t 1.046 |
| 2026-10-01 | 3 | Zvezda–Efes | ZVE–EFE | 65.5 | 71.5 | -6.0 | 89 | over | under | no | actual: 89 c-reb; 84 missed fg; reboppr-t 1.060 |
| 2026-10-01 | 3 | Virtus–Olympiacos | VIR–OLY | 63.5 | 69.5 | -6.0 | 75 | over | under | no | actual: 75 c-reb; 75 missed fg; reboppr-t 1.000 |
| 2026-10-01 | 3 | Paris–Zalgiris | PAR–ZAL | 64.5 | 71.5 | -7.0 | 85 | over | under | no | actual: 85 c-reb; 77 missed fg; reboppr-t 1.104 |

## w3 postgame diagnostic

all four w3 games finished with reboppr-t >= 1.000:

- HAP–RMA: 68 / 65 = 1.046
- ZVE–EFE: 89 / 84 = 1.060
- VIR–OLY: 75 / 75 = 1.000
- PAR–ZAL: 85 / 77 = 1.104

this is a useful warning against manually forcing a low-rebound bias. the model should remain direction-neutral and let opportunity, rebound realization, team identity and matchup relationships generate any persistent effect.

## h2h tracking rule

for every matchup with previous-season regular-season meetings, record:

1. h2h-1 c-reb
2. h2h-2 c-reb
3. h2h average
4. h2h gap = h2h-2 - h2h-1
5. a continuous closeness/stability measure
6. h2h opportunity environment where available
7. h2h orb/drb profile where available

when h2h-1 and h2h-2 are close, the matchup-specific signal is allowed to retain more weight. when they are far apart, the signal is shrunk toward the broader historical/current-season evidence. this is a structural rule, not an under bias.

## current experiment rules

1. never rewrite a pregame forecast after the game.
2. never use the provider line to generate the model forecast.
3. record the decision-time line separately from later line movement.
4. team rebounds are explanatory/context data only; they are excluded from settled c-reb.
5. current-season team identity can create a data-driven adjustment, but the model does not receive a manually imposed team bias.
6. use stable three-letter ids for teams and never reuse an id.
7. keep missing data as `nr` instead of filling it with hindsight.
8. after a meaningful sample accumulates, evaluate calibration, residuals, line gaps, and out-of-sample hit rates before changing weights.
