#!/usr/bin/env python3
"""Generate JAVA PREP Day 43-50 folders (theory, README, 4 Maven tasks each).

Reuses the shared generator in scripts/days_25_42/common.py (same task layout, poms and docs).

Usage: python3 scripts/generate_days_43_50.py [day ...]

Design decisions (documented in the day theory files):
  * Spring Boot version is inherited from common.BOOT_VERSION (3.4.1, same as Days 28/29).
  * Day 44 simulates the gateway filter chain in plain Java instead of depending on the reactive
    spring-cloud-starter-gateway + Spring Cloud BOM (Project 03 uses the real gateway).
  * Kafka tests use spring-kafka-test @EmbeddedKafka (no Docker, no local broker).
  * JPA tests use H2; no Lombok anywhere.
  * No JDK is required to GENERATE; run `mvn test` inside a task to verify (expected RED before solving).
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "days_25_42"))
sys.path.insert(0, str(HERE / "days_43_50"))

import common  # noqa: E402

MODULES = ["d43", "d44", "d45", "d46", "d47", "d48", "d49", "d50"]


def main() -> None:
    only = {int(a) for a in sys.argv[1:]}
    mods = {m: importlib.import_module(m) for m in MODULES}
    for d in sorted((x for x in common.DAYS if x["num"] >= 43), key=lambda x: x["num"]):
        if only and d["num"] not in only:
            continue
        common.generate_day(d)
        print(f"Generated Day {d['num']:02d} - {d['title']} ({len(d['tasks'])} tasks)")
    for m in mods.values():
        for rel, content in getattr(m, "EXTRA", {}).items():
            common.write(common.ROOT / rel, content)
            print(f"Wrote {rel}")


if __name__ == "__main__":
    main()
