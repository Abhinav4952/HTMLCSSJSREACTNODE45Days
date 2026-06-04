# Evaluation Criteria — Day 43 — Task 4 — Issuer + audience claims

## Scope

`src/app.js` token mint + verify.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 60 | Tests pass including negative audience case. |
| Claim discipline | 30 | Uses `issuer`/`audience` on sign + verify. |
| Security notes | 10 | No secrets logged; `.env` not committed. |

## Pass / fail gates

- Accepts arbitrary JWT without audience check.
- `npm test` fails.

## AI grading prompt

Verify `jwt.verify` uses audience/issuer options matching constants and returns scope claim.
