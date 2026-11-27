# Bankroll — 2026-27

Ledger: `data/bets_2026_27.csv` — 61 tickets, 2026-09-28 → 2026-11-25.

Open tickets are excluded from every total below; they are listed at
the end with their stake and what they would return.

| | |
|---|---:|
| tickets | **61** settled |
| won / lost | 36 / 25 |
| staked | **3,207.91** |
| returned | **8,917.94** |
| net | **+5,710.03** |
| ROI | **+178.0%** |
| calendar days (first → last ticket) | 59 |
| betting days | 29 |
| net per calendar day | +96.78 |
| net per betting day | +196.90 |
| net per day since season start (2026-09-24) | +90.64 |

## By site

```
                             n  W/L      staked  returned        net      ROI
?                            1   0/1       90.00      0.00     -90.00  -100.0%
Duel                        17   8/9      908.28  2,038.59  +1,130.31  +124.4%
Empire                      43  28/15   2,209.63  6,879.35  +4,669.72  +211.3%
all                         61  36/25   3,207.91  8,917.94  +5,710.03  +178.0%
```

## By ticket type

```
                             n  W/L      staked  returned        net      ROI
single                      14  10/4      916.57  1,138.20    +221.63   +24.2%
2-fold                      23  10/13   1,131.58  1,423.46    +291.88   +25.8%
3-fold                      17  13/4      863.59  4,070.40  +3,206.81  +371.3%
4-fold                       5   3/2      277.13  2,285.88  +2,008.75  +724.8%
5-fold                       2   0/2       19.04      0.00     -19.04  -100.0%
```

## Weeks (W1 starts at the first ticket)

```
week       dates                       n  W/L      staked        net      ROI    cum net
W1         2026-09-28 .. 2026-10-04    7   4/3      167.79    +303.33  +180.8%    +303.33
W2         2026-10-05 .. 2026-10-11    4   3/1      176.50    +251.93  +142.7%    +555.26
W3         2026-10-12 .. 2026-10-18   10   7/3      562.37  +1,452.86  +258.3%  +2,008.12
W4         2026-10-19 .. 2026-10-25    2   0/2      134.29    -134.29  -100.0%  +1,873.83
W5         2026-10-26 .. 2026-11-01    6   5/1      346.58    +929.09  +268.1%  +2,802.92
W6         2026-11-02 .. 2026-11-08    5   3/2      329.70    +562.36  +170.6%  +3,365.28
W7         2026-11-09 .. 2026-11-15    7   5/2      489.21  +1,224.41  +250.3%  +4,589.69
W8         2026-11-16 .. 2026-11-22   14   6/8      704.57    +799.71  +113.5%  +5,389.40
W9         2026-11-23 .. 2026-11-25    6   3/3      296.90    +320.63  +108.0%  +5,710.03
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
E4 — iki site (65 + 65 $)    2026-11-11 .. 2026-11-25   27      64.4   90.00  +2,344.75  +157.3%  +156.32
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
- `2026-11-25` ? single — DUB-PRT under 70.5; actual 71 (nine rebounds in the last two minutes); site and price not stated
- `2026-11-25` Duel 2-fold — OLY-HAP U70.5 1.80 + BAS-EFE U70.5 1.90; OLY-HAP landed 56 (under by 14.5), BAS-EFE 72 (over by 1.5)
- `2026-11-25` Empire 2-fold — same 2-fold on the other site; split confirmed by user: 65 Duel + 32 Empire = 97

## Excluded (screenshots but not c-reb)

- `2026-10-15` Empire single — Real Madrid total points U96.5, 30.00 staked, lost — a points bet that slipped into the slips; kept out of the ledger
