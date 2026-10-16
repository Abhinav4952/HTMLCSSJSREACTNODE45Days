#!/usr/bin/env python3
"""Verify tasks with Maven: stub must FAIL tests (not compile errors); stub+reference solution must PASS.
usage: JAVA_HOME=... MVN_SETTINGS=... verify_stage.py day [day ...] [-t N]
"""
import importlib, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "days_25_42"))
import common  # noqa
args = sys.argv[1:]
days = [int(a) for a in args if a.isdigit()]
settings = os.environ.get("MVN_SETTINGS")

def mvn(d):
    cmd = ["mvn", "-q", "-B"] + (["-s", settings] if settings else []) + ["test"]
    r = subprocess.run(cmd, cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr

def check(job):
    day, n, t = job
    src = common.ROOT / f"Day {day:02d}/practical-tasks/task-{n:02d}-{t['slug']}"
    dst = Path("/tmp/verify") / f"d{day}t{n}"
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("target"))
    rc, out = mvn(dst)
    msgs = []
    if rc == 0: msgs.append("STUB PASSES (should fail)")
    elif "COMPILATION ERROR" in out: msgs.append("STUB COMPILE ERROR\n" + out[:1500])
    for k, v in t["sol"].items():
        common.write(dst / common.resolve_path(k, day, n), common.subst(v, day, n))
    rc, out = mvn(dst)
    if rc != 0:
        msgs.append("SOLUTION FAIL\n" + "\n".join(l for l in out.splitlines() if "ERROR" in l or "FAIL" in l)[:3500])
    return f"Day {day} task {n} {t['slug']}: " + ("OK" if not msgs else "\n".join(msgs))

jobs = []
for day in days:
    importlib.import_module(f"d{day}")
    d = next(x for x in common.DAYS if x["num"] == day)
    for n, t in enumerate(d["tasks"], 1):
        jobs.append((day, n, t))
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(check, jobs):
        print(res, flush=True)
