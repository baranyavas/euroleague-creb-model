# 4-leg nights — remaining regular season

A 4-fold needs four games inside one 45-minute window (each line opens
60 minutes before its own tip). `legs` is the widest legal window on
that night. Only nights with **4+** can carry a 4-fold; a 3 is a
3-fold night, not four legs squeezed.

```
date           R legs  window
2026-11-24  14    3      19:00Z: MUN-TEL, PAM-PAN, ASV-MIL
2026-11-25  14    3      19:15Z: OLY-HTA, BAS-IST, MAD-ZAL
2026-12-03  15    2      17:30Z: IST-PAM, ULK-RED
2026-12-04  15    2      19:15Z: OLY-ASV, BAS-TEL
2026-12-10  16    3      18:45Z: HTA-ASV, PAM-RED, MIL-MUN
2026-12-11  16    3      19:15Z: PAN-OLY, VIR-TEL, PAR-BAR
2026-12-15  17    6  *** 19:15Z: ULK-HTA, VIR-ASV, PAM-DUB, MAD-MUN, PRS-OLY, TEL-ZAL
2026-12-16  17    2      19:15Z: PAN-RED, BAS-BAR
2026-12-17  18    3      19:00Z: ULK-TEL, ASV-DUB, MAD-PAM
2026-12-18  18    4  *** 19:00Z: MUN-PAN, BAS-PRS, RED-BES, BAR-VIR
2026-12-22  19    4  *** 18:45Z: HTA-PAR, MUN-OLY, ASV-BAR, VIR-MAD
2026-12-23  19    3      19:00Z: RED-BAS, TEL-IST, MIL-PRS
2026-12-29  20    3      19:30Z: BAS-PAM, PAR-ZAL, MAD-DUB
2026-12-30  20    4  *** 19:00Z: MUN-BES, ASV-OLY, VIR-MIL, PRS-RED
2027-01-06  21    1      19:30Z: BAR-BES
2027-01-07  21    3      19:30Z: PAM-PAR, MIL-HTA, MAD-OLY
2027-01-08  21    2      19:00Z: RED-ASV, BAS-VIR
2027-01-12  22    6  *** 19:00Z: ASV-ZAL, RED-MAD, PAN-PAM, VIR-IST, BAR-MIL, TEL-MUN
2027-01-13  22    1      17:00Z: BES-PAR
2027-01-14  23    3      18:45Z: HTA-PAM, PAN-MUN, MIL-ASV
2027-01-15  23    3      19:15Z: OLY-PRS, VIR-BAR, PAR-ULK
2027-01-21  24    5  *** 19:00Z: PAM-ASV, MUN-MIL, MAD-TEL, PAR-OLY, PRS-BAS
2027-01-22  24    2      17:30Z: IST-DUB, ZAL-VIR
2027-01-28  25    4  *** 19:00Z: MUN-PAM, OLY-TEL, VIR-PRS, BAS-ZAL
2027-01-29  25    4  *** 19:00Z: ASV-HTA, PAN-IST, BAR-DUB, MIL-PAR
2027-02-02  26    5  *** 19:05Z: TEL-VIR, PAN-DUB, BAS-ULK, PAR-MAD, PRS-BES
2027-02-03  26    3      18:45Z: HTA-OLY, MUN-RED, BAR-ASV
2027-02-04  27    2      17:30Z: IST-TEL, ZAL-BES
2027-02-05  27    5  *** 19:00Z: ASV-ULK, MIL-PAN, BAS-RED, PAR-HTA, PAM-BAR
2027-02-10  28    2      18:45Z: HTA-BAS, ASV-IST
2027-02-11  28    4  *** 19:00Z: RED-PAR, TEL-BAR, VIR-MUN, PAM-PRS
2027-02-12  28    2      17:45Z: ULK-MIL, ZAL-MAD
2027-03-04  29    5  *** 19:15Z: PAN-BES, VIR-HTA, PAM-ZAL, PRS-TEL, BAS-PAR
2027-03-05  29    4  *** 19:00Z: MUN-ASV, RED-ULK, BAR-MAD, MIL-IST
2027-03-09  30    6  *** 19:00Z: MUN-IST, TEL-RED, VIR-ULK, BAS-PAN, MAD-HTA, PAR-PRS
2027-03-10  30    1      16:00Z: DUB-PAM
2027-03-11  31    5  *** 19:00Z: MUN-HTA, TEL-ASV, MAD-VIR, PRS-PAN, PAR-IST
2027-03-12  31    3      19:00Z: RED-DUB, OLY-BES, BAR-BAS
2027-03-18  32    4  *** 19:05Z: TEL-PAM, PAN-ZAL, MAD-BAS, PAR-MUN
2027-03-19  32    3      19:00Z: ASV-VIR, RED-OLY, BAR-HTA
2027-03-23  33    3      19:00Z: ASV-PAN, PAR-VIR, PRS-MIL
2027-03-24  33    3      19:00Z: MUN-MAD, OLY-BAR, PAM-BES
2027-03-25  34    3      18:45Z: HTA-DUB, ASV-PRS, PAN-PAR
2027-03-26  34    5  *** 19:00Z: MUN-ZAL, RED-PAM, OLY-VIR, MIL-TEL, MAD-BES
2027-03-31  35    2      17:30Z: IST-OLY, ZAL-HTA
2027-04-01  35    4  *** 18:05Z: TEL-ULK, PAM-MAD, MIL-BES, PRS-DUB
2027-04-02  35    3      18:30Z: BAR-PAN, BAS-MUN, PAR-ASV
2027-04-06  36    6  *** 18:30Z: VIR-PAM, BAS-ASV, RED-PAN, MAD-MIL, PRS-IST, BAR-MUN
2027-04-07  36    2      16:00Z: TEL-PAR, DUB-ZAL
2027-04-08  37    6  *** 17:45Z: HTA-RED, MUN-ULK, ASV-MAD, PAN-VIR, PAM-IST, MIL-BAS
2027-04-09  37    2      18:15Z: OLY-ZAL, PAR-DUB
2027-04-15  38    4  *** 17:30Z: IST-HTA, RED-MIL, TEL-BAS, PAN-MAD
2027-04-16  38    2      18:15Z: OLY-PAM, BAR-PAR
```

- upcoming nights: **53**
- 4-leg nights: **21**
- 3-leg nights: **17**
- 2-leg nights: **12**
- 1-leg nights: **3**

## The 4-fold candidates

### 2026-12-15 — round 17

- `19:15Z` ULK vs HTA
- `19:30Z` VIR vs ASV
- `19:30Z` PAM vs DUB
- `19:45Z` MAD vs MUN
- `19:45Z` PRS vs OLY
- `20:00Z` TEL vs ZAL

Window: 19:15Z – 20:00Z (45 min)

### 2026-12-18 — round 18

- `19:00Z` MUN vs PAN
- `19:30Z` BAS vs PRS
- `19:30Z` RED vs BES
- `19:45Z` BAR vs VIR

Window: 19:00Z – 19:45Z (45 min)

### 2026-12-22 — round 19

- `18:45Z` HTA vs PAR
- `19:00Z` MUN vs OLY
- `19:00Z` ASV vs BAR
- `19:30Z` VIR vs MAD

Window: 18:45Z – 19:30Z (45 min)

### 2026-12-30 — round 20

- `19:00Z` MUN vs BES
- `19:00Z` ASV vs OLY
- `19:30Z` VIR vs MIL
- `19:45Z` PRS vs RED

Window: 19:00Z – 19:45Z (45 min)

### 2027-01-12 — round 22

- `19:00Z` ASV vs ZAL
- `19:00Z` RED vs MAD
- `19:15Z` PAN vs PAM
- `19:30Z` VIR vs IST
- `19:30Z` BAR vs MIL
- `19:30Z` TEL vs MUN

Window: 19:00Z – 19:30Z (30 min)

### 2027-01-21 — round 24

- `19:00Z` PAM vs ASV
- `19:00Z` MUN vs MIL
- `19:45Z` MAD vs TEL
- `19:45Z` PAR vs OLY
- `19:45Z` PRS vs BAS

Window: 19:00Z – 19:45Z (45 min)

### 2027-01-28 — round 25

- `19:00Z` MUN vs PAM
- `19:15Z` OLY vs TEL
- `19:30Z` VIR vs PRS
- `19:30Z` BAS vs ZAL

Window: 19:00Z – 19:30Z (30 min)

### 2027-01-29 — round 25

- `19:00Z` ASV vs HTA
- `19:15Z` PAN vs IST
- `19:30Z` BAR vs DUB
- `19:30Z` MIL vs PAR

Window: 19:00Z – 19:30Z (30 min)

### 2027-02-02 — round 26

- `19:05Z` TEL vs VIR
- `19:15Z` PAN vs DUB
- `19:30Z` BAS vs ULK
- `19:45Z` PAR vs MAD
- `19:45Z` PRS vs BES

Window: 19:05Z – 19:45Z (40 min)

### 2027-02-05 — round 27

- `19:00Z` ASV vs ULK
- `19:30Z` MIL vs PAN
- `19:30Z` BAS vs RED
- `19:45Z` PAR vs HTA
- `19:45Z` PAM vs BAR

Window: 19:00Z – 19:45Z (45 min)

### 2027-02-11 — round 28

- `19:00Z` RED vs PAR
- `19:05Z` TEL vs BAR
- `19:30Z` VIR vs MUN
- `19:30Z` PAM vs PRS

Window: 19:00Z – 19:30Z (30 min)

### 2027-03-04 — round 29

- `19:15Z` PAN vs BES
- `19:30Z` VIR vs HTA
- `19:30Z` PAM vs ZAL
- `19:45Z` PRS vs TEL
- `19:45Z` BAS vs PAR

Window: 19:15Z – 19:45Z (30 min)

### 2027-03-05 — round 29

- `19:00Z` MUN vs ASV
- `19:00Z` RED vs ULK
- `19:30Z` BAR vs MAD
- `19:30Z` MIL vs IST

Window: 19:00Z – 19:30Z (30 min)

### 2027-03-09 — round 30

- `19:00Z` MUN vs IST
- `19:05Z` TEL vs RED
- `19:30Z` VIR vs ULK
- `19:30Z` BAS vs PAN
- `19:45Z` MAD vs HTA
- `19:45Z` PAR vs PRS

Window: 19:00Z – 19:45Z (45 min)

### 2027-03-11 — round 31

- `19:00Z` MUN vs HTA
- `19:05Z` TEL vs ASV
- `19:45Z` MAD vs VIR
- `19:45Z` PRS vs PAN
- `19:45Z` PAR vs IST

Window: 19:00Z – 19:45Z (45 min)

### 2027-03-18 — round 32

- `19:05Z` TEL vs PAM
- `19:15Z` PAN vs ZAL
- `19:45Z` MAD vs BAS
- `19:45Z` PAR vs MUN

Window: 19:05Z – 19:45Z (40 min)

### 2027-03-26 — round 34

- `19:00Z` MUN vs ZAL
- `19:00Z` RED vs PAM
- `19:15Z` OLY vs VIR
- `19:30Z` MIL vs TEL
- `19:45Z` MAD vs BES

Window: 19:00Z – 19:45Z (45 min)

### 2027-04-01 — round 35

- `18:05Z` TEL vs ULK
- `18:30Z` PAM vs MAD
- `18:30Z` MIL vs BES
- `18:45Z` PRS vs DUB

Window: 18:05Z – 18:45Z (40 min)

### 2027-04-06 — round 36

- `18:30Z` VIR vs PAM
- `18:30Z` BAS vs ASV
- `18:30Z` RED vs PAN
- `18:45Z` MAD vs MIL
- `18:45Z` PRS vs IST
- `18:45Z` BAR vs MUN

Window: 18:30Z – 18:45Z (15 min)

### 2027-04-08 — round 37

- `17:45Z` HTA vs RED
- `18:00Z` MUN vs ULK
- `18:00Z` ASV vs MAD
- `18:15Z` PAN vs VIR
- `18:30Z` PAM vs IST
- `18:30Z` MIL vs BAS

Window: 17:45Z – 18:30Z (45 min)

### 2027-04-15 — round 38

- `17:30Z` IST vs HTA
- `18:00Z` RED vs MIL
- `18:05Z` TEL vs BAS
- `18:15Z` PAN vs MAD

Window: 17:30Z – 18:15Z (45 min)
