# 4-leg nights — remaining regular season

A 4-fold needs four games inside one 45-minute window (each line opens
60 minutes before its own tip). `legs` is the widest legal window on
that night. Only nights with **4+** can carry a 4-fold; a 3 is a
3-fold night, not four legs squeezed.

```
date           R legs  window
2026-11-24  14    3      19:00Z: BAY-MAC, VAL-PAN, ASV-MIL
2026-11-25  14    3      19:15Z: OLY-HAP, BAS-EFE, RMA-ZAL
2026-12-03  15    2      17:30Z: EFE-VAL, FEN-CZV
2026-12-04  15    2      19:15Z: OLY-ASV, BAS-MAC
2026-12-10  16    3      18:45Z: HAP-ASV, VAL-CZV, MIL-BAY
2026-12-11  16    3      19:15Z: PAN-OLY, VIR-MAC, PRT-BAR
2026-12-15  17    6  *** 19:15Z: FEN-HAP, VIR-ASV, VAL-DUB, RMA-BAY, PRS-OLY, MAC-ZAL
2026-12-16  17    2      19:15Z: PAN-CZV, BAS-BAR
2026-12-17  18    3      19:00Z: FEN-MAC, ASV-DUB, RMA-VAL
2026-12-18  18    4  *** 19:00Z: BAY-PAN, BAS-PRS, CZV-BJK, BAR-VIR
2026-12-22  19    4  *** 18:45Z: HAP-PRT, BAY-OLY, ASV-BAR, VIR-RMA
2026-12-23  19    3      19:00Z: CZV-BAS, MAC-EFE, MIL-PRS
2026-12-29  20    3      19:30Z: BAS-VAL, PRT-ZAL, RMA-DUB
2026-12-30  20    4  *** 19:00Z: BAY-BJK, ASV-OLY, VIR-MIL, PRS-CZV
2027-01-06  21    1      19:30Z: BAR-BJK
2027-01-07  21    3      19:30Z: VAL-PRT, MIL-HAP, RMA-OLY
2027-01-08  21    2      19:00Z: CZV-ASV, BAS-VIR
2027-01-12  22    6  *** 19:00Z: ASV-ZAL, CZV-RMA, PAN-VAL, VIR-EFE, BAR-MIL, MAC-BAY
2027-01-13  22    1      17:00Z: BJK-PRT
2027-01-14  23    3      18:45Z: HAP-VAL, PAN-BAY, MIL-ASV
2027-01-15  23    3      19:15Z: OLY-PRS, VIR-BAR, PRT-FEN
2027-01-21  24    5  *** 19:00Z: VAL-ASV, BAY-MIL, RMA-MAC, PRT-OLY, PRS-BAS
2027-01-22  24    2      17:30Z: EFE-DUB, ZAL-VIR
2027-01-28  25    4  *** 19:00Z: BAY-VAL, OLY-MAC, VIR-PRS, BAS-ZAL
2027-01-29  25    4  *** 19:00Z: ASV-HAP, PAN-EFE, BAR-DUB, MIL-PRT
2027-02-02  26    5  *** 19:05Z: MAC-VIR, PAN-DUB, BAS-FEN, PRT-RMA, PRS-BJK
2027-02-03  26    3      18:45Z: HAP-OLY, BAY-CZV, BAR-ASV
2027-02-04  27    2      17:30Z: EFE-MAC, ZAL-BJK
2027-02-05  27    5  *** 19:00Z: ASV-FEN, MIL-PAN, BAS-CZV, PRT-HAP, VAL-BAR
2027-02-10  28    2      18:45Z: HAP-BAS, ASV-EFE
2027-02-11  28    4  *** 19:00Z: CZV-PRT, MAC-BAR, VIR-BAY, VAL-PRS
2027-02-12  28    2      17:45Z: FEN-MIL, ZAL-RMA
2027-03-04  29    5  *** 19:15Z: PAN-BJK, VIR-HAP, VAL-ZAL, PRS-MAC, BAS-PRT
2027-03-05  29    4  *** 19:00Z: BAY-ASV, CZV-FEN, BAR-RMA, MIL-EFE
2027-03-09  30    6  *** 19:00Z: BAY-EFE, MAC-CZV, VIR-FEN, BAS-PAN, RMA-HAP, PRT-PRS
2027-03-10  30    1      16:00Z: DUB-VAL
2027-03-11  31    5  *** 19:00Z: BAY-HAP, MAC-ASV, RMA-VIR, PRS-PAN, PRT-EFE
2027-03-12  31    3      19:00Z: CZV-DUB, OLY-BJK, BAR-BAS
2027-03-18  32    4  *** 19:05Z: MAC-VAL, PAN-ZAL, RMA-BAS, PRT-BAY
2027-03-19  32    3      19:00Z: ASV-VIR, CZV-OLY, BAR-HAP
2027-03-23  33    3      19:00Z: ASV-PAN, PRT-VIR, PRS-MIL
2027-03-24  33    3      19:00Z: BAY-RMA, OLY-BAR, VAL-BJK
2027-03-25  34    3      18:45Z: HAP-DUB, ASV-PRS, PAN-PRT
2027-03-26  34    5  *** 19:00Z: BAY-ZAL, CZV-VAL, OLY-VIR, MIL-MAC, RMA-BJK
2027-03-31  35    2      17:30Z: EFE-OLY, ZAL-HAP
2027-04-01  35    4  *** 18:05Z: MAC-FEN, VAL-RMA, MIL-BJK, PRS-DUB
2027-04-02  35    3      18:30Z: BAR-PAN, BAS-BAY, PRT-ASV
2027-04-06  36    6  *** 18:30Z: VIR-VAL, BAS-ASV, CZV-PAN, RMA-MIL, PRS-EFE, BAR-BAY
2027-04-07  36    2      16:00Z: MAC-PRT, DUB-ZAL
2027-04-08  37    6  *** 17:45Z: HAP-CZV, BAY-FEN, ASV-RMA, PAN-VIR, VAL-EFE, MIL-BAS
2027-04-09  37    2      18:15Z: OLY-ZAL, PRT-DUB
2027-04-15  38    4  *** 17:30Z: EFE-HAP, CZV-MIL, MAC-BAS, PAN-RMA
2027-04-16  38    2      18:15Z: OLY-VAL, BAR-PRT
```

- upcoming nights: **53**
- 4-leg nights: **21**
- 3-leg nights: **17**
- 2-leg nights: **12**
- 1-leg nights: **3**

## The 4-fold candidates

### 2026-12-15 — round 17

- `19:15Z` FEN vs HAP
- `19:30Z` VIR vs ASV
- `19:30Z` VAL vs DUB
- `19:45Z` RMA vs BAY
- `19:45Z` PRS vs OLY
- `20:00Z` MAC vs ZAL

Window: 19:15Z – 20:00Z (45 min)

### 2026-12-18 — round 18

- `19:00Z` BAY vs PAN
- `19:30Z` BAS vs PRS
- `19:30Z` CZV vs BJK
- `19:45Z` BAR vs VIR

Window: 19:00Z – 19:45Z (45 min)

### 2026-12-22 — round 19

- `18:45Z` HAP vs PRT
- `19:00Z` BAY vs OLY
- `19:00Z` ASV vs BAR
- `19:30Z` VIR vs RMA

Window: 18:45Z – 19:30Z (45 min)

### 2026-12-30 — round 20

- `19:00Z` BAY vs BJK
- `19:00Z` ASV vs OLY
- `19:30Z` VIR vs MIL
- `19:45Z` PRS vs CZV

Window: 19:00Z – 19:45Z (45 min)

### 2027-01-12 — round 22

- `19:00Z` ASV vs ZAL
- `19:00Z` CZV vs RMA
- `19:15Z` PAN vs VAL
- `19:30Z` VIR vs EFE
- `19:30Z` BAR vs MIL
- `19:30Z` MAC vs BAY

Window: 19:00Z – 19:30Z (30 min)

### 2027-01-21 — round 24

- `19:00Z` VAL vs ASV
- `19:00Z` BAY vs MIL
- `19:45Z` RMA vs MAC
- `19:45Z` PRT vs OLY
- `19:45Z` PRS vs BAS

Window: 19:00Z – 19:45Z (45 min)

### 2027-01-28 — round 25

- `19:00Z` BAY vs VAL
- `19:15Z` OLY vs MAC
- `19:30Z` VIR vs PRS
- `19:30Z` BAS vs ZAL

Window: 19:00Z – 19:30Z (30 min)

### 2027-01-29 — round 25

- `19:00Z` ASV vs HAP
- `19:15Z` PAN vs EFE
- `19:30Z` BAR vs DUB
- `19:30Z` MIL vs PRT

Window: 19:00Z – 19:30Z (30 min)

### 2027-02-02 — round 26

- `19:05Z` MAC vs VIR
- `19:15Z` PAN vs DUB
- `19:30Z` BAS vs FEN
- `19:45Z` PRT vs RMA
- `19:45Z` PRS vs BJK

Window: 19:05Z – 19:45Z (40 min)

### 2027-02-05 — round 27

- `19:00Z` ASV vs FEN
- `19:30Z` MIL vs PAN
- `19:30Z` BAS vs CZV
- `19:45Z` PRT vs HAP
- `19:45Z` VAL vs BAR

Window: 19:00Z – 19:45Z (45 min)

### 2027-02-11 — round 28

- `19:00Z` CZV vs PRT
- `19:05Z` MAC vs BAR
- `19:30Z` VIR vs BAY
- `19:30Z` VAL vs PRS

Window: 19:00Z – 19:30Z (30 min)

### 2027-03-04 — round 29

- `19:15Z` PAN vs BJK
- `19:30Z` VIR vs HAP
- `19:30Z` VAL vs ZAL
- `19:45Z` PRS vs MAC
- `19:45Z` BAS vs PRT

Window: 19:15Z – 19:45Z (30 min)

### 2027-03-05 — round 29

- `19:00Z` BAY vs ASV
- `19:00Z` CZV vs FEN
- `19:30Z` BAR vs RMA
- `19:30Z` MIL vs EFE

Window: 19:00Z – 19:30Z (30 min)

### 2027-03-09 — round 30

- `19:00Z` BAY vs EFE
- `19:05Z` MAC vs CZV
- `19:30Z` VIR vs FEN
- `19:30Z` BAS vs PAN
- `19:45Z` RMA vs HAP
- `19:45Z` PRT vs PRS

Window: 19:00Z – 19:45Z (45 min)

### 2027-03-11 — round 31

- `19:00Z` BAY vs HAP
- `19:05Z` MAC vs ASV
- `19:45Z` RMA vs VIR
- `19:45Z` PRS vs PAN
- `19:45Z` PRT vs EFE

Window: 19:00Z – 19:45Z (45 min)

### 2027-03-18 — round 32

- `19:05Z` MAC vs VAL
- `19:15Z` PAN vs ZAL
- `19:45Z` RMA vs BAS
- `19:45Z` PRT vs BAY

Window: 19:05Z – 19:45Z (40 min)

### 2027-03-26 — round 34

- `19:00Z` BAY vs ZAL
- `19:00Z` CZV vs VAL
- `19:15Z` OLY vs VIR
- `19:30Z` MIL vs MAC
- `19:45Z` RMA vs BJK

Window: 19:00Z – 19:45Z (45 min)

### 2027-04-01 — round 35

- `18:05Z` MAC vs FEN
- `18:30Z` VAL vs RMA
- `18:30Z` MIL vs BJK
- `18:45Z` PRS vs DUB

Window: 18:05Z – 18:45Z (40 min)

### 2027-04-06 — round 36

- `18:30Z` VIR vs VAL
- `18:30Z` BAS vs ASV
- `18:30Z` CZV vs PAN
- `18:45Z` RMA vs MIL
- `18:45Z` PRS vs EFE
- `18:45Z` BAR vs BAY

Window: 18:30Z – 18:45Z (15 min)

### 2027-04-08 — round 37

- `17:45Z` HAP vs CZV
- `18:00Z` BAY vs FEN
- `18:00Z` ASV vs RMA
- `18:15Z` PAN vs VIR
- `18:30Z` VAL vs EFE
- `18:30Z` MIL vs BAS

Window: 17:45Z – 18:30Z (45 min)

### 2027-04-15 — round 38

- `17:30Z` EFE vs HAP
- `18:00Z` CZV vs MIL
- `18:05Z` MAC vs BAS
- `18:15Z` PAN vs RMA

Window: 17:30Z – 18:15Z (45 min)
