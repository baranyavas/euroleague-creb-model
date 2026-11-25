# Bankroll — 2026-27

Ledger: `data/bets_2026_27.csv` — 58 tickets, 2026-09-28 → 2026-11-24.

Open tickets are excluded from every total below; they are listed at
the end with their stake and what they would return.

| | |
|---|---:|
| tickets | **58** settled |
| won / lost | 36 / 22 |
| staked | **3,020.91** |
| returned | **8,917.94** |
| net | **+5,897.03** |
| ROI | **+195.2%** |
| calendar days (first → last ticket) | 58 |
| betting days | 28 |
| net per calendar day | +101.67 |
| net per betting day | +210.61 |
| net per day since season start (2026-09-24) | +95.11 |

## By site

```
                             n  W/L      staked  returned        net      ROI
Duel                        16   8/8      843.28  2,038.59  +1,195.31  +141.7%
Empire                      42  28/14   2,177.63  6,879.35  +4,701.72  +215.9%
all                         58  36/22   3,020.91  8,917.94  +5,897.03  +195.2%
```

## By ticket type

```
                             n  W/L      staked  returned        net      ROI
single                      13  10/3      826.57  1,138.20    +311.63   +37.7%
2-fold                      21  10/11   1,034.58  1,423.46    +388.88   +37.6%
3-fold                      17  13/4      863.59  4,070.40  +3,206.81  +371.3%
4-fold                       5   3/2      277.13  2,285.88  +2,008.75  +724.8%
5-fold                       2   0/2       19.04      0.00     -19.04  -100.0%
```

## Weeks (W1 starts at the first ticket)

```
week       dates                       n  W/L      staked        net      ROI
W1         2026-09-28 .. 2026-10-04    7   4/3      167.79    +303.33  +180.8%
W2         2026-10-05 .. 2026-10-11    4   3/1      176.50    +251.93  +142.7%
W3         2026-10-12 .. 2026-10-18   10   7/3      562.37  +1,452.86  +258.3%
W4         2026-10-19 .. 2026-10-25    2   0/2      134.29    -134.29  -100.0%
W5         2026-10-26 .. 2026-11-01    6   5/1      346.58    +929.09  +268.1%
W6         2026-11-02 .. 2026-11-08    5   3/2      329.70    +562.36  +170.6%
W7         2026-11-09 .. 2026-11-15    7   5/2      489.21  +1,224.41  +250.3%
W8         2026-11-16 .. 2026-11-22   14   6/8      704.57    +799.71  +113.5%
W9         2026-11-23 .. 2026-11-24    3   3/0      109.90    +507.63  +461.9%
```

## Stake ladder (what the slips actually show)

```
period                      n  median     min     max
2026-09-28 .. 2026-09-30    3    19.9   18.70   19.92
2026-10-01 .. 2026-10-08    7    35.6   10.00   37.19
2026-10-09 .. 2026-11-05   22    65.5    2.78   74.72
2026-11-06 .. 2026-11-20   23    64.4    9.04   77.40
```

## Limit eras

```
era                          dates                       n med stake     max        net      ROI  per day
E1 — 20 $ limiti             2026-09-28 .. 2026-09-30    3      19.9   19.92    +128.23  +219.2%   +42.74
E2 — 35 $ bandı              2026-10-01 .. 2026-10-08    7      35.6   37.19    +495.06  +227.4%   +61.88
E3 — 65 $ bandı              2026-10-09 .. 2026-11-06   24      65.5   74.72  +2,741.99  +190.3%   +94.55
E4 — iki site (65 + 65 $)    2026-11-11 .. 2026-11-24   24      64.4   77.40  +2,531.75  +194.2%  +180.84
```

## Flagged rows

- `2026-10-01` Empire 3-fold — OPEN leg ignored, already lost
- `2026-10-08` Empire 2-fold — stake derived from payout
- `2026-10-13` Empire 2-fold — time cut off
- `2026-10-13` Empire 4-fold — time cut off
- `2026-10-15` Empire 2-fold — stake corrected 82.44 -> 62.44 (era-2 limit)
- `2026-10-16` Empire 3-fold — MIXED: 2 EL c-reb legs + volleyball Zawiercie; stake corrected 85.52 -> 65.52 (era-2 limit)
- `2026-10-16` Empire 4-fold — return computed, card cut
- `2026-10-22` Empire 4-fold — header cut; 1 team-total leg
- `2026-10-28` Empire 2-fold — includes an ASVEL team-total leg
- `2026-11-06` Empire 3-fold — relabelled Duel->Empire; Duel's first ticket is 11 Nov
- `2026-11-20` Empire 3-fold — stake derived from payout
- `2026-11-24` Empire 3-fold — same 3-fold on the other site; Empire capped this ticket at 25, took 24.90; potential 148.22
- `2026-11-24` Duel 3-fold — R14 window A: BAY-MAC U68.5 1.77, VAL-PAN U75.5 1.77, ASV-MIL U65.5 1.90; potential 428.58
- `2026-11-24` Duel 2-fold — same night without ASV-MIL; the 1.90 leg's max-profit allowance was used by the 72 ticket; potential 40.73

## Excluded (screenshots but not c-reb)

- `2026-10-15` Empire single — Real Madrid total points U96.5, 30.00 staked, lost — a points bet that slipped into the slips; kept out of the ledger
