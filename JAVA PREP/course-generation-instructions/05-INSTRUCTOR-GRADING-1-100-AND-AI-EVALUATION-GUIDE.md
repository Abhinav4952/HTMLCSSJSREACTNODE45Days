# 05 — Instructor Grading (1–100) and AI Evaluation Guide

**Instruction set version:** `1.0.0`
**Use with:** `03` (per-task `EVALUATION_CRITERIA.md` for candidates) and `04` (task design).

This document is for **instructors** and **AI grading agents**. It standardizes how to assign **1–100** scores for Java backend prep work (plain Java, SQL/JDBC, Spring Boot, microservices, capstone) and how to give constructive feedback to graduate-level learners preparing for backend roles.

---

## 1. Where the numeric rubric lives

- **Candidate-facing:** each task’s `EVALUATION_CRITERIA.md` (see `03` §8).
- **Instructor/AI-only (optional):** `Day XX/INSTRUCTOR_GRADING_1-100.md`, one file per day, summarizing per-task `/25` slices (four tasks → `/100` day total). With three tasks, use `/33`, `/33`, `/34`.

Candidates focus on `TASK_INSTRUCTIONS.md` + `EVALUATION_CRITERIA.md`. Instructors/AI use the day file plus this guide so learners are not distracted by `/100` in every task folder. If a per-task numeric sheet exists, it must not contradict the day file without an instructor note.

---

## 2. Grader mindset (non-negotiable tone)

- **Reward:** meeting task instructions and learning goals; correct use of the day’s concepts; clear naming; evidence of debugging and understanding.
- **Do not penalize heavily for:** missing enterprise extras (hexagonal architecture, MapStruct, full CI) unless required by the task.
- **Penalize meaningfully for:** skipped stated requirements; wrong concept use (e.g. `==` for string equality, entity returned from controller after Day 31, plaintext passwords, SQL concatenation); tests modified/disabled to pass; hard-coded returns that only satisfy visible tests; copying without understanding when evidence exists.
- **Do NOT deduct for leftover `TODO` comments** when the required behavior is implemented. Comments are cosmetic. A `TODO` marking genuinely unimplemented behavior is scored under **Requirements coverage** for the missing work, not for the comment.
- **Default feedback style:** "what works → smallest next step to level up", citing the day’s theory section or official docs (Javadoc, Spring reference, PostgreSQL docs).

---

## 3. Default 100-point model

Use this model per task unless the task’s `EVALUATION_CRITERIA.md` overrides weights.

| Category | Points | Instructor notes |
|----------|-------:|------------------|
| **Automated tests (`mvn test`)** | **40** | Score ≈ proportion of tests passing. Skipped/`@Disabled` tests count as failing. Tests changed by the candidate → see gates. |
| **Requirements coverage** | **25** | Map each bullet in "What you will implement" to yes / partial / no. |
| **Code quality** | **20** | Idiomatic Java 21, correct concept use, naming, single responsibility, no duplication, proper encapsulation/immutability, sensible layering. |
| **Robustness & safety** | **10** | Null/boundary handling, correct exceptions, resource closing, thread-safety (Days 20–22, 42), SQL injection safety (Day 27+), validation/auth correctness (Days 31+). |
| **Readability & process** | **5** | Formatting, meaningful commits, no `target/`/IDE files committed, README/notes where requested. |

### 3.1 Phase-specific adjustments

| Phase | Adjustment |
|-------|------------|
| **Core Java (01–24)** | Default model. Add day-specific checks (e.g. Day 05: uses `equals`, not `==`; Day 14: no `ConcurrentModificationException`; Day 20: no unsynchronized shared mutation). |
| **SQL/JDBC (25–27)** | Tests **30**, Requirements **25**, **SQL/DAO quality 25** (constraints, normalization, parameter binding, resource handling), Robustness **15**, Readability & process **5**. PostgreSQL-only features not testable on H2 are graded by rubric review (move those points into SQL/DAO quality). |
| **Spring Boot (28–42)** | Default model; Code quality includes layering, constructor injection, DTO use, correct status codes, no entity leakage. Robustness includes validation, `ProblemDetail` consistency, transaction boundaries. |
| **Security tasks (37–38, 47–48)** | Use Tests 30 / Requirements 25 / Code quality 15 / **Security correctness 25** / Readability & process 5. Security correctness covers BCrypt, token validation, 401 vs 403, no secret/log leaks. |
| **Microservices & Kafka (43–46)** | Tests 35, Requirements 25, Code quality 15, **Resilience/messaging correctness 20** (timeouts, idempotency, DLT, bounded waits), Readability 5. |
| **Capstone (47–48)** | Use the Security-task weights plus ownership/pagination checks; the day total may be reweighted by the instructor. |
| **Days 24, 49, 50 (review/integration)** | Default model; for timed tasks (Day 50) score partial credit by passing tests at the time limit and apply a short **explain-your-solution** viva as optional bonus (does not exceed 100). |

Whenever weights are adjusted, the adjusted table must be printed in the day’s `INSTRUCTOR_GRADING_1-100.md` and mirrored in the task’s `EVALUATION_CRITERIA.md`.

---

## 4. Translating categories to a single 1–100 score

### 4.1 Day-level (recommended)

1. Score each task out of **25** (four tasks): scale each category proportionally. For the default model use **10 + 6 + 5 + 2.5 + 1.5 = 25** (round to nearest 0.5).
2. Sum tasks → **Day total /100**; round to the nearest integer.

### 4.2 Task-only reporting

Score categories at full weight (sum 100) and report per task.

### 4.3 Test-based scoring detail

```text
testScore = 40 × (passingTests / totalTests)
```

- Count only tests present in the **original** test files. If the candidate edited tests, re-run the **original** tests from the instructor copy.
- If the build does not compile → tests score 0 and the "compiles" gate fails (Section 6).

Do **not** invent sub-points outside the tables without recording them in the Notes column.

---

## 5. Suggested banding (cohort-adjustable)

Apply to **Day total /100**.

| Total | Label | Typical meaning |
|------:|-------|-----------------|
| **90–100** | **Excellent** | All requirements met; clean idiomatic code; demonstrates understanding beyond the checklist. |
| **80–89** | **Strong** | Requirements met; minor gaps in robustness/style. |
| **70–79** | **Satisfactory** | Core requirements met; several small issues or one moderate gap. |
| **60–69** | **Needs revision** | Important requirement missing or a wrong pattern; salvageable with targeted fixes. |
| **< 60** | **Incomplete / redo** | Multiple requirements missing, broken build, or academic-integrity concerns. |

Your program sets official pass marks.

---

## 6. Pass / fail gates (hard stops)

Regardless of numeric score, flag **automatic redo** when:

- The project **does not compile** (`mvn test-compile` fails).
- Tests were **edited, deleted, or `@Disabled`** to force a pass (unless the task allowed edits).
- **Hard-coded outputs** keyed to test inputs rather than real logic.
- **Secrets** (real tokens, keys, passwords, connection strings) committed.
- A **forbidden API/library** from the task Constraints is used (e.g. Lombok, streams on a "no streams" task, Spring in Days 01–27).
- Security tasks: **plaintext password storage**, signature verification disabled, or JWT accepted without expiry check.
- JDBC tasks: **string-concatenated SQL** with user input in the "safe" implementation.
- **Academic dishonesty** evidence → follow institutional policy (separate from the numeric rubric).

---

## 7. Feedback candidates will actually use

Order:

1. **Recognition** — what clearly meets the brief (file + behavior).
2. **Priority fixes** — max **3**, ordered by impact.
3. **Stretch (optional)** — one "level up" tied to interviews/employability (e.g. "explain why `HashMap` resize preserves order within buckets", "add an index and show `EXPLAIN` before/after").

Prefer: "For the next iteration, try …", "This meets the lab; in production you might also …".
Avoid: "trivially wrong", "obviously bad".

---

## 8. AI-assisted grading workflow

1. Open `Day XX/INSTRUCTOR_GRADING_1-100.md` (if present), each task’s `TASK_INSTRUCTIONS.md`, and `EVALUATION_CRITERIA.md`.
2. Collect evidence:
   - `mvn -q test` output (tests run / failures / errors / skipped) — run the **instructor copy** of tests.
   - `git diff --stat` against the starter, and `git status` (check for `target/`, `.idea/`).
   - Source files under `src/main/java`.
   - For Spring tasks: manual `curl` transcripts if the rubric requires.
3. Check **gates** (Section 6) first.
4. Score categories; sum.
5. Output:
   - **Day total /100** with per-task subscores
   - **Band** and pass/needs-revision recommendation
   - **3 prioritized improvements** (≤ 2 sentences each)
   - **Hard-fail issues** listed separately

### 8.1 Paste-ready AI prompt

```text
You are grading a Java 21 backend prep lab (Maven, JUnit 5, AssertJ; Spring Boot 4 from Day 28).
Use ONLY observable evidence: submitted files, mvn test output, and git diff. Do not assume unstated tooling.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md.
Use Day XX/INSTRUCTOR_GRADING_1-100.md (if present) and each task's EVALUATION_CRITERIA.md for weights.

Rules:
- Run the ORIGINAL tests; if candidate tests were modified/disabled, flag a hard fail.
- Do NOT deduct for leftover TODO comments when behavior is implemented; score missing behavior under Requirements coverage.
- Check for hard-coded returns tailored to test inputs.
- Check concept correctness for the day (e.g. equals vs ==, immutability, transactions, 401 vs 403).

Output:
1) Day total /100 with per-task subscores (tests / requirements / quality / robustness / process)
2) Band (Excellent / Strong / Satisfactory / Needs revision / Incomplete) per guide §5
3) Three concrete improvements, each <= 2 sentences
4) Separate list of hard-fail issues, if any
Tone: constructive, specific, recognition first.
```

### 8.2 Per-task grader checklist

- [ ] Compiles; `mvn test` executed from the task root.
- [ ] Original tests untouched (compare against starter).
- [ ] Test counts recorded (run/fail/error/skip).
- [ ] No `target/`, `.idea/`, `*.iml`, `.env` committed.
- [ ] Day-specific concept checks completed.
- [ ] No secrets; no forbidden APIs.
- [ ] Feedback follows recognition → fixes → stretch.

---

## 9. Day-specific check examples (extend per day)

| Day | Check |
|----:|-------|
| 05 | String comparison uses `equals`; builder used in loops |
| 08 | Class is truly immutable (final fields, defensive copies) |
| 09 | `equals`/`hashCode` consistent and symmetric |
| 11 | Resources closed via try-with-resources; cause preserved |
| 15 | No reliance on `HashMap` iteration order |
| 17–18 | No side effects inside stream lambdas; correct collector choice |
| 20–21 | Shared state protected; no sleep-based sync |
| 27 | `PreparedStatement` for all user input; connections closed/pooled |
| 31 | Entities not exposed; validation messages returned as `ProblemDetail` |
| 35 | N+1 eliminated (query count asserted); `@Version` conflict handled |
| 38 | 401 for missing/invalid token; 403 for forbidden role/owner |
| 43 | Fallback executes; circuit opens after configured failures |
| 46 | Duplicate events processed exactly once; poison message lands in DLT |
| 48 | Ownership enforced; pagination bounds validated |

---

## 10. Extending to post-Day-50 projects

StayEasy, PayFlow, and PeopleHub are graded at **milestone** granularity: use the same 1–100 model with a rubric added to each project spec (feature checklist, test suite, security review, README quality). Keep candidate-facing criteria aligned with what is graded numerically.

---

## 11. Changelog

| Version | Date | Notes |
|---------|------|-------|
| `1.0.0` | 2026-10-16 | Initial Java grading guide: default 100-point model, phase adjustments, gates, AI prompt, no-TODO-penalty policy. |
