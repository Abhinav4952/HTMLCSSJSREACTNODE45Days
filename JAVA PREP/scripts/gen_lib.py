#!/usr/bin/env python3
"""Shared generator library for JAVA PREP days 13-24.

Task Java sources are authored in *solution form* with markers:

    //@TODO label | actionable instruction
    ...solution body...
    //@END

In stub mode the marked region becomes a TODO comment plus
`throw new UnsupportedOperationException("TODO(DayXX-taskYY): ...")`.
In solution mode (used only to verify the tests) markers are dropped.
Test classes name requirement-grouped methods `rN_...` for the Test map.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def pad(n: int) -> str:
    return f"{n:02d}"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


MARK_RE = re.compile(r"^(?P<ind>[ \t]*)//@TODO (?P<label>[^|\n]+?) \| (?P<text>[^\n]+)\n(?P<body>.*?)^[ \t]*//@END[ \t]*\n", re.S | re.M)


def todo_items(src: str) -> list[tuple[str, str]]:
    return [(m.group("label").strip(), m.group("text").strip()) for m in MARK_RE.finditer(src)]


def render_java(src: str, dd: str, tt: str, stub: bool) -> str:
    src = src.replace("@PKG@", f"com.javaprep.day{dd}.task{tt}")
    tag = f"TODO(Day{dd}-task{tt})"

    def repl(m: re.Match) -> str:
        if not stub:
            return m.group("body")
        ind = m.group("ind")
        text = m.group("text").strip().replace('"', "'")
        return (
            f"{ind}// {tag}: {text}\n"
            f'{ind}throw new UnsupportedOperationException("{tag}: {m.group("label").strip().replace(chr(34), chr(39))}");\n'
        )

    return MARK_RE.sub(repl, src)


def pom_xml(dd: str, tt: str, slug: str, mockito: bool, jacoco: bool) -> str:
    extra_deps = ""
    if mockito:
        extra_deps = """    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-core</artifactId>
      <version>${mockito.version}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-junit-jupiter</artifactId>
      <version>${mockito.version}</version>
      <scope>test</scope>
    </dependency>
"""
    mock_prop = "    <mockito.version>5.14.2</mockito.version>\n" if mockito else ""
    jacoco_plugin = ""
    if jacoco:
        jacoco_plugin = """      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.12</version>
        <executions>
          <execution>
            <goals>
              <goal>prepare-agent</goal>
            </goals>
          </execution>
          <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
              <goal>report</goal>
            </goals>
          </execution>
        </executions>
      </plugin>
"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.javaprep.day{dd}</groupId>
  <artifactId>task-{tt}-{slug}</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <name>Day {dd} - task-{tt}-{slug}</name>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>21</maven.compiler.release>
    <junit.version>5.11.4</junit.version>
    <assertj.version>3.27.3</assertj.version>
{mock_prop}  </properties>
  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>${{junit.version}}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.assertj</groupId>
      <artifactId>assertj-core</artifactId>
      <version>${{assertj.version}}</version>
      <scope>test</scope>
    </dependency>
{extra_deps}  </dependencies>
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
{jacoco_plugin}    </plugins>
  </build>
</project>
"""


def bullets(items) -> str:
    return "\n".join(f"- {i}" for i in items)


def numbered(items) -> str:
    return "\n".join(f"{n}. {i}" for n, i in enumerate(items, 1))


# ---------------------------------------------------------------- theory
def render_theory(d: dict) -> str:
    xx = pad(d["num"])
    tasks = ", ".join(f"`task-{pad(i)}-{t['slug']}`" for i, t in enumerate(d["tasks"], 1))
    out = [
        f"# Day {xx} — {d['title']}",
        "",
        f"**Phase:** Core Java  ",
        f"**Primary theme:** {d['theme']}  ",
        f"**Estimated study time:** {d.get('time', '2–3 h theory + 3–5 h tasks')}  ",
        f"**Related tasks:** {tasks}  ",
        f"**Instruction alignment:** Maps to the Day {xx} entry of the 50-day topic map (`course-generation-instructions/04`).  ",
        "**Java / Spring versions:** Java 21 (no Spring today)",
        "",
        "## Overview",
        "",
        d["overview"].strip(),
        "",
        "## Day roadmap",
        "",
        numbered([s["title"] for s in d["sections"]] + ["Interview angles", "Common mistakes & debugging", "Further reading, glossary, answers"]),
        "",
    ]
    answers = []
    for n, s in enumerate(d["sections"], 1):
        out += [f"### {s['title']}", "", "#### What it is", "", s["what"].strip(), "", "#### Why it exists / why it matters", "", s["why"].strip(), ""]
        out += ["#### Pros and cons", "", "**Pros**", "", bullets(s["pros"]), "", "**Cons / tradeoffs**", "", bullets(s["cons"]), ""]
        out += ["#### What happens without it / when misused", "", s["without"].strip(), ""]
        out += ["#### Syntax and rules", "", s["syntax"].strip(), ""]
        out += ["#### Examples", ""]
        for k, (cap, code) in enumerate(s["examples"], 1):
            out += [f"**Example {n}.{k} — {cap}**", "", "```java", code.strip("\n"), "```", ""]
        out += ["#### Quick checks", ""]
        for k, (q, a) in enumerate(s["quick"], 1):
            out.append(f"{k}. {q}")
            answers.append((f"{n}.{k}", q, a))
        out.append("")
    out += ["## Interview angles", ""]
    for q, a in d["interview"]:
        out += [f"**Q: {q}**", "", a, ""]
    out += ["## Common mistakes & debugging", "", bullets(d["mistakes"]), "", "## Further reading", "", bullets(d["reading"]), ""]
    out += ["## Glossary", "", "| Term | Meaning |", "|------|---------|"]
    out += [f"| {t} | {m} |" for t, m in d["glossary"]]
    out += ["", "## Answers", "", "Answers to every **Quick check** above (numbered `section.question`).", ""]
    for num, q, a in answers:
        out += [f"- **{num}** — {q}  ", f"  {a}", ""]
    return "\n".join(out)


def render_readme(d: dict) -> str:
    xx = pad(d["num"])
    rows = "\n".join(
        f"| {i} | `task-{pad(i)}-{t['slug']}` | Plain Java | `mvn test` |" for i, t in enumerate(d["tasks"], 1)
    )
    return f"""# Day {xx} — {d['title']}

## Learning objectives

{bullets(d['objectives'])}

## Prerequisites

{bullets(d['prereqs'])}

## How to use this folder

1. Read [`DAY-{xx}-THEORY-AND-REFERENCE.md`](DAY-{xx}-THEORY-AND-REFERENCE.md) first.
2. Open each task folder under `practical-tasks/` as its own Maven project in IntelliJ.
3. Run `mvn test` (**red**), implement the `TODO(Day{xx}-taskYY)` stubs, run `mvn test` again until **green**.
4. Do not edit tests, `TASK_INSTRUCTIONS.md`, or `EVALUATION_CRITERIA.md`.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
{rows}

**Estimated time:** {d.get('time', '2–3 h theory + 3–5 h tasks')}  
**Phase:** Core Java
"""


# ---------------------------------------------------------------- task docs
def test_map(test_srcs: dict[str, str]):
    groups: dict[int, list[str]] = {}
    count = 0
    for src in test_srcs.values():
        for m in re.finditer(r"@(?:Test|ParameterizedTest)\b[^\n]*\n(?:\s*@[^\n]*\n)*\s*(?:public\s+)?void\s+(\w+)\s*\(", src):
            name = m.group(1)
            count += 1
            r = re.match(r"r(\d+)_", name)
            groups.setdefault(int(r.group(1)) if r else 0, []).append(name)
    return groups, count


def render_instructions(d: dict, t: dict, i: int) -> str:
    dd, tt = pad(d["num"]), pad(i)
    main_files = "\n".join(
        f"| `src/main/java/com/javaprep/day{dd}/task{tt}/{n}` | {'Stubs with TODOs' if todo_items(s) else 'Provided type (no changes needed)'} |"
        for n, s in t["main"].items()
    )
    test_files = "\n".join(
        f"| `src/test/java/com/javaprep/day{dd}/task{tt}/{n}` | Specification tests (read-only) |" for n in t["test"]
    )
    todo_rows = []
    for n, s in t["main"].items():
        for label, text in todo_items(s):
            todo_rows.append(f"| `{n}` — `{label}` | `TODO(Day{dd}-task{tt})` | {text} |")
    groups, count = test_map(t["test"])
    tm_rows = []
    for r in sorted(groups):
        if r == 0:
            continue
        tm_rows.append(f"| {r} | {', '.join('`' + x + '`' for x in groups[r])} |")
    if 0 in groups:
        tm_rows.append(f"| general | {', '.join('`' + x + '`' for x in groups[0])} |")
    cls = t["class_name"]
    hints = "\n\n".join(f"<details><summary>Hint {n}</summary>\n\n{h}\n\n</details>" for n, h in enumerate(t["hints"], 1))
    return f"""# Task {i} — {t['title']}

**Day:** {dd} · **Task ID:** Day{dd}-task{tt} · **Type:** Plain Java · **Difficulty:** {t['difficulty']}

## Summary

{t['summary'].strip()}

## Learning goals

{bullets(t['goals'])}

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit {'5.11.4'}, AssertJ 3.27.3{', Mockito 5.14.2' if t.get('mockito') else ''}) |
{main_files}
{test_files}

## Prerequisites

{bullets((t.get('prereqs') or ['Day ' + dd + ' theory file read']))}

## What you will implement

{numbered(t['implement'])}

## Constraints

{bullets(t['constraints'] + ['Java 21; no Docker; no external services; no Lombok'])}

## Step-by-step guidance

{numbered(t['steps'])}

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

At the start roughly **{count} tests** run and fail (stubs throw `UnsupportedOperationException` whose message starts with `TODO(Day{dd}-task{tt})`).

### Run one test class

```bash
mvn -Dtest={cls}Test test
```

### Manual checks

{chr(10).join('- [ ] ' + c for c in t['manual'])}

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
{chr(10).join(todo_rows)}

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
{chr(10).join(tm_rows)}

## Edge cases to handle

{bullets(t['edges'])}

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day {dd}: {t['title']}`

## Hints (optional)

{hints}
"""


def render_eval(d: dict, t: dict, i: int) -> str:
    dd, tt = pad(d["num"]), pad(i)
    files = ", ".join(f"`{n}`" for n in t["main"] if todo_items(t["main"][n]))
    return f"""# Evaluation Criteria — Day {dd} — Task {tt} — {t['title']}

## Scope

Graded: the behavior and quality of the implementation in {files} against the provided tests and the requirements in `TASK_INSTRUCTIONS.md`. Out of scope: build tooling changes, formatting of provided tests, anything outside `src/main/java`.

## Weighting (100 points unless the instructor overrides)

| Category | Points | Description |
|----------|-------:|-------------|
| Automated tests (`mvn test`) | 40 | Fraction of tests passing; no skipped/@Disabled tests |
| Requirements coverage | 25 | Each "What you will implement" bullet satisfied |
| Code quality | 20 | Naming, structure, idiomatic Java 21, no duplication, correct use of the day's concepts |
| Robustness & safety | 10 | Edge cases, null/validation handling, exceptions, thread-safety/security where relevant |
| Readability & process | 5 | Clear commits, formatting, sensible comments |

## Pass / fail gates (automatic fail if violated)

- Tests modified/disabled to force a pass
- Hard-coded secrets
- Forbidden APIs from Constraints used
- Project does not compile

## Detailed rubric

### Automated tests

- Full marks only when every test passes with no `@Disabled` and no edits to test files.
- Partial credit is proportional to passing tests; a compile failure scores 0 in this category.

### Requirements coverage

{bullets(t['rubric_requirements'])}

### Code quality

{bullets(t['rubric_quality'])}

### Robustness & safety

{bullets(t['rubric_robust'])}

### Day-specific checks

{bullets(t['rubric_day'])}

## Evidence the grader should collect

- `mvn test` summary (tests run / failures / errors / skipped)
- Optional: `git diff --stat`{', JaCoCo summary (`target/site/jacoco/index.html`)' if d['num'] >= 23 else ''}

## AI-assisted grading prompt (optional)

```
You are grading Day {dd} Task {tt} ({t['title']}) for a graduate Java backend course.
Use the mvn test summary as the primary signal, then review {files} for the rubric items above.
Penalize hard-coded returns that merely satisfy tests, edits to tests, and forbidden APIs.
Leftover TODO comments are NOT penalized when the behavior is implemented.
Score /100 with the weights in EVALUATION_CRITERIA.md and list blocking issues first.
```
"""


# ---------------------------------------------------------------- driver
def generate_day(d: dict, out_root: Path, stub: bool = True, docs: bool = True) -> None:
    xx = pad(d["num"])
    day_dir = out_root / f"Day {xx}"
    if docs:
        write(day_dir / "README.md", render_readme(d))
        write(day_dir / f"DAY-{xx}-THEORY-AND-REFERENCE.md", render_theory(d))
    for i, t in enumerate(d["tasks"], 1):
        tt = pad(i)
        td = day_dir / "practical-tasks" / f"task-{tt}-{t['slug']}"
        write(td / "pom.xml", pom_xml(xx, tt, t["slug"], bool(t.get("mockito")), d["num"] == 23))
        if docs:
            write(td / "TASK_INSTRUCTIONS.md", render_instructions(d, t, i))
            write(td / "EVALUATION_CRITERIA.md", render_eval(d, t, i))
        pkg = f"com/javaprep/day{xx}/task{tt}"
        for n, s in t["main"].items():
            write(td / "src/main/java" / pkg / n, render_java(s, xx, tt, stub))
        for n, s in t["test"].items():
            write(td / "src/test/java" / pkg / n, render_java(s, xx, tt, False))
