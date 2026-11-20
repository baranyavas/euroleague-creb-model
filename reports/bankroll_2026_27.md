# Bankroll — 2026-27

Ledger: `data/bets_2026_27.csv` — 56 tickets, 2026-09-28 → 2026-11-20.

| | |
|---|---:|
| tickets | **56** |
| won / lost | 33 / 23 |
| staked | **2,961.01** |
| returned | **8,300.41** |
| net | **+5,339.40** |
| ROI | **+180.3%** |
| calendar days (first → last ticket) | 54 |
| betting days | 27 |
| net per calendar day | +98.88 |
| net per betting day | +197.76 |
| net per day since season start (2026-09-24) | +92.06 |

## By site

```
                             n  W/L      staked  returned        net      ROI
Duel                        15   7/8      818.28  1,932.48  +1,114.20  +136.2%
Empire                      41  26/15   2,142.73  6,367.93  +4,225.20  +197.2%
all                         56  33/23   2,961.01  8,300.41  +5,339.40  +180.3%
```

## By ticket type

```
                             n  W/L      staked  returned        net      ROI
single                      14  10/4      856.57  1,138.20    +281.63   +32.9%
2-fold                      20   9/11   1,041.58  1,382.73    +341.15   +32.8%
3-fold                      15  11/4      766.69  3,493.60  +2,726.91  +355.7%
4-fold                       5   3/2      277.13  2,285.88  +2,008.75  +724.8%
5-fold                       2   0/2       19.04      0.00     -19.04  -100.0%
```

## Weeks (W1 starts at the first ticket)

```
week       dates                       n  W/L      staked        net      ROI
W1         2026-09-28 .. 2026-10-04    7   4/3      167.79    +303.33  +180.8%
W2         2026-10-05 .. 2026-10-11    4   3/1      176.50    +251.93  +142.7%
W3         2026-10-12 .. 2026-10-18   11   7/4      612.37  +1,402.86  +229.1%
W4         2026-10-19 .. 2026-10-25    2   0/2      134.29    -134.29  -100.0%
W5         2026-10-26 .. 2026-11-01    6   5/1      346.58    +929.09  +268.1%
W6         2026-11-02 .. 2026-11-08    5   3/2      329.70    +562.36  +170.6%
W7         2026-11-09 .. 2026-11-15    7   5/2      489.21  +1,224.41  +250.3%
W8         2026-11-16 .. 2026-11-20   14   6/8      704.57    +799.71  +113.5%
```

## Stake ladder (what the slips actually show)

```
period                      n  median     min     max
2026-09-28 .. 2026-09-30    3    19.9   18.70   19.92
2026-10-01 .. 2026-10-08    7    35.6   10.00   37.19
2026-10-09 .. 2026-11-05   23    65.5    2.78   82.44
2026-11-06 .. 2026-11-20   23    64.4    9.04   77.40
```

## Limit eras

```
era                          dates                       n med stake     max        net      ROI  per day
E1 — 20 $ limiti             2026-09-28 .. 2026-10-08   10      35.6   37.19    +623.29  +225.6%   +56.66
E2 — 65 $ bandı              2026-10-09 .. 2026-11-05   23      65.5   82.44  +2,459.18  +180.7%   +87.83
E3 — Duel eklendi (~140 $)   2026-11-06 .. 2026-11-20   23      64.4   77.40  +2,256.93  +170.4%  +150.46
```

## Flagged rows

- `2026-10-01` Empire 3-fold — OPEN leg ignored, already lost
- `2026-10-08` Empire 2-fold — stake derived from payout
- `2026-10-13` Empire 2-fold — time cut off
- `2026-10-13` Empire 4-fold — time cut off
- `2026-10-15` Empire single — TEAM total (Real Madrid U56.5), not match total
- `2026-10-16` Empire 3-fold — MIXED: 2 EL c-reb legs + volleyball Zawiercie; stake corrected 85.52 -> 65.52 (era-2 limit)
- `2026-10-16` Empire 4-fold — return computed, card cut
- `2026-10-22` Empire 4-fold — header cut; 1 team-total leg
- `2026-10-28` Empire 2-fold — includes an ASVEL team-total leg
- `2026-11-20` Empire 3-fold — stake derived from payout
