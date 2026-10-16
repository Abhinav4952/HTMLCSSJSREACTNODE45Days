#!/usr/bin/env python3
"""Fast verification without Maven: javac + JUnit console launcher.
Needs /tmp/libs (assertj, bytebuddy, mockito, objenesis) and /tmp/junit-console.jar.
usage: fast_verify.py 13 14 ...   (solutions must pass; stubs must compile and fail fully)
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
JAVA = "/opt/homebrew/opt/openjdk@21/bin"
LIBS = [str(p) for p in Path("/tmp/libs").glob("*.jar")]
CONSOLE = "/tmp/junit-console.jar"
CP = ":".join(LIBS + [CONSOLE])


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def build_and_test(task: Path, out: Path):
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    srcs = [str(p) for p in task.rglob("*.java")]
    r = run([f"{JAVA}/javac", "-proc:none", "-Xlint:-options", "--release", "21", "-cp", CP, "-d", str(out), *srcs])
    if r.returncode != 0:
        return None, r.stderr
    r = run([f"{JAVA}/java", "-jar", CONSOLE, "execute", "--class-path", f"{out}:{':'.join(LIBS)}",
             "--scan-class-path", str(out), "--details=tree", "--disable-banner", "--disable-ansi-colors"])
    return r.stdout + r.stderr, ""


def counts(text):
    def g(label):
        m = re.search(r"\[\s*(\d+) tests " + label, text)
        return int(m.group(1)) if m else 0
    return g("successful"), g("failed"), g("found")


def main():
    days = [int(x) for x in sys.argv[1:]]
    bad = 0
    subprocess.run([sys.executable, str(HERE / "gen_days_13_24.py"), "--solution", "--out", "/tmp/fv/sol", "--days", *map(str, days)],
                   capture_output=True)
    for d in days:
        for sol_task in sorted((Path("/tmp/fv/sol") / f"Day {d:02d}" / "practical-tasks").glob("task-*")):
            out, err = build_and_test(sol_task, Path("/tmp/fv/out/sol") / sol_task.name)
            if out is None:
                print(f"SOL COMPILE FAIL {d} {sol_task.name}\n{err[:1500]}")
                bad += 1
                continue
            ok, failed, found = counts(out)
            if failed or ok != found or found == 0:
                print(f"SOL TEST FAIL {d} {sol_task.name}: {ok}/{found}\n{out[-2500:]}")
                bad += 1
            else:
                print(f"ok   Day {d:02d} {sol_task.name}: {ok} tests")
            stub_task = ROOT / f"Day {d:02d}" / "practical-tasks" / sol_task.name
            out, err = build_and_test(stub_task, Path("/tmp/fv/out/stub") / sol_task.name)
            if out is None:
                print(f"STUB COMPILE FAIL {d} {sol_task.name}\n{err[:1500]}")
                bad += 1
                continue
            ok, failed, found = counts(out)
            todo_ok = "TODO(Day" in out
            if ok != 0 or failed != found or not todo_ok:
                print(f"STUB PROBLEM {d} {sol_task.name}: passed={ok} failed={failed} found={found} todoMsg={todo_ok}")
                bad += 1
    print("DONE, problems:", bad)


if __name__ == "__main__":
    main()
