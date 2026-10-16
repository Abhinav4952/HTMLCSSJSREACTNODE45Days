"""Shared generator for JAVA PREP Days 25-42 (SQL/JDBC + Spring Boot phases)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # JAVA PREP/

BOOT_VERSION = "3.4.1"
BOOT_NOTE = (
    "Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds."
)

DAYS: list[dict] = []


def pad(n: int) -> str:
    return f"{n:02d}"


def day(num, title, phase, theme, objectives, prereqs, topics, tasks, interview, mistakes, reading, glossary, hours, spring=False):
    DAYS.append(dict(num=num, title=title, phase=phase, theme=theme, objectives=objectives, prereqs=prereqs,
                     topics=topics, tasks=tasks, interview=interview, mistakes=mistakes, reading=reading,
                     glossary=glossary, hours=hours, spring=spring))


def T(title, what, why, pros, cons, without, syntax, examples, checks):
    """Theory topic. examples: [(title, lang, code)], checks: [(question, answer)]"""
    return dict(title=title, what=what, why=why, pros=pros, cons=cons, without=without, syntax=syntax,
                examples=examples, checks=checks)


def dep(g, a, v=None, scope=None):
    s = f"    <dependency>\n      <groupId>{g}</groupId>\n      <artifactId>{a}</artifactId>\n"
    if v:
        s += f"      <version>{v}</version>\n"
    if scope:
        s += f"      <scope>{scope}</scope>\n"
    return s + "    </dependency>\n"


def task(slug, title, diff, ttype, summary, kind, files, reqs, edges, hints, deps=None, starters=None,
         goals=None, note=None, sol=None):
    """kind: plain | h2 | boot. files: path -> content (main/, test/, res/, tres/ prefixes or raw)."""
    return dict(slug=slug, title=title, diff=diff, ttype=ttype, summary=summary, kind=kind, files=files,
                reqs=reqs, edges=edges, hints=hints, deps=deps or [], starters=starters or [],
                goals=goals or [], note=note, sol=sol or {})


# ------------------------------------------------------------------ boilerplate shared by tasks
APP = """package %PKG%;

import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
}
"""

SQLLAB = """package %PKG%;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * PROVIDED helper (do not edit). Runs the learner's SQL files against an in-memory H2 database in
 * PostgreSQL mode.
 *
 * <ul>
 *   <li>{@code -- ...} lines are comments (including TODO markers).</li>
 *   <li>Statements are split on {@code ;} (do not put semicolons inside string literals).</li>
 *   <li>If a script contains no statements yet, an UnsupportedOperationException with the TODO tag is thrown.</li>
 *   <li>{@code answers.sql} is split into named blocks using marker lines like {@code -- @name}.</li>
 * </ul>
 */
public final class SqlLab {

    /** Base URL from the course spec; {@link #open()} appends a unique database name per test. */
    public static final String BASE_URL =
            "jdbc:h2:mem:%DB%;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DEFAULT_NULL_ORDERING=HIGH";

    private SqlLab() {
    }

    public static Connection open() throws SQLException {
        String url = BASE_URL.replace("mem:%DB%", "mem:%DB%_" + UUID.randomUUID().toString().replace("-", ""))
                + ";DB_CLOSE_DELAY=-1";
        return DriverManager.getConnection(url, "sa", "");
    }

    public static void runScript(Connection c, String path, String tag) throws SQLException, IOException {
        List<String> statements = statements(Files.readString(Path.of(path)));
        if (statements.isEmpty()) {
            throw new UnsupportedOperationException("TODO(" + tag + "): " + path + " has no SQL statements yet");
        }
        try (Statement st = c.createStatement()) {
            for (String s : statements) {
                st.execute(s);
            }
        }
    }

    /** Parses {@code -- @name} blocks; every block must contain one statement. */
    public static Map<String, String> namedBlocks(String path, String tag) throws IOException {
        Map<String, String> out = new LinkedHashMap<>();
        String current = null;
        StringBuilder body = new StringBuilder();
        for (String line : Files.readAllLines(Path.of(path))) {
            String t = line.trim();
            if (t.startsWith("-- @")) {
                if (current != null) {
                    out.put(current, body.toString().trim());
                }
                current = t.substring(4).trim();
                body.setLength(0);
            } else if (!t.startsWith("--") && current != null) {
                body.append(line).append('\\n');
            }
        }
        if (current != null) {
            out.put(current, body.toString().trim());
        }
        for (Map.Entry<String, String> e : out.entrySet()) {
            if (e.getValue().isBlank()) {
                throw new UnsupportedOperationException("TODO(" + tag + "): block '" + e.getKey() + "' in " + path + " is empty");
            }
        }
        return out;
    }

    /** Executes a named block and returns rows (SELECT) as lists of values. */
    public static List<List<Object>> query(Connection c, String sql) throws SQLException {
        List<List<Object>> rows = new ArrayList<>();
        try (Statement st = c.createStatement(); ResultSet rs = st.executeQuery(stripSemicolon(sql))) {
            ResultSetMetaData md = rs.getMetaData();
            while (rs.next()) {
                List<Object> row = new ArrayList<>();
                for (int i = 1; i <= md.getColumnCount(); i++) {
                    row.add(rs.getObject(i));
                }
                rows.add(row);
            }
        }
        return rows;
    }

    public static int update(Connection c, String sql) throws SQLException {
        try (Statement st = c.createStatement()) {
            return st.executeUpdate(stripSemicolon(sql));
        }
    }

    public static long scalar(Connection c, String sql) throws SQLException {
        return ((Number) query(c, sql).get(0).get(0)).longValue();
    }

    private static String stripSemicolon(String sql) {
        String s = sql.trim();
        return s.endsWith(";") ? s.substring(0, s.length() - 1) : s;
    }

    static List<String> statements(String script) {
        StringBuilder cleaned = new StringBuilder();
        for (String line : script.split("\\\\R")) {
            if (!line.trim().startsWith("--")) {
                cleaned.append(line).append('\\n');
            }
        }
        List<String> out = new ArrayList<>();
        for (String part : cleaned.toString().split(";")) {
            if (!part.isBlank()) {
                out.add(part.trim());
            }
        }
        return out;
    }
}
"""


def sqllab(day_num: int) -> str:
    return SQLLAB.replace("%DB%", f"day{pad(day_num)}")


# ------------------------------------------------------------------ poms
def pom_xml(day_num, artifact, t):
    kind = t["kind"]
    extra = "".join(t["deps"])
    if kind == "boot":
        starters = "".join(dep("org.springframework.boot", s) for s in t["starters"])
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <!-- {BOOT_NOTE} -->
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>{BOOT_VERSION}</version>
    <relativePath/>
  </parent>
  <groupId>com.javaprep.day{pad(day_num)}</groupId>
  <artifactId>{artifact}</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <name>Day {pad(day_num)} — {artifact}</name>
  <properties>
    <java.version>21</java.version>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>
  <dependencies>
{starters}{extra}{dep("org.springframework.boot", "spring-boot-starter-test", scope="test")}  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration>
          <!-- Lets Mockito/ByteBuddy/Hibernate proxies work on JDKs newer than 21 (harmless on 21). -->
          <argLine>-Dnet.bytebuddy.experimental=true</argLine>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
"""
    h2 = dep("com.h2database", "h2", "2.3.232", "test") if kind == "h2" else ""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.javaprep.day{pad(day_num)}</groupId>
  <artifactId>{artifact}</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <name>Day {pad(day_num)} — {artifact}</name>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>
  <dependencies>
{extra}{h2}{dep("org.junit.jupiter", "junit-jupiter", "5.11.4", "test")}{dep("org.assertj", "assertj-core", "3.27.3", "test")}  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.13.0</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.2</version>
      </plugin>
    </plugins>
  </build>
</project>
"""


# ------------------------------------------------------------------ writers
def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def subst(s: str, d: int, t: int) -> str:
    return (s.replace("%PKG%", f"com.javaprep.day{pad(d)}.task{pad(t)}")
             .replace("%TAG%", f"Day{pad(d)}-task{pad(t)}")
             .replace("%XX%", pad(d)).replace("%YY%", pad(t)))


def resolve_path(key: str, d: int, t: int) -> str:
    pkg = f"com/javaprep/day{pad(d)}/task{pad(t)}"
    if key.startswith("main/"):
        return f"src/main/java/{pkg}/{key[5:]}"
    if key.startswith("test/"):
        return f"src/test/java/{pkg}/{key[5:]}"
    if key.startswith("res/"):
        return f"src/main/resources/{key[4:]}"
    if key.startswith("tres/"):
        return f"src/test/resources/{key[5:]}"
    return key


def theory_md(d):
    xx = pad(d["num"])
    tasks = ", ".join(f"`task-{pad(i)}-{t['slug']}`" for i, t in enumerate(d["tasks"], 1))
    spring = f"Java 21, Spring Boot {BOOT_VERSION} (course target: Spring Boot 4 when available)" if d["spring"] else "Java 21, H2 2.3.232 (PostgreSQL mode)"
    L = [f"# Day {xx} — {d['title']}", "",
         f"**Phase:** {d['phase']}  ",
         f"**Primary theme:** {d['theme']}  ",
         f"**Estimated study time:** {d['hours']}  ",
         f"**Related tasks:** {tasks}  ",
         f"**Instruction alignment:** Maps to Day {xx} in the 50-day topic map (`course-generation-instructions/04`).  ",
         f"**Java / Spring versions:** {spring}", ""]
    if d["spring"]:
        L += [f"> **Note:** {BOOT_NOTE} Production APIs shown here are largely identical in Boot 4; "
              "differences (starter splitting, Jackson 3) are called out where they matter.", ""]
    L += ["## Overview", "", d["theme"] + ". "
          "This day gives you the mental model first, then makes you prove it with tests. "
          "In real backend work these topics decide whether your service is correct, secure, and operable; "
          "in interviews they are the topics where shallow answers are exposed quickly.", "",
          "## Day roadmap", ""]
    for i, tp in enumerate(d["topics"], 1):
        L.append(f"{i}. {tp['title']}")
    L += [f"{len(d['topics']) + 1}. Interview corner, common mistakes, glossary", "",
          "## Subtopics", ""]
    for tp in d["topics"]:
        L += [f"### {tp['title']}", "", "#### What it is", "", tp["what"], "",
              "#### Why it exists / why it matters", "", tp["why"], "",
              "#### Pros and cons", "", "**Pros**", ""]
        L += [f"- {p}" for p in tp["pros"]]
        L += ["", "**Cons / trade-offs**", ""]
        L += [f"- {c}" for c in tp["cons"]]
        L += ["", "#### What happens without it / when misused", "", tp["without"], "",
              "#### Syntax and rules", "", tp["syntax"], "", "#### Examples", ""]
        for i, (et, lang, code) in enumerate(tp["examples"], 1):
            L += [f"**Example {i} — {et}**", "", f"```{lang}", code.strip("\n"), "```", ""]
        L += ["#### Quick checks", ""]
        L += [f"{i}. {q}" for i, (q, _) in enumerate(tp["checks"], 1)]
        L.append("")
    L += ["## Interview corner", ""]
    for i, (q, a) in enumerate(d["interview"], 1):
        L += [f"**Q{i}. {q}**", "", a, ""]
    L += ["## Common mistakes & debugging", ""] + [f"- {m}" for m in d["mistakes"]] + ["", "## Further reading", ""]
    L += [f"- {r}" for r in d["reading"]] + ["", "## Glossary", "", "| Term | Meaning |", "|------|---------|"]
    L += [f"| {a} | {b} |" for a, b in d["glossary"]] + ["", "## Answers", ""]
    for tp in d["topics"]:
        L += [f"### {tp['title']}", ""]
        L += [f"{i}. {a}" for i, (_, a) in enumerate(tp["checks"], 1)]
        L.append("")
    return "\n".join(L)


def readme_md(d):
    xx = pad(d["num"])
    L = [f"# Day {xx} — {d['title']}", "", "## Learning objectives", ""]
    L += [f"- {o}" for o in d["objectives"]]
    L += ["", "## Prerequisites", ""] + [f"- {p}" for p in d["prereqs"]]
    if d["spring"]:
        L += ["", "## Spring Boot version note", "", f"{BOOT_NOTE}"]
    L += ["", "## How to use this folder", "",
          f"1. Read [`DAY-{xx}-THEORY-AND-REFERENCE.md`](DAY-{xx}-THEORY-AND-REFERENCE.md) first.",
          "2. Open each task folder as its own Maven project in IntelliJ.",
          "3. Run `mvn test` (red) -> implement the `TODO(DayXX-taskYY)` markers -> `mvn test` (green).",
          "", "## Task list", "", "| Order | Folder | Type | Verify with |", "|------:|--------|------|-------------|"]
    for i, t in enumerate(d["tasks"], 1):
        L.append(f"| {i} | `task-{pad(i)}-{t['slug']}` | {t['ttype']} | `mvn test` |")
    L += ["", f"**Estimated time:** {d['hours']}  ", f"**Phase:** {d['phase']}", ""]
    return "\n".join(L)


CONSTRAINTS = {
    "plain": "Java 21; no Spring; no Lombok.",
    "h2": "Java 21; plain JDBC/SQL only (no Spring, no Lombok); H2 2.3.232 in PostgreSQL mode is the only database.",
    "boot": f"Java 21; Spring Boot {BOOT_VERSION} starters already declared in `pom.xml`; no Lombok; do not add dependencies.",
}


def task_md(d, t, n, main_todos, test_names):
    xx, yy = pad(d["num"]), pad(n)
    tag = f"Day{xx}-task{yy}"
    provided = "\n".join(f"| `{resolve_path(k, d['num'], n)}` | {'Stubs / starter code (edit the TODOs)' if 'TODO(' in subst(v, d['num'], n) else 'Provided helper or test (do not edit)'} |"
                         for k, v in t["files"].items())
    todo_rows = "\n".join(f"| `{p}` | `{tg}` | {txt} |" for p, tg, txt in main_todos) or f"| (see sources) | `TODO({tag})` | implement |"
    test_rows = "\n".join(f"| {i} | `{n_}` |" for i, n_ in enumerate(test_names, 1))
    reqs = "\n".join(f"{i}. {r}" for i, r in enumerate(t["reqs"], 1))
    edges = "\n".join(f"- {e}" for e in t["edges"])
    hints = "\n".join(f"<details><summary>Hint {i}</summary>\n{h}\n</details>\n" for i, h in enumerate(t["hints"], 1))
    goals = "\n".join(f"- {g}" for g in (t["goals"] or ["Apply today's theory to a small, testable problem", "Drive the work from failing tests (`mvn test`)", "Replace stubs/TODO markers with real behavior"]))
    note = f"\n> {BOOT_NOTE}\n" if d["spring"] else ""
    return f"""# Task {n} — {t['title']}

**Day:** {xx} · **Task ID:** {tag} · **Type:** {t['ttype']} · **Difficulty:** {t['diff']}
{note}
## Summary

{t['summary']}

## Learning goals

{goals}

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21) |
{provided}

## Prerequisites

- Day {xx} theory read
- JDK 21 + Maven 3.9+ on PATH

## What you will implement

{reqs}

## Constraints

- {CONSTRAINTS[t['kind']]}
- Do not edit test files or this document; edit only the places marked `TODO({tag})`.
- Do not hard-code values just to satisfy a test — implement real behavior.

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO({tag})` (or fail on missing behavior).
2. Work through the requirements above one at a time, re-running the matching test.
3. Run the full suite until it is green.
4. Commit: `Day {xx}: complete task-{yy}-{t['slug']}`.

## How to run and verify

```bash
java -version   # 21.x
mvn -v          # 3.9+
mvn test        # expected RED at the start
mvn -Dtest=<TestClass> test
```

## TODO map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
{todo_rows}

## Test map

| # | Test method |
|--:|-------------|
{test_rows}

## Edge cases to handle

{edges}

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] No `target/` or IDE files committed; no secrets
- [ ] Commit message: `Day {xx}: {t['title']}`

## Hints (optional)

{hints}"""


def eval_md(d, t, n):
    xx, yy = pad(d["num"]), pad(n)
    reqs = "\n".join(f"- {r}" for r in t["reqs"])
    edges = "\n".join(f"- {e}" for e in t["edges"])
    return f"""# Evaluation Criteria — Day {xx} — Task {yy} — {t['title']}

## Scope

Automated JUnit verification plus light code/SQL quality review for Day {xx} Task {yy} (`{t['slug']}`).

## Weighting (100 points)

| Category | Points |
|----------|-------:|
| Correctness (all tests green, requirements met) | 60 |
| Edge cases and error contracts | 20 |
| Code clarity (naming, simplicity, idiomatic Spring/SQL) | 15 |
| Git / hygiene (no `target/`, no secrets, only intended files changed) | 5 |

## Pass / fail gates (automatic fail if violated)

- Project does not compile or `mvn test` fails
- Tests, `pom.xml`, or provided helpers modified to force a pass
- Hard-coded answers that special-case test inputs
- Secrets or `target/` committed

## Detailed rubric

### Correctness

{reqs}

### Edge cases

{edges}

### Security / privacy

- No SQL built by string concatenation with user input; no secrets in source; no sensitive data in logs (where applicable).

## Evidence the grader should collect

- Output of `mvn test`
- Diff of files containing `TODO(Day{xx}-task{yy})`

## AI grading prompt (paste into your grader)

```
You are grading Day {xx} Task {yy} ({t['title']}) for a graduate Java backend course.
Use only observable evidence (mvn test output and the diff). Score /100 with the rubric weights.
List blocking issues first. Penalize hard-coded outputs and edited tests. Leftover TODO comments are fine
when behavior is implemented and tests pass.
```
"""


def generate_day(d):
    xx = pad(d["num"])
    base = ROOT / f"Day {xx}"
    write(base / "README.md", readme_md(d))
    write(base / f"DAY-{xx}-THEORY-AND-REFERENCE.md", theory_md(d))
    for n, t in enumerate(d["tasks"], 1):
        tdir = base / "practical-tasks" / f"task-{pad(n)}-{t['slug']}"
        todos, tests = [], []
        for k, v in t["files"].items():
            content = subst(v, d["num"], n)
            rel = resolve_path(k, d["num"], n)
            write(tdir / rel, content)
            for line in content.splitlines():
                m = re.search(r"TODO\((Day\d+-task\d+)\):\s*(.*)", line)
                if not m or k.startswith("test/") or "UnsupportedOperationException" in line:
                    continue
                txt = m.group(2).strip().rstrip('");*/ ').strip()
                todos.append((rel.split("/")[-1], m.group(1), txt))
            if k.startswith("test/"):
                tests += re.findall(r"void\s+(\w+)\s*\(", content)
        seen, dedup = set(), []
        for x in todos:
            if (x[0], x[2]) not in seen:
                seen.add((x[0], x[2]))
                dedup.append(x)
        write(tdir / "pom.xml", pom_xml(d["num"], f"task-{pad(n)}-{t['slug']}", t))
        write(tdir / "TASK_INSTRUCTIONS.md", task_md(d, t, n, dedup, tests))
        write(tdir / "EVALUATION_CRITERIA.md", eval_md(d, t, n))
        write(tdir / ".gitignore", "target/\n.idea/\n*.iml\n")
