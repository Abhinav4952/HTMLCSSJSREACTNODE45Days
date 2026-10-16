#!/usr/bin/env python3
"""Generate the three JAVA PREP capstone projects (docs, PostgreSQL scripts, Spring Boot skeletons).

Usage: python3 scripts/generate_projects.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "projects"))

import p01  # noqa: E402
import p02  # noqa: E402
import p03  # noqa: E402

ROOT = HERE.parent

if __name__ == "__main__":
    for m in (p01, p02, p03):
        m.build(ROOT)
        print("Generated", m.NAME)
