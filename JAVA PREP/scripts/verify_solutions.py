#!/usr/bin/env python3
"""Maintainer tool: copy each task to /tmp, apply the reference solution (task['sol']), run mvn test.

Usage: python3 scripts/verify_solutions.py <day> [task-index ...]
Set MVN_SETTINGS to a settings.xml if your default Maven mirror is unreachable.
"""
import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "days_25_42"))
import common  # noqa: E402

day = int(sys.argv[1])
only = {int(a) for a in sys.argv[2:]}
importlib.import_module(f"d{day}")
d = next(x for x in common.DAYS if x["num"] == day)
settings = os.environ.get("MVN_SETTINGS")
for n, t in enumerate(d["tasks"], 1):
    if only and n not in only:
        continue
    if not t["sol"]:
        print(f"task {n}: no reference solution, skipped")
        continue
    src = common.ROOT / f"Day {day:02d}/practical-tasks/task-{n:02d}-{t['slug']}"
    dst = Path("/tmp/verify") / f"d{day}t{n}"
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("target"))
    for k, v in t["sol"].items():
        common.write(dst / common.resolve_path(k, day, n), common.subst(v, day, n))
    cmd = ["mvn", "-q"] + (["-s", settings] if settings else []) + ["test"]
    r = subprocess.run(cmd, cwd=dst, capture_output=True, text=True)
    out = r.stdout + r.stderr
    print(f"task {n} {t['slug']}: {'PASS' if r.returncode == 0 else 'FAIL'}")
    if r.returncode:
        print("\n".join(l for l in out.splitlines() if "ERROR" in l or "Exception" in l or "expected" in l.lower())[:3500])
