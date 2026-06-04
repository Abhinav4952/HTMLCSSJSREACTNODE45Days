# Task 1 — ESM, `import.meta.url`, and `path`

## Summary

Implement small helpers that derive **`__dirname`-equivalent paths** in **ES modules** using `fileURLToPath` and `path.join`.

## Learning goals

- Convert a `file:` URL string to an absolute filesystem path safely.
- Build paths relative to **the current module**, not `process.cwd()`.

## Provided files

| File | Purpose |
|------|---------|
| `src/pathLab.js` | Your implementations (`TODO`). |
| `tests/pathLab.test.js` | Vitest checks (read-only). |
| `fixtures/hello.txt` | Sample file for path resolution. |

## Prerequisites

- Node **18+** installed.

## What you will implement

1. `moduleDirname(importMetaUrl)` returns the directory containing the module identified by a `file:` URL string.
2. `joinRelativeToModule(importMetaUrl, ...segments)` joins additional path segments after that directory.

## Constraints

- Use **`node:url`** and **`node:path`** built-ins only (no third-party path libs).
- Only edit files that contain `TODO(Day41-task01)`.

## Step-by-step guidance

1. Read `fileURLToPath` docs; confirm it accepts `import.meta.url`-style strings.
2. Implement `moduleDirname` as `path.dirname(fileURLToPath(importMetaUrl))`.
3. Implement `joinRelativeToModule` using `path.join(moduleDirname(importMetaUrl), ...segments)`.

## How to run and verify

### Install dependencies

```bash
cd "Day 41/practical-tasks/task-01-esm-path-and-url-basics"
npm install
```

### Run tests

```bash
npm test
```

Tests are expected to **fail** until both `TODO`s are implemented.

## `TODO` map

| Location | Done means |
|----------|-------------|
| `src/pathLab.js` — `moduleDirname` | Returns correct absolute directory for a `file:` URL. |
| `src/pathLab.js` — `joinRelativeToModule` | Joins segments relative to that directory. |

## Submission checklist (Git)

- [ ] Only intentional files changed; no secrets.
- [ ] `npm test` passes locally.

## Hints

<details>
<summary>Spoiler: canonical snippet</summary>

```js
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const dir = path.dirname(fileURLToPath(importMetaUrl));
```

</details>
