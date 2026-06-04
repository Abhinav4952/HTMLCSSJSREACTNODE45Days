# Evaluation Criteria — Day 44 — Task 1 — Mongoose connect + health

## Scope

`src/db/mongoose.js` implementation; provided files for env + server wiring should remain coherent.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 55 | `npm test` passes (in-memory Mongo). |
| Configuration | 25 | Uses `MONGODB_URI` + `MONGODB_DB_NAME` / default `course-node-45`. |
| Hygiene | 20 | No secrets in repo; clear error if URI missing for `npm start`. |

## Pass / fail gates

- `npm test` fails.
- Real Atlas password committed in `.env` / source.

## AI grading prompt

Confirm `connectMongo` calls `mongoose.connect` with `{ dbName }` from env, `/health` reports `connected` after successful connect, and `.env` is absent from git.
