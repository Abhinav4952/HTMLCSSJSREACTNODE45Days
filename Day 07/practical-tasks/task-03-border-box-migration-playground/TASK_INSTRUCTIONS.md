# Task 03 — `border-box` Migration Playground

## Summary

You inherit a layout written in **`content-box` thinking** (widths that accidentally include padding twice in the author’s head). Migrate the layout to a **consistent `border-box` model** and fix overflow.

## Learning goals

- Normalize `box-sizing` and reconcile `width: 100%` + padding patterns.

## Provided files

- `index.html`, `styles/main.css`

## What you will implement

Complete `TODO(Day07-task03)` markers.

## Manual checks

- [ ] No horizontal scrollbar at 360px for the card row (unless instructor allows).

## `TODO` map

| TODO | Done means |
|------|------------|
| global | universal border-box |
| cards | three `.tile` equal visual widths in row without overflow |
| legacy | remove/replace conflicting rules in `.legacy` block |
