# Day 03 — Tables

**Primary theme:** Accessible, structured HTML tables for tabular data  
**Estimated study time:** 1–2 hours theory + 3–6 hours tasks  
**Related tasks:** `task-01-simple-data-table`, `task-02-thead-tbody-scope-headers`, `task-03-colspan-rowspan-timetable`, `task-04-styled-pricing-table`  
**Instruction alignment:** Maps to *Tables* (`table`, `thead/tbody`, `tr/td/th`, colspan/rowspan, styling, accessibility cautions).

---

## Overview

Tables are the right tool when **two or more dimensions** of meaning intersect (row entity × column metric). They are the wrong tool when you only want columns visually—use CSS layout for that. Today you will learn the browser’s table model just enough to ship **screen-reader friendly** grids of real data and to avoid common pitfalls (`rowspan` mistakes, missing `th scope`, empty tables used for spacing).

---

## Day roadmap

1. [Table anatomy](#table-anatomy)
2. [Header cells and `scope`](#header-cells-and-scope)
3. [`colspan` and `rowspan`](#colspan-and-rowspan)
4. [Styling and accessibility cautions](#styling-and-accessibility-cautions)
5. [Common mistakes & debugging](#common-mistakes--debugging)
6. [Further reading](#further-reading)
7. [Glossary](#glossary)
8. [Answers (self-test)](#answers-self-test)

---

## Table anatomy

### What it is

A `<table>` wraps **rows** (`<tr>`) containing **cells** (`<td>` data, `<th>` headers). `<caption>` titles the table for everyone; `<thead>`, `<tbody>`, `<tfoot>` group rows for parsing, printing, and styling.

#### Why it exists / why it matters

Tables expose a grid semantics to assistive technologies. `<caption>` is announced as the table’s name; skipping it forces users to guess context from surrounding prose.

#### Pros and cons

- **Pros:** Precise alignment of numeric columns; excellent for comparisons.
- **Pros:** `tfoot` repeats on printed pages in many browsers for totals.
- **Cons:** Wide tables overflow small screens—plan responsive strategies (Day 13–14 revisit).
- **Cons:** Deeply nested tables (layout tables) are maintenance nightmares.

#### What happens without it / when misused

- Missing `<thead>` for header rows makes styling and scripting brittle.
- Using tables for **page layout** harms accessibility and responsive reflow.

#### Syntax and rules

```html
<table>
  <caption>Quarterly totals</caption>
  <thead>
    <tr><th scope="col">Team</th><th scope="col">Q1</th></tr>
  </thead>
  <tbody>
    <tr><th scope="row">A</th><td>12</td></tr>
  </tbody>
</table>
```

#### Examples

**Tiny — minimal**

```html
<table>
  <tr><td>1</td><td>2</td></tr>
</table>
```

**Tiny — caption**

```html
<table>
  <caption>Lab scores</caption>
  <tr><th scope="col">Lab</th><th scope="col">Points</th></tr>
  <tr><td>01</td><td>10</td></tr>
</table>
```

**Medium — grouped**

```html
<table>
  <caption>Inventory</caption>
  <thead>
    <tr><th scope="col">SKU</th><th scope="col">Qty</th></tr>
  </thead>
  <tbody>
    <tr><td>A-100</td><td>3</td></tr>
    <tr><td>B-220</td><td>0</td></tr>
  </tbody>
  <tfoot>
    <tr><th scope="row">Total</th><td>3</td></tr>
  </tfoot>
</table>
```

#### Quick checks

1. Where does `<caption>` appear relative to `<thead>`?
2. Why avoid tables for overall page layout?
3. Name two child elements of `<tr>`.

---

## Header cells and `scope`

### What it is

`<th>` marks header cells. The `scope` attribute clarifies whether a header applies to a **column** (`col`), **row** (`row`), or groups (`colgroup`/`rowgroup`—advanced).

#### Why it exists / why it matters

Screen readers use `th` + `scope` to build spoken associations (“Q1, 12”) without the user memorizing column order.

#### Pros and cons

- **Pros:** Simple, widely supported association model.
- **Cons:** Complex irregular headers may need `headers`/`id` pairs (later topic).

#### What happens without it / when misused

- Visual bolding via `<td><strong>` loses table semantics—prefer `<th>`.

#### Syntax and rules

```html
<tr>
  <th scope="row">Alice</th>
  <td>92</td>
</tr>
```

#### Examples

**Tiny**

```html
<th scope="col">Date</th>
```

**Tiny**

```html
<th scope="row">Row label</th>
```

**Medium**

```html
<thead>
  <tr>
    <th scope="col">Student</th>
    <th scope="col">Attendance</th>
    <th scope="col">Project</th>
  </tr>
</thead>
```

#### Quick checks

1. When use `scope="row"` vs `scope="col"`?
2. Is `<th>` allowed in `<tbody>`?
3. What problem does `scope` primarily solve?

---

## `colspan` and `rowspan`

### What it is

`colspan` merges a cell across multiple columns; `rowspan` merges across rows. The **sum of columns per row** must still line up after merges.

#### Why it exists / why it matters

Schedules, pricing tiers, and merged labels use spans to mirror paper forms—when done correctly.

#### Pros and cons

- **Pros:** Expresses merged headers compactly.
- **Cons:** Easy to mis-count and break the grid (validator/cell inspector helps).
- **Cons:** Large span tables are harder to make responsive.

#### What happens without it / when misused

- Off-by-one `rowspan` leaves “holes” or shifted columns.

#### Syntax and rules

```html
<tr>
  <th colspan="2" scope="colgroup">Morning</th>
</tr>
```

#### Examples

**Tiny — colspan**

```html
<tr>
  <td colspan="2">Merged across two columns</td>
</tr>
```

**Tiny — rowspan**

```html
<tr>
  <th rowspan="2" scope="row">Team A</th>
  <td>Game 1</td>
</tr>
<tr>
  <td>Game 2</td>
</tr>
```

**Medium — timetable corner**

```html
<table>
  <tr>
    <td></td>
    <th scope="col">09:00</th>
    <th scope="col">10:00</th>
  </tr>
  <tr>
    <th scope="row">Mon</th>
    <td colspan="2">Workshop</td>
  </tr>
</table>
```

#### Quick checks

1. If a row has three `<td>` and one uses `colspan="2"`, how many grid columns must exist?
2. Why test tables in the W3C validator after edits?
3. When might `rowspan` harm small-screen layouts?

---

## Styling and accessibility cautions

### What it is

`border-collapse: collapse`, `border-spacing`, zebra striping via `:nth-child`, and `text-align: end` for numbers improve readability. `role="presentation"` is rarely correct for real data tables—avoid stripping semantics.

#### Why it exists / why it matters

Dense tables fatigue readers; alignment helps scan columns; focus styles matter when cells include controls (Day 04).

#### Pros and cons

- **Pros:** Subtle striping improves row tracking.
- **Cons:** Ultra-low contrast borders fail WCAG.

#### What happens without it / when misused

- `display: block` hacks on `tr` can destroy table semantics—use with extreme care.

#### Syntax and rules

```css
table {
  border-collapse: collapse;
  width: 100%;
}
th,
td {
  border: 1px solid #cbd5e1;
  padding: 0.5rem;
}
```

#### Examples

**Tiny**

```css
caption {
  caption-side: top;
  text-align: start;
  font-weight: 600;
}
```

**Tiny**

```css
tbody tr:nth-child(even) {
  background: #f8fafc;
}
```

**Medium**

```css
th[scope="col"] {
  border-bottom: 2px solid #0f172a;
}
td:nth-child(n + 2) {
  text-align: end;
  font-variant-numeric: tabular-nums;
}
```

#### Quick checks

1. Why prefer `border-collapse: collapse` in many designs?
2. What does `font-variant-numeric: tabular-nums` help with?
3. When is zebra striping more harmful than helpful?

---

## Common mistakes & debugging

- Columns “don’t line up”: draw the grid on paper before coding spans.
- Forgetting `<caption>`: add a concise human-readable title.
- Numeric alignment: right-align or tabular numbers for money columns.

---

## Further reading

- [MDN — `<table>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/table)
- [MDN — Table accessibility](https://developer.mozilla.org/en-US/docs/Learn/HTML/Tables/Advanced)
- [W3C Nu Html Checker](https://validator.w3.org/nu/)

---

## Glossary

| Term | Meaning |
|------|---------|
| **`scope`** | Associates `th` cells with a row or column. |
| **`colspan` / `rowspan`** | Cell merge attributes spanning columns/rows. |

---

## Answers (self-test)

**Anatomy**

1. First child of `<table>` if present, before `<thead>` in typical patterns (spec allows various orders but caption first is common practice).
2. Layout tables break semantic navigation and responsive reflow patterns.
3. `<th>` or `<td>` (and script/template elements in advanced cases).

**Headers**

1. Row header labels a row; column header labels a column.
2. Yes, for row headers in body rows.
3. Screen reader association between headers and data cells.

**Spans**

1. The row still occupies the full column count of the table—here effectively two logical columns covered by one cell plus one other cell depends on layout; student should reason about total width—answer pattern: total columns = sum of colspans in row.
2. Catches malformed row/column counts.
3. Tall merged cells can reduce visible context on small screens.

**Styling**

1. Shared borders without double-thick lines between cells.
2. Aligns digits for money columns vertically.
3. When stripes distract from heatmaps or dense sparkline content—context dependent.
