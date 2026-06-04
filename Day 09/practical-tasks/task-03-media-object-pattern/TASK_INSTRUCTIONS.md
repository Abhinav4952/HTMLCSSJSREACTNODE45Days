# Task 03 — Media Object Pattern

## Summary

Implement a reusable **media object** row: avatar square + multi-line text, aligned to the top, robust when text wraps.

## Acceptance

- Avatar does not shrink when text grows.
- Text column uses `min-width: 0` (or equivalent) so long words can wrap instead of forcing horizontal overflow.

## `TODO` map

| TODO | Done means |
|------|------------|
| `.mo` | flex row + gap |
| `.mo__media` | fixed square |
| `.mo__body` | flex:1 and min-width:0 |
