#!/usr/bin/env python3
"""Generate JAVA PREP Day 13-24 folders.

Usage:
  python3 scripts/gen_days_13_24.py                      # write stubs + docs into JAVA PREP/
  python3 scripts/gen_days_13_24.py --solution --out /tmp/verify [--days 13 14]
                                                         # reference solutions (to verify the tests)
Day data lives in scripts/days/dayNN.py (each defines DAY).
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "days"))

import gen_lib  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(gen_lib.ROOT))
    ap.add_argument("--solution", action="store_true")
    ap.add_argument("--days", nargs="*", type=int, default=list(range(13, 25)))
    args = ap.parse_args()
    for n in args.days:
        d = importlib.import_module(f"day{n}").DAY
        gen_lib.generate_day(d, Path(args.out), stub=not args.solution, docs=not args.solution)
        print(f"Day {n:02d}: {len(d['tasks'])} tasks")


if __name__ == "__main__":
    main()
