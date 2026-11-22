# Team codes

Reading layer only. Every file (`data/decisions_2026_27.csv`,
`data/decision_registry.md`, the forecast CLI) keeps the registry ids; these
are the three-letter codes the cards and the fixture tables print.

| code | team | API code | registry id |
|---|---|---|---|
| BAR | Barcelona | BAR | BAR |
| OLY | Olympiacos | OLY | OLY |
| FEN | Fenerbahçe | **ULK** | FEN |
| EFE | Anadolu Efes | **IST** | EFE |
| RMA | Real Madrid | **MAD** | RMA |
| BAY | Bayern München | **MUN** | BAY |
| MCO | Monaco | MCO | MCO |
| PRS | Paris | **PRS** | **PAR** |
| PRT | Partizan | **PAR** | **PTZ** |
| CZV | Crvena zvezda | **RED** | **ZVE** |
| MAC | Maccabi Tel Aviv | **TEL** | MAC |
| BJK | Beşiktaş | **BES** | BJK |
| HAP | Hapoel Tel Aviv | **HTA** | HAP |
| VAL | Valencia | **PAM** | VAL |
| PAN | Panathinaikos | PAN | PAN |
| ASV | ASVEL | ASV | ASV |
| MIL | Olimpia Milano | MIL | MIL |
| BAS | Baskonia | BAS | BAS |
| VIR | Virtus Bologna | VIR | VIR |
| DUB | Dubai | DUB | DUB |

The traps are Paris/Partizan (the API code `PAR` is Partizan, the registry id
`PAR` is Paris) and Crvena zvezda (`RED` in the API, `ZVE` in the registry,
`CZV` here). `config.short()` maps both onto one display code, so either
input prints correctly.

Change a display code in `src/config.py` (`DISPLAY`), never in the CSVs.
