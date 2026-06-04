# Evaluation Criteria — Day 01 — Task 01 — Minimal Valid HTML5 Document

## Scope

Graded: `index.html` structure and metadata requested in `TASK_INSTRUCTIONS.md`.  
Out of scope: visual design, CSS frameworks, JavaScript.

## Weighting (100 points unless instructor overrides)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 45 | Doctype, `lang`, charset, viewport, title, body content present and valid |
| Requirements coverage | 30 | Every TODO item satisfied; no stale TODO comments left misleadingly |
| Code quality | 15 | Consistent indentation; sensible title wording |
| Docs / readability | 10 | Optional short HTML comment block documenting student id is OK; no noisy debug markup |

## Pass / fail gates (automatic fail if violated)

- `<!DOCTYPE html>` missing or not first.
- Missing `<meta charset="utf-8">` or charset not in `<head>`.
- File does not open in a browser without fatal parse issues caused by candidate edits.

## Detailed rubric

### Correctness

- **45/45:** All gates pass; `lang` appropriate; viewport meta present and sensible.
- **30–44:** One non-critical omission (e.g. weak title) with otherwise valid structure.
- **Below 30:** Major structural errors (e.g. `<head>` after `<body>`).

### Edge cases

- Charset present but not UTF-8 declared—flag for discussion unless instructor allows legacy encodings.

### Security / privacy (if applicable)

- No external tracking scripts required; if added voluntarily, must not include API keys.

### UX / accessibility (if applicable)

- Meaningful `<title>`; language attribute set.

## Evidence the grader should collect

- Note browser used.
- Optional: W3C Nu Html Checker link or screenshot if instructor requires validation.

## AI grading prompt (paste into your grader)

You are evaluating a graduate-level HTML assignment. Use only observable criteria in this file. Check `index.html` for: `<!DOCTYPE html>` first line; `html[lang]`; utf-8 charset meta early in head; viewport meta; descriptive title; body has visible greeting. Return Pass/Fail, score table, blocking issues, suggestions.
