"""Validate the built dataset against the numbers already published in README.

This is a regression test for the pipeline, not a new model:
if the parser is right, the 2025-26 regular season must reproduce the
baseline that v0.7 was built on.

    python -m src.validate
"""

from __future__ import annotations

import csv
import math
import statistics

from . import config

# Published in README.md ("2025-26 first findings").
EXPECTED = {
    "games": 380,
    "mean_creb": 62.01,
    "median_creb": 61,
    "sd_creb": 7.56,
    "mean_missed_fg": 67.53,
    "pct_70": 14.5,
    "pct_80": 1.3,
    "corr": 0.907,
    "r2": 0.823,
    "ols_intercept": 3.126,
    "ols_beta": 0.8719,
}


def load_games(season: str) -> list[dict]:
    path = config.DATA_PROC / "games.csv"
    with path.open(newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r["season"] == season]


def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    beta = sxy / sxx
    intercept = my - beta * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (intercept + beta * x)) ** 2 for x, y in zip(xs, ys))
    return intercept, beta, 1 - ss_res / ss_tot


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(
        sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)
    )
    return num / den


def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    flag = "PASS" if ok else "FAIL"
    print(f"  [{flag}] {name:<16} got {got:>10.3f}   repo {want:>10.3f}")
    return ok


def main() -> int:
    games = load_games(config.BASE_SEASON)
    creb = [int(g["creb_total"]) for g in games]
    miss = [int(g["missed_fg_total"]) for g in games]
    n = len(games)

    print(f"{config.BASE_SEASON} regular season: {n} games")
    intercept, beta, r2 = ols(miss, creb)
    corr = pearson(miss, creb)

    results = [
        check("games", n, EXPECTED["games"], 0),
        check("mean c-reb", statistics.mean(creb), EXPECTED["mean_creb"], 0.05),
        check("median c-reb", statistics.median(creb), EXPECTED["median_creb"], 0.5),
        check("sd c-reb", statistics.pstdev(creb), EXPECTED["sd_creb"], 0.05),
        check("mean missed fg", statistics.mean(miss), EXPECTED["mean_missed_fg"], 0.05),
        check(
            "70+ share %",
            100 * sum(c >= 70 for c in creb) / n,
            EXPECTED["pct_70"],
            0.2,
        ),
        check(
            "80+ share %",
            100 * sum(c >= 80 for c in creb) / n,
            EXPECTED["pct_80"],
            0.2,
        ),
        check("corr", corr, EXPECTED["corr"], 0.005),
        check("OLS r2", r2, EXPECTED["r2"], 0.005),
        check("OLS intercept", intercept, EXPECTED["ols_intercept"], 0.05),
        check("OLS beta", beta, EXPECTED["ols_beta"], 0.005),
    ]

    # Settlement identity per team-game: total_reb = c-reb + team_reb.
    with (config.DATA_PROC / "team_games.csv").open(newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["season"] == config.BASE_SEASON]
    bad = [
        r for r in rows
        if int(r["total_reb"]) != int(r["creb"]) + int(r["team_reb"])
    ]
    print(f"\nsettlement identity (total = c-reb + team): {len(rows) - len(bad)}/{len(rows)}")
    if bad:
        print("  broken rows:", len(bad))

    # One canonical code scheme: processed data must hold canonical ids only.
    # An API code that still maps somewhere (PAR -> PRT) means the edge
    # conversion was skipped, and PAR would silently read as Paris.
    with (config.DATA_PROC / "team_games.csv").open(newline="", encoding="utf-8") as fh:
        ids = {r["team_id"] for r in csv.DictReader(fh)} | {
            r["opp_id"] for r in csv.DictReader(fh)
        }
    unknown = sorted(i for i in ids if i not in config.TEAM_NAME)
    leaked = sorted(i for i in ids if config.club_id(i) != i)
    print(f"\nteam codes: {len(ids)} ids, unknown {unknown or 'none'}, "
          f"api codes leaked {leaked or 'none'}")
    codes_ok = not unknown and not leaked

    ok = all(results) and not bad and codes_ok
    print("\nBASELINE REPRODUCED" if ok else "\nBASELINE MISMATCH — do not trust the parser")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
