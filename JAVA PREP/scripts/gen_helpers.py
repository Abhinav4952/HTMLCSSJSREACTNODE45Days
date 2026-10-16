"""Small constructors that keep day data files compact."""
from __future__ import annotations


def sec(title, what, why, pros, cons, without, syntax, examples, quick):
    return dict(title=title, what=what, why=why, pros=pros, cons=cons, without=without,
                syntax=syntax, examples=examples, quick=quick)


def task(slug, title, difficulty, cls, summary, implement, edges, main, test, hints,
         day_checks, goals=None, constraints=None, mockito=False, prereqs=None):
    return dict(
        slug=slug, title=title, difficulty=difficulty, class_name=cls, summary=summary,
        goals=goals or ["Practice today's theory with a focused, testable API",
                        "Drive the implementation from failing JUnit 5 + AssertJ tests",
                        "Replace each `UnsupportedOperationException` stub with real behavior"],
        implement=implement, edges=edges, main=main, test=test, hints=hints,
        constraints=constraints or ["Do not edit the tests; do not hard-code expected values"],
        steps=[
            "Run `mvn test` and confirm every failure mentions `TODO(Day..-task..)` (red).",
            "Read the test class: it is the specification. Note the `rN_` prefixes map to the numbered requirements.",
            "Implement one TODO at a time, re-running `mvn -Dtest=" + cls + "Test test` after each.",
            "Refactor for clarity once green; re-run the full suite.",
            "Commit with the message given in the submission checklist.",
        ],
        manual=["No `UnsupportedOperationException` stubs remain on any path exercised by the tests",
                "Each public method has a one-line comment or self-explanatory name",
                "You can explain every line to a reviewer without referring to the tests"],
        rubric_requirements=[f"Requirement {n}: {r}" for n, r in enumerate(implement, 1)],
        rubric_quality=["Names express intent; methods stay short and single-purpose",
                        "No copy-pasted branches; idiomatic Java 21 (e.g. `List.of`, `var` where it helps, records where given)",
                        "No unnecessary raw types, casts, or `@SuppressWarnings` without a comment"],
        rubric_robust=edges[:4] if len(edges) >= 2 else edges,
        rubric_day=day_checks,
        mockito=mockito, prereqs=prereqs,
    )
