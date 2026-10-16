"""Helper: write each source once with stub markers; derive learner stub + reference solution.

Markers (own line, inside Java sources):
    //B! description   ... code ...   //E!   -> stub: TODO comment + throw UnsupportedOperationException
    //A! description   ... code ...   //E!   -> stub: TODO comment only (annotations/fields/config)
"""
import re

from common import *  # noqa: F401,F403


def split_markers(code: str):
    stub, sol, mode, ind = [], [], None, ""
    for line in code.split("\n"):
        s = line.strip()
        m = re.match(r"//([BA])!\s*(.*)$", s)
        if m and mode is None:
            mode, desc = m.group(1), m.group(2)
            ind = line[: len(line) - len(line.lstrip())]
            stub.append(f"{ind}// TODO(%TAG%): {desc}")
            if mode == "B":
                stub.append(f'{ind}throw new UnsupportedOperationException("TODO(%TAG%): {desc.replace(chr(34), chr(39))}");')
            continue
        if s == "//E!":
            mode = None
            continue
        if mode is None or s.startswith("//"):
            stub.append(line)  # code outside regions, and comments inside regions, stay visible to learners
        sol.append(line)
    return "\n".join(stub), "\n".join(sol)


def tk(slug, title, diff, summary, srcs, tests, reqs, edges, hints, starters, deps=None, extra=None,
       ttype="Spring Boot", goals=None):
    files, sol = {}, {}
    for k, v in srcs.items():
        stub, full = split_markers(v)
        files[k] = stub
        if stub != full:
            sol[k] = full
    files.update(tests)
    files.update(extra or {})
    return task(slug, title, diff, ttype, summary, "boot", files, reqs, edges, hints, deps=deps or [],
                starters=starters, goals=goals, sol=sol)


H2 = dep("com.h2database", "h2", None, "test")
H2_PG_PROPS = ("spring.datasource.url=jdbc:h2:mem:%DBNAME%;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DEFAULT_NULL_ORDERING=HIGH;DB_CLOSE_DELAY=-1\n"
               "spring.datasource.username=sa\nspring.datasource.password=\n"
               "spring.jpa.hibernate.ddl-auto=create-drop\nspring.jpa.open-in-view=false\n"
               "spring.test.database.replace=none\n")


def h2props(day, t, extra=""):
    return H2_PG_PROPS.replace("%DBNAME%", f"day{day}t{t}") + extra
