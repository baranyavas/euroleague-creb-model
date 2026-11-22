# Team codes

One scheme, everywhere: `data/decisions_2026_27.csv`,
`data/decision_registry.md`, `data/processed/`, the model and the cards all
use the codes in the left column. The EuroLeague API speaks a different code
for eleven clubs; `config.club_id()` converts them **at the edge** (build,
slate, nights), so an API code never reaches a file.

| code | team | API code |
|---|---|---|
| BAR | Barcelona | BAR |
| OLY | Olympiacos | OLY |
| FEN | Fenerbahçe | **ULK** |
| EFE | Anadolu Efes | **IST** |
| RMA | Real Madrid | **MAD** |
| BAY | Bayern München | **MUN** |
| MCO | Monaco | MCO |
| PRS | Paris | PRS |
| PRT | Partizan | **PAR** |
| CZV | Crvena zvezda | **RED** |
| MAC | Maccabi Tel Aviv | **TEL** |
| BJK | Beşiktaş | **BES** |
| HAP | Hapoel Tel Aviv | **HTA** |
| VAL | Valencia | **PAM** |
| PAN | Panathinaikos | PAN |
| ASV | ASVEL | ASV |
| MIL | Olimpia Milano | MIL |
| BAS | Baskonia | BAS |
| VIR | Virtus Bologna | VIR |
| DUB | Dubai | DUB |
| ZAL | Žalgiris Kaunas | ZAL |

## The Paris/Partizan trap, and how it is closed

It used to be two schemes at once: the API's `PAR` was **Partizan**, while the
registry's `PAR` was **Paris**. A bare `PAR` therefore had no safe reading, and
a lookup in the wrong space would silently price Partizan as Paris.

It is resolved by deleting one of the two names:

- **Paris is `PRS`. Partizan is `PRT`.** Neither is `PAR` any more, in any file.
- `PAR` now exists only as an API code, and `club_id("PAR") = "PRT"` runs in
  `build.py` before anything is written.
- `python -m src.validate` fails if an API code ever appears in
  `data/processed/` or if a team id is missing from `TEAM_NAME`.

If a new club appears, add it to `TEAM_NAME` and, when the API calls it
something else, to `CLUB_ID`. Then run `python -m src.validate`.
