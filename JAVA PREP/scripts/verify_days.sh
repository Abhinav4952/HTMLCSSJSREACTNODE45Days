#!/usr/bin/env bash
# Verify generated tasks: solutions must pass; stubs must compile and fail.
# usage: scripts/verify_days.sh 13 14 ...
set -u
export JAVA_HOME=${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}
export PATH="$JAVA_HOME/bin:$PATH"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
SOL=/tmp/javaprep-verify-sol
rm -rf "$SOL"
python3 "$HERE/gen_days_13_24.py" --solution --out "$SOL" --days "$@" >/dev/null
fail=0
for d in "$@"; do
  for t in "$SOL/Day $d"/practical-tasks/*/; do
    out=$(cd "$t" && mvn -s /tmp/central-settings.xml -q -B test 2>&1); rc=$?
    if [ $rc -ne 0 ]; then echo "SOLUTION FAIL: $t"; echo "$out" | grep -E "ERROR|FAIL|expected|Expecting" | head -15; fail=1; else echo "ok  $t"; fi
  done
  for t in "$ROOT/Day $d"/practical-tasks/*/; do
    out=$(cd "$t" && mvn -s /tmp/central-settings.xml -q -B test 2>&1); rc=$?
    if [ $rc -eq 0 ]; then echo "STUB PASSES (bad): $t"; fail=1; fi
    if echo "$out" | grep -q "COMPILATION ERROR"; then echo "STUB COMPILE ERROR: $t"; echo "$out" | grep ERROR | head; fail=1; fi
    tests=$(echo "$out" | grep -E "Tests run:.*Fail" | tail -1)
    echo "stub $t -> $tests"
    (cd "$t" && rm -rf target)
  done
done
exit $fail
