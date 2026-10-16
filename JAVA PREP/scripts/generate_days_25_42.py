#!/usr/bin/env python3
"""Generate JAVA PREP Day 25-42 folders (theory, README, 4 Maven tasks each).

Usage: python3 scripts/generate_days_25_42.py [day ...]
"""
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "days_25_42"))

import common  # noqa: E402

MODULES = ["d25", "d26", "d27", "d28", "d29", "d30", "d31", "d32", "d33", "d34", "d35", "d36", "d37", "d38",
           "d39", "d40", "d41", "d42"]


def main() -> None:
    only = {int(a) for a in sys.argv[1:]}
    for m in MODULES:
        try:
            importlib.import_module(m)
        except ModuleNotFoundError as e:
            if e.name == m:
                continue
            raise
    for d in sorted(common.DAYS, key=lambda x: x["num"]):
        if only and d["num"] not in only:
            continue
        common.generate_day(d)
        print(f"Generated Day {d['num']:02d} — {d['title']} ({len(d['tasks'])} tasks)")


if __name__ == "__main__":
    main()
