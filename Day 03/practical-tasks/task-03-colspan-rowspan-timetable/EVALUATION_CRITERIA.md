# Evaluation Criteria — Day 03 — Task 03 — Colspan/Rowspan Timetable

## Scope

Graded: correctness of span geometry + semantics.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | Grid lines up; rowspan/colspan valid |
| Requirements coverage | 25 | Minimum size met |
| Code quality | 20 | Readable header organization |
| Readability | 10 | Caption + labels |

## Pass / fail gates

- Broken table layout (ragged rows) due to span miscount.
- No `rowspan` or no `colspan`.

## AI grading prompt

Inspect table for presence of colspan and rowspan, caption, th scopes where appropriate, and visually consistent columns.
