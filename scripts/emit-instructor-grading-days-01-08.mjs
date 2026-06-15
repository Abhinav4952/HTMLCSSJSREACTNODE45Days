/**
 * Generates one INSTRUCTOR_GRADING_1-100.md per Day 01–08 at Day XX/INSTRUCTOR_GRADING_1-100.md
 * (day-wise grading; not inside each task folder).
 *
 * Run from repo root: node scripts/emit-instructor-grading-days-01-08.mjs
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

/** @typedef {{ day:string, slug:string, title:string, type:'html'|'css'|'js', checks:string[], gates?:string[] }} Task */

/** @type {Task[]} */
const TASKS = [
  {
    day: '01',
    slug: 'task-01-minimal-valid-document',
    title: 'Minimal valid HTML5 document',
    type: 'html',
    checks: [
      '<!DOCTYPE html> present and first; HTML5 mode implied.',
      '<html lang="…"> set meaningfully (e.g. en unless directed).',
      'Charset + viewport meta + <title> present and sensible.',
      'Body content renders; no broken self-inflicted console errors from markup.',
      'TODO markers resolved per cohort policy (no “fake done”).',
    ],
    gates: ['Missing doctype or charset where required by instructions.'],
  },
  {
    day: '01',
    slug: 'task-02-head-metadata-basics',
    title: 'Head metadata basics',
    type: 'html',
    checks: [
      'Favicon / icon link wired as instructed; paths valid.',
      'Social / SEO meta only if task asked—avoid cargo-cult tags.',
      'Title and description (if required) match visible page intent.',
      'Relative asset paths resilient to opening file vs simple server.',
    ],
  },
  {
    day: '01',
    slug: 'task-03-external-assets-defer-async',
    title: 'External assets defer/async',
    type: 'html',
    checks: [
      'Scripts placed per lab goals (defer/async semantics understood in markup).',
      'No duplicate loads unless justified; order preserves dependencies.',
      'CSS linked once; no flash of totally unstyled content beyond lab scope.',
      'Brief rationale comment acceptable; avoid essay-length comments.',
    ],
  },
  {
    day: '01',
    slug: 'task-04-structured-profile-page',
    title: 'Structured profile page',
    type: 'html',
    checks: [
      'Landmarks/sections reflect outline (header/main/section/article as taught).',
      'Heading levels coherent (no skipped levels for decoration).',
      'Lists/tables only where semantically correct.',
      'Readable source formatting; IDs/classes meaningful.',
    ],
  },

  {
    day: '02',
    slug: 'task-01-article-outline-headings',
    title: 'Article outline & headings',
    type: 'html',
    checks: [
      'Single h1 (unless task explicitly allows pattern X).',
      'Heading order matches document outline in DevTools outline/A11y tree.',
      'Paragraph/sectioning supports scanning (not wall of divs).',
    ],
  },
  {
    day: '02',
    slug: 'task-02-inline-semantics-and-lists',
    title: 'Inline semantics & lists',
    type: 'html',
    checks: [
      'Appropriate emphasis elements (strong/em/cite/q) vs bold italics alone.',
      'Lists: ol/ul choice matches meaning; nesting valid.',
      'Links descriptive (avoid “click here” unless task teaches contrast).',
    ],
  },
  {
    day: '02',
    slug: 'task-03-font-stack-and-line-height',
    title: 'Font stack & line-height',
    type: 'css',
    checks: [
      'font-family stack plausible with fallbacks.',
      'line-height improves readability vs browser default where asked.',
      'No illegible contrast on body text (basic WCAG awareness).',
    ],
  },
  {
    day: '02',
    slug: 'task-04-inheritance-reading-page',
    title: 'Inheritance reading page',
    type: 'css',
    checks: [
      'Demonstrates inheritance/cascade goal from instructions (specific selectors).',
      'Unexpected overrides explained by source order/specificity (if rubric asks).',
      'CSS organized by section or component, not one giant unordered block.',
    ],
  },

  {
    day: '03',
    slug: 'task-01-simple-data-table',
    title: 'Simple data table',
    type: 'html',
    checks: [
      'table/thead/tbody structure where required; tr/td/th valid.',
      'Captions or headings if specified; no layout tables for data.',
    ],
  },
  {
    day: '03',
    slug: 'task-02-thead-tbody-scope-headers',
    title: 'Scope headers & thead/tbody',
    type: 'html',
    checks: [
      'th scope values correct for reading axis (col/row as taught).',
      'Header cells align with data cells visually and structurally.',
    ],
  },
  {
    day: '03',
    slug: 'task-03-colspan-rowspan-timetable',
    title: 'Colspan/rowspan timetable',
    type: 'html',
    checks: [
      'colspan/rowspan grid mathematically consistent (no ragged holes).',
      'Screen reader sanity: headers still discoverable where required.',
    ],
  },
  {
    day: '03',
    slug: 'task-04-styled-pricing-table',
    title: 'Styled pricing table',
    type: 'css',
    checks: [
      'Table remains semantic after styling (no display:table hacks that destroy semantics).',
      'Zebra/hover/borders readable; responsive shrink doesn’t destroy alignment beyond lab scope.',
    ],
  },

  {
    day: '04',
    slug: 'task-01-labeled-fieldset-form',
    title: 'Labeled fieldset form',
    type: 'html',
    checks: [
      'Every input has label (explicit for/id or wrapping pattern per task).',
      'fieldset/legend used correctly if required.',
      'Button types intentional (submit vs button).',
    ],
    gates: ['Clickable label not associated with control (if task requires labels).'],
  },
  {
    day: '04',
    slug: 'task-02-html5-inputs-validation',
    title: 'HTML5 inputs & validation',
    type: 'html',
    checks: [
      'Appropriate input types (email/url/number/date…) per brief.',
      'Validation attributes used as taught (required, min/max, pattern) without fighting UX.',
      'Error affordances match instructions (native vs custom if specified).',
    ],
  },
  {
    day: '04',
    slug: 'task-03-textarea-select-buttons',
    title: 'Textarea, select, buttons',
    type: 'html',
    checks: [
      'select options meaningful; optgroup if specified.',
      'textarea sizing/resize rules per CSS brief.',
      'Keyboard operable controls (no trapped focus in simple pages).',
    ],
  },
  {
    day: '04',
    slug: 'task-04-get-post-method-lab',
    title: 'GET/POST method lab',
    type: 'html',
    checks: [
      'Forms use correct method/action targets per instructions.',
      'Control names produce expected query/body shape in devtools network preview.',
      'Security hygiene: no secrets in GET URLs for passwords (if applicable to scenario).',
    ],
    gates: ['Password or sensitive data placed in GET form (redo + teach).'],
  },

  {
    day: '05',
    slug: 'task-01-selector-practice-board',
    title: 'Selector practice board',
    type: 'css',
    checks: [
      'Selectors match targets without over-broad `*` abuse unless taught.',
      'Combinators/pseudo-classes used as specified.',
    ],
  },
  {
    day: '05',
    slug: 'task-02-borders-backgrounds-cards',
    title: 'Borders & backgrounds cards',
    type: 'css',
    checks: [
      'border-radius/background layering matches mock intent.',
      'Contrast readable on cards; borders don’t clip content unexpectedly.',
    ],
  },
  {
    day: '05',
    slug: 'task-03-text-decoration-transform-banner',
    title: 'Text decoration & transform banner',
    type: 'css',
    checks: [
      'text-decoration / text-transform applied per spec.',
      'Transforms don’t harm readability; transform-origin considered if animated.',
    ],
  },
  {
    day: '05',
    slug: 'task-04-product-card-gallery',
    title: 'Product card gallery',
    type: 'css',
    checks: [
      'Card layout stable; images sized (object-fit if taught).',
      'Hover/focus states visible and not keyboard-hostile.',
    ],
  },

  {
    day: '06',
    slug: 'task-01-shadow-studio-cards',
    title: 'Shadow studio cards',
    type: 'css',
    checks: [
      'box-shadow/text-shadow used intentionally (layered shadows if asked).',
      'Performance reasonable (no enormous blur chains unless instructed).',
    ],
  },
  {
    day: '06',
    slug: 'task-02-fluid-type-clamp-and-viewport',
    title: 'Fluid type clamp & viewport units',
    type: 'css',
    checks: [
      'clamp()/min()/max() fluid type behaves across two viewport widths in manual check.',
      'vw/vh used without accidental overflow traps (where task warns).',
    ],
  },
  {
    day: '06',
    slug: 'task-03-em-rem-compounding-trap',
    title: 'em/rem compounding trap',
    type: 'css',
    checks: [
      'Demonstrates understanding of em compounding vs rem stability per brief.',
      'Fix avoids “magic numbers” without brief justification comments if rubric expects explanation.',
    ],
  },
  {
    day: '06',
    slug: 'task-04-css-length-math-lab',
    title: 'CSS length math lab (Vitest)',
    type: 'js',
    checks: [
      '`npm test` passes with no edits to autograder files.',
      'Public functions match contracts (NaN, RangeError message exactness if specified).',
      'No global side effects; pure functions remain pure.',
      'Readable names; small helpers only if they clarify (avoid over-abstraction).',
    ],
    gates: ['Tests edited against instructions; plagiarism on implementations.'],
  },

  {
    day: '07',
    slug: 'task-01-box-model-measurement-sheet',
    title: 'Box model measurement sheet',
    type: 'css',
    checks: [
      'padding/border/margin relationships match exercise measurements.',
      'box-sizing choice consistent with instructions (content-box vs border-box lesson).',
    ],
  },
  {
    day: '07',
    slug: 'task-02-margin-collapse-detective',
    title: 'Margin collapse detective',
    type: 'css',
    checks: [
      'Collapse scenarios identified/fixes match taught rules.',
      'Demonstrations reproducible in browser (not accidental layout dependence).',
    ],
  },
  {
    day: '07',
    slug: 'task-03-border-box-migration-playground',
    title: 'border-box migration playground',
    type: 'css',
    checks: [
      'Global/local border-box strategy matches brief; no double resets chaos.',
      'Regression checks: widths predictable after migration.',
    ],
  },
  {
    day: '07',
    slug: 'task-04-triple-collapse-clinic',
    title: 'Triple collapse clinic',
    type: 'css',
    checks: [
      'Three collapse cases addressed distinctly (not one hack for all).',
      'Comments explain “why” briefly where non-obvious.',
    ],
  },

  {
    day: '08',
    slug: 'task-01-static-relative-playground',
    title: 'Static/relative playground',
    type: 'css',
    checks: [
      'relative offsets behave as instructed; containing blocks understood.',
      'No accidental absolute unless task introduces it next.',
    ],
  },
  {
    day: '08',
    slug: 'task-02-absolute-containing-block-challenge',
    title: 'Absolute containing block challenge',
    type: 'css',
    checks: [
      'position:absolute positioned against correct ancestor per brief.',
      'z-index/stacking not “random”; offsets measurable.',
    ],
  },
  {
    day: '08',
    slug: 'task-03-fixed-header-sticky-sidebar',
    title: 'Fixed header & sticky sidebar',
    type: 'css',
    checks: [
      'fixed header doesn’t obscure content (padding/margin compensation if required).',
      'sticky behavior respects overflow ancestors (common footgun—note in feedback if hit).',
    ],
  },
  {
    day: '08',
    slug: 'task-04-stacking-context-z-index-mystery',
    title: 'Stacking context & z-index mystery',
    type: 'css',
    checks: [
      'stacking context sources identified (opacity/transform/etc. if in brief).',
      'Fix uses minimal z-index changes; avoids z-index arms race where possible.',
    ],
  },
];

const DAY_FOCUS = {
  '01': 'HTML5 shell, metadata, assets, structured profile markup.',
  '02': 'Semantic outline, inline semantics, typography, inheritance/cascade.',
  '03': 'Accessible tables: structure, scope, spanning, presentation styling.',
  '04': 'Forms: labels, HTML5 inputs, controls, GET vs POST.',
  '05': 'Selectors, borders/backgrounds, text decoration/transform, card gallery.',
  '06': 'Shadows, fluid type & units, em/rem mental model, Vitest units lab.',
  '07': 'Box model, margin collapse, border-box migration.',
  '08': 'Positioning: static/relative, absolute, fixed/sticky, stacking contexts.',
};

function taskIndexFromSlug(slug) {
  const m = /^task-(\d+)-/.exec(slug);
  return m ? Number(m[1]) : 0;
}

function perTaskCategoryRows(type) {
  if (type === 'js') {
    return [
      '| Requirements (instructions + API) | 9 |  |  |',
      '| `npm test` / correctness | 9 |  |  |',
      '| Code clarity & safety | 5 |  |  |',
      '| Process & polish | 2 |  |  |',
      '| **Subtotal this task** | **25** |  |  |',
    ].join('\n');
  }
  return [
    '| Requirements coverage | 10 |  |  |',
    '| Correctness (browser / behavior) | 8 |  |  |',
    '| Semantics, a11y, maintainability | 5 |  |  |',
    '| Process & polish | 2 |  |  |',
    '| **Subtotal this task** | **25** |  |  |',
  ].join('\n');
}

function renderTaskSection(t) {
  const idx = taskIndexFromSlug(t.slug);
  const gates = (t.gates ?? []).map((g) => `- **Hard concern:** ${g}`).join('\n');
  const gatesBlock =
    gates.length > 0
      ? `**Hard concerns for this task:**\n\n${gates}\n`
      : '**Hard concerns:** add institution-specific issues if discovered.\n';

  const checks = t.checks.map((c) => `- ${c}`).join('\n');

  return `### Task ${idx} — ${t.title}

- **Folder:** \`practical-tasks/${t.slug}/\`
- **Type:** **${t.type.toUpperCase()}**${t.type === 'js' ? ' (Vitest)' : ''}
- **Candidate rubric:** \`practical-tasks/${t.slug}/EVALUATION_CRITERIA.md\`
- **Brief:** \`practical-tasks/${t.slug}/TASK_INSTRUCTIONS.md\`

#### Observable checklist

${checks}

${gatesBlock}
#### Score this task (max **25**)

Use category maxima below; **sum row must not exceed 25** for this task.

| Category | Max | Score | Notes |
|----------|----:|------:|-------|
${perTaskCategoryRows(t.type)}
`;
}

function renderDay(day) {
  const tasks = TASKS.filter((t) => t.day === day).sort(
    (a, b) => taskIndexFromSlug(a.slug) - taskIndexFromSlug(b.slug),
  );
  const focus = DAY_FOCUS[day] || `See DAY-${day}-THEORY-AND-REFERENCE.md`;
  const sections = tasks.map(renderTaskSection).join('\n');

  return `# Instructor grading — Day ${day} (1–100)

> **Learner profile:** Second-year graduate. Grade for **lab completion** and **taught concepts**, not production polish.

## Canonical methodology

Use **\`course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md\`** for category definitions, bands, feedback tone, and AI workflow.

## Day snapshot

- **Primary focus (map):** ${focus}
- **This file lives at:** \`Day ${day}/INSTRUCTOR_GRADING_1-100.md\` (**day-level**; not inside each \`task-*\` folder).

## Day scoring model (100 = full day)

| Task slot | Max points | Running total |
|-----------|------------:|---------------|
| Task 1 | 25 | 25 |
| Task 2 | 25 | 50 |
| Task 3 | 25 | 75 |
| Task 4 | 25 | **100** |

**Day total /100** = sum of the four task subtotals (each task scored out of **25**).

For **HTML/CSS tasks**, within each /25 use the scaled rows in each task’s table (10 + 8 + 5 + 2). For **Day 06 Task 4 (Vitest)**, use the JS row group (9 + 9 + 5 + 2).

---

## Tasks

${sections}
---

## Day record sheet (optional)

| Task | Max | Score | Notes |
|------|----:|------:|-------|
| Task 1 | 25 |  |  |
| Task 2 | 25 |  |  |
| Task 3 | 25 |  |  |
| Task 4 | 25 |  |  |
| **Day total** | **100** |  |  |

## Day-level band (same scale as guide §5)

Map **Day total** to labels using \`05-…\` §5 (Excellent 90–100, Strong 80–89, …).

## AI-assisted grading prompt (paste)

\`\`\`text
Grade the full Day ${day} submission (all tasks under Day ${day}/practical-tasks/).
Evidence: <paste diff or list files reviewed>.
For each task, fill the /25 table using the checklist in Day ${day}/INSTRUCTOR_GRADING_1-100.md; sum to /100.
Follow course-generation-instructions/05-INSTRUCTOR-GRADING-1-100-AND-AI-EVALUATION-GUIDE.md for tone and output format.
Return: day total /100, per-task subscores, pass/needs-revision, 3 day-level improvement suggestions, hard concerns.
\`\`\`
`;
}

const DAYS = ['01', '02', '03', '04', '05', '06', '07', '08'];

for (const day of DAYS) {
  const outDir = path.join(ROOT, `Day ${day}`);
  const out = path.join(outDir, 'INSTRUCTOR_GRADING_1-100.md');
  if (!fs.existsSync(outDir)) {
    console.error('Missing day folder:', outDir);
    process.exitCode = 1;
    continue;
  }
  fs.writeFileSync(out, `${renderDay(day).trim()}\n`, 'utf8');
  console.log('Wrote', path.relative(ROOT, out));
}

console.log('Done: day files', DAYS.length);
