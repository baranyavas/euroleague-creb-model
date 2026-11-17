"""Build the c-reb dataset from cached EuroLeague XML.

    python -m src.build            # use cache, fetch what is missing
    python -m src.build --refresh  # re-download results + box scores

Writes:
    data/processed/games.csv       one row per game
    data/processed/team_games.csv  one row per team-game
"""

from __future__ import annotations

import argparse
import csv
import sys
import time

from . import config, el_api


def build(refresh: bool = False) -> None:
    config.DATA_PROC.mkdir(parents=True, exist_ok=True)
    games_rows: list[dict] = []
    team_rows: list[dict] = []
    problems: list[str] = []

    for season in config.SEASONS:
        results = el_api.parse_results(el_api.results_xml(season, refresh=refresh))
        if config.REGULAR_SEASON_ONLY:
            results = [g for g in results if g["phase"] == "RS"]
        results.sort(key=lambda g: (g["date"], g["code"]))
        print(f"{season}: {len(results)} regular-season games", flush=True)

        for i, meta in enumerate(results, 1):
            if i % 25 == 0:
                print(f"  {i}/{len(results)}", flush=True)
            try:
                box = el_api.parse_game(
                    el_api.game_xml(season, meta["code"], refresh=refresh)
                )
            except Exception as exc:
                problems.append(f"{season} game {meta['code']}: {exc}")
                continue

            home, away = box["home"], box["away"]
            creb_total = home["creb"] + away["creb"]
            miss_total = home["missed_fg"] + away["missed_fg"]
            reboppr_t = round(creb_total / miss_total, 3) if miss_total else ""

            games_rows.append(
                {
                    "season": season,
                    "phase": meta["phase"],
                    "gameday": meta["gameday"],
                    "date": meta["date"],
                    "gamecode": meta["code"],
                    "away_id": config.club_id(meta["away_code"]),
                    "home_id": config.club_id(meta["home_code"]),
                    "away_name": meta["away_name"],
                    "home_name": meta["home_name"],
                    "away_score": meta["away_score"],
                    "home_score": meta["home_score"],
                    "creb_away": away["creb"],
                    "creb_home": home["creb"],
                    "creb_total": creb_total,
                    "team_reb_away": away["team_reb"],
                    "team_reb_home": home["team_reb"],
                    "missed_fg_away": away["missed_fg"],
                    "missed_fg_home": home["missed_fg"],
                    "missed_fg_total": miss_total,
                    "poss_total": round(home["poss"] + away["poss"], 1),
                    "reboppr_t": reboppr_t,
                }
            )

            for side, other, is_home in (("home", "away", 1), ("away", "home", 0)):
                me, opp = box[side], box[other]
                team_rows.append(
                    {
                        "season": season,
                        "phase": meta["phase"],
                        "gameday": meta["gameday"],
                        "date": meta["date"],
                        "gamecode": meta["code"],
                        "team_id": config.club_id(meta[f"{side}_code"]),
                        "team_name": meta[f"{side}_name"],
                        "opp_id": config.club_id(meta[f"{other}_code"]),
                        "home": is_home,
                        "creb": me["creb"],
                        "opp_creb": opp["creb"],
                        "total_reb": me["total_reb"],
                        "team_reb": me["team_reb"],
                        "oreb": me["oreb"],
                        "dreb": me["dreb"],
                        "fga": me["fga"],
                        "fgm": me["fgm"],
                        "fta": me["fta"],
                        "ftm": me["ftm"],
                        "tov": me["tov"],
                        "missed_fg": me["missed_fg"],
                        "opp_missed_fg": opp["missed_fg"],
                        "poss": round(me["poss"], 1),
                        "reboppr_o": (
                            round(me["oreb"] / me["missed_fg"], 3)
                            if me["missed_fg"] else ""
                        ),
                        "reboppr_d": (
                            round(me["dreb"] / opp["missed_fg"], 3)
                            if opp["missed_fg"] else ""
                        ),
                    }
                )

        # bar beat: nothing to do here, just keeps the loop readable
        time.sleep(0)

    _write(config.DATA_PROC / "games.csv", games_rows)
    _write(config.DATA_PROC / "team_games.csv", team_rows)

    print(f"wrote {len(games_rows)} games / {len(team_rows)} team-games")
    if problems:
        print("problems:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)


def _write(path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    build(refresh=args.refresh)
