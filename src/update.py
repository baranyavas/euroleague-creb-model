"""One command to refresh the whole repo.

    python -m src.update

fetch + build -> validate -> season report -> registry backfill -> STATE.md

The retrospective backtest needs numpy/pandas (it imports model/), so run it
separately with the venv:

    ./.venv/bin/python -m src.forecast --backtest
"""

from __future__ import annotations

import sys

from . import build, report, state, validate


def _run_backtest() -> None:
    """Retrospective check; needs numpy/pandas, so it is optional."""
    try:
        from . import forecast
    except ModuleNotFoundError as exc:
        print(f"skip backtest ({exc}); run it with ./.venv/bin/python", file=sys.stderr)
        return
    rows = forecast.load_team_games()
    idx = forecast.team_index(rows)
    games = forecast.load_games()
    decisions = forecast.load_decisions()
    forecast.write_backtest(forecast.backtest(idx, games, decisions))


def main() -> int:
    print("== build ==")
    build.build()

    print("\n== validate ==")
    if validate.main() != 0:
        print("\nvalidation failed; stopping before the report.", file=sys.stderr)
        return 1

    print("\n== report ==")
    report.main()

    print("\n== backtest ==")
    _run_backtest()

    print("\n== state ==")
    state.main()

    print("\ndone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
