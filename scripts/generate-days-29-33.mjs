import { copyFileSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");

const vitestPkg = (name) =>
  JSON.stringify(
    {
      name,
      version: "1.0.0",
      private: true,
      type: "module",
      scripts: { test: "vitest run" },
      devDependencies: { vitest: "^2.1.9" },
    },
    null,
    2,
  ) + "\n";

const npmrc = "registry=https://registry.npmjs.org/\n";

function writeFile(path, body) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, body, "utf8");
}

function evalMd(day, task, title) {
  const d = String(day).padStart(2, "0");
  const t = String(task).padStart(2, "0");
  return `# Evaluation Criteria — Day ${day} — Task ${t} — ${title}

## Scope

Graded: candidate \`src/\` edits vs Vitest tests.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | \`npm test\` passes |
| Code quality | 20 | Readable |
| Requirements coverage | 25 | Meets TASK_INSTRUCTIONS |
| Docs / readability | 15 | Matches brief |

## Pass / fail gates

- Any test failure.

## AI-assisted grading prompt (optional)

\`\`\`markdown
Context: \`Day ${d}/practical-tasks/task-${t}-...\`.
Verify \`npm test\` passes.
\`\`\`
`;
}

function taskInstr(day, task, title, summary, goals, impl) {
  const d = String(day).padStart(2, "0");
  const t = String(task).padStart(2, "0");
  const implText = Array.isArray(impl) ? impl.join("\n\n") : impl;
  return `# Task ${task} — ${title}

## Summary

${summary}

## Learning goals

${goals.map((g) => `- ${g}`).join("\n")}

## Provided files

- \`package.json\`, \`.npmrc\`, \`src/\`, \`tests/\`

## Prerequisites

- Day ${d} theory.

## What you will implement

${implText}

## Constraints

- Do not edit tests.

## How to run and verify

\`\`\`bash
cd "Day ${d}/practical-tasks/task-${t}-<folder-slug>"
npm install
npm test
\`\`\`

## Submission checklist (Git)

- [ ] \`npm test\` passes
`;
}

function dayReadme(day, title, objectives, folders) {
  const d = String(day).padStart(2, "0");
  const rows = folders
    .map(
      (f, i) =>
        `| ${i + 1} | \`${f}\` | JavaScript | \`npm install\` → \`npm test\` |`,
    )
    .join("\n");
  return `# Day ${day} — ${title}

## Learning objectives

${objectives.map((o) => `- ${o}`).join("\n")}

## Prerequisites

- **Day ${day - 1}** and earlier JavaScript days.

## How to use this folder

1. Read \`DAY-${d}-THEORY-AND-REFERENCE.md\`.
2. Run tasks in order with Vitest.

## Task list

| Order | Folder | Type | Verify with |
|------:|--------|------|-------------|
${rows}
`;
}

function writeDay(dayMeta) {
  const d = String(dayMeta.day).padStart(2, "0");
  const dayDir = join(ROOT, `Day ${d}`);
  writeFile(join(dayDir, "README.md"), dayMeta.readme);
  writeFile(join(dayDir, `DAY-${d}-THEORY-AND-REFERENCE.md`), dayMeta.theory);
  for (const t of dayMeta.tasks) {
    const base = join(dayDir, "practical-tasks", t.folder);
    writeFile(join(base, "package.json"), vitestPkg(t.pkgName));
    writeFile(join(base, ".npmrc"), npmrc);
    writeFile(join(base, "src", t.srcFile), t.src);
    writeFile(join(base, "tests", t.testFile), t.test);
    writeFile(join(base, "TASK_INSTRUCTIONS.md"), t.instructions);
    writeFile(join(base, "EVALUATION_CRITERIA.md"), evalMd(dayMeta.day, t.index, t.evalTitle));
  }
}

writeDay({
  day: 29,
  readme: dayReadme(29, "ES2015 Classes: `extends` and `super`", [
    "Declare classes with concise method syntax.",
    "Use **`extends`** and **`super`** for inheritance.",
    "Override methods while calling parent implementations when needed.",
  ], [
    "task-01-class-animal-speak",
    "task-02-extends-dog-super",
    "task-03-instanceof-hierarchy",
    "task-04-shape-area-challenge",
  ]),
  theory: `# Day 29 — ES2015 Classes: \`extends\` and \`super\`

**Primary theme:** Class syntax, inheritance, and \`super\` calls  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Instruction alignment:** Maps to *ES2015 classes and inheritance*.

---

## Overview

Classes are syntactic sugar over prototypes but encourage clearer hierarchies. \`extends\` sets up the prototype chain, and \`super\` lets a subclass invoke the parent constructor or methods.

---

## Day roadmap

1. Class basics
2. \`extends\` / \`super\` in constructors
3. \`super\` in methods
4. Further reading (MDN)

---

## Further reading

- MDN: [Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes)
- MDN: [\`extends\`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/extends)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Subclass** | Derived class via \`extends\`. |

`,
  tasks: [
    {
      index: 1,
      folder: "task-01-class-animal-speak",
      pkgName: "day-29-task-01-class-animal-speak",
      srcFile: "animal.js",
      testFile: "animal.test.js",
      evalTitle: "Animal class",
      src: `export class Animal {
  constructor(name = "") {
    // TODO(Day29-task01): store name string (default ""). If non-string, treat as ""
    this.name = "";
  }

  speak() {
    // TODO(Day29-task01): return "..." if name empty/whitespace-only else "<name> says something" (trim name)
    return "";
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { Animal } from "../src/animal.js";

describe("Animal", () => {
  it("speaks with name", () => {
    expect(new Animal("Ada").speak()).toBe("Ada says something");
  });

  it("handles missing name", () => {
    expect(new Animal().speak()).toBe("...");
  });
});
`,
      instructions: taskInstr(
        29,
        1,
        "Animal class",
        "Basic class with constructor + method.",
        ["Warm-up class syntax."],
        ["1. Implement \`constructor\` + \`speak\` per tests."],
      ),
    },
    {
      index: 2,
      folder: "task-02-extends-dog-super",
      pkgName: "day-29-task-02-extends-dog-super",
      srcFile: "dog.js",
      testFile: "dog.test.js",
      evalTitle: "extends + super",
      src: `import { Animal } from "./animal.js";

export class Dog extends Animal {
  constructor(name, breed) {
    // TODO(Day29-task02): super(name); store breed string (default "mixed")
    super("");
    this.breed = "mixed";
  }

  speak() {
    // TODO(Day29-task02): return super.speak() + " (" + this.breed + ")"
    return "";
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { Dog } from "../src/dog.js";

describe("Dog", () => {
  it("uses super", () => {
    const d = new Dog("Rex", "corgi");
    expect(d.speak()).toBe("Rex says something (corgi)");
  });
});
`,
      instructions: taskInstr(
        29,
        2,
        "Dog extends Animal",
        "Subclass constructor must call \`super\` and extend \`speak\`.",
        ["Practice \`extends\` + \`super\` in methods."],
        ["1. Call \`super(name)\`.", "2. Append breed in \`speak\` using \`super.speak()\`."],
      ),
    },
    {
      index: 3,
      folder: "task-03-instanceof-hierarchy",
      pkgName: "day-29-task-03-instanceof-hierarchy",
      srcFile: "hierarchy.js",
      testFile: "hierarchy.test.js",
      evalTitle: "instanceof",
      src: `export class Animal {
  constructor(name = "") {
    this.name = typeof name === "string" ? name : "";
  }
}

export class Dog extends Animal {
  constructor(name = "", breed = "mixed") {
    super(name);
    this.breed = typeof breed === "string" ? breed : "mixed";
  }
}

export function classifyPet(x) {
  // TODO(Day29-task03): return "dog" if Dog, else "animal" if Animal, else "unknown" (most specific first)
  return "unknown";
}
`,
      test: `import { describe, expect, it } from "vitest";
import { Animal, Dog, classifyPet } from "../src/hierarchy.js";

describe("classifyPet", () => {
  it("uses instanceof", () => {
    expect(classifyPet(new Dog("a", "b"))).toBe("dog");
    expect(classifyPet(new Animal("a"))).toBe("animal");
    expect(classifyPet({})).toBe("unknown");
  });
});
`,
      instructions: taskInstr(
        29,
        3,
        "instanceof hierarchy",
        "Branch on runtime types using \`instanceof\`.",
        ["Connect classes to \`instanceof\` checks."],
        ["1. Order checks from most specific to least specific."],
      ),
    },
    {
      index: 4,
      folder: "task-04-shape-area-challenge",
      pkgName: "day-29-task-04-shape-area-challenge",
      srcFile: "shapes.js",
      testFile: "shapes.test.js",
      evalTitle: "Shape area challenge",
      src: `export class Rectangle {
  constructor(w, h) {
    this.w = w;
    this.h = h;
  }
  area() {
    // TODO(Day29-task04): return w*h if finite positives else 0
    return 0;
  }
}

export class Square extends Rectangle {
  constructor(side) {
    // TODO(Day29-task04): super(side, side)
    super(0, 0);
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { Rectangle, Square } from "../src/shapes.js";

describe("Shapes", () => {
  it("computes rectangle area", () => {
    expect(new Rectangle(3, 4).area()).toBe(12);
  });

  it("square uses super", () => {
    expect(new Square(5).area()).toBe(25);
  });
});
`,
      instructions: taskInstr(
        29,
        4,
        "Shape area challenge",
        "Subclass \`Square\` must route through \`Rectangle\` constructor correctly.",
        ["Practice \`super\` in subclass constructor."],
        ["1. \`Square\` calls \`super(side, side)\`.", "2. Guard invalid dimensions in \`area\`."],
      ),
    },
  ],
});

writeDay({
  day: 30,
  readme: dayReadme(30, "Regular Expressions: Flags, Literals, Classes, Quantifiers", [
    "Use \`RegExp\` and regex literals with common **flags**.",
    "Match digit/letter classes and combine quantifiers.",
    "Choose between greedy vs non-greedy where it matters (preview for Day 33).",
  ], [
    "task-01-regex-test-flags",
    "task-02-digit-letter-classes",
    "task-03-quantifiers-basics",
    "task-04-extract-yaml-ish-keys-challenge",
  ]),
  theory: `# Day 30 — Regular Expressions (Basics)

**Primary theme:** Flags, literals, character classes, quantifiers  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Instruction alignment:** Maps to *Regular expressions — basics*.

---

## Overview

Regular expressions search structured text: identifiers, dates, IDs, logs. Master the **literal syntax**, **flags** like \`i\` and \`m\`, and safe boundaries with quantifiers.

---

## Further reading

- MDN: [Regular expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions)

`,
  tasks: [
    {
      index: 1,
      folder: "task-01-regex-test-flags",
      pkgName: "day-30-task-01-regex-test-flags",
      srcFile: "flagsLab.js",
      testFile: "flagsLab.test.js",
      evalTitle: "Regex flags",
      src: `export function hasCaseInsensitiveYes(text) {
  // TODO(Day30-task01): return true if /yes/i matches text (string input else false)
  return false;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { hasCaseInsensitiveYes } from "../src/flagsLab.js";

describe("hasCaseInsensitiveYes", () => {
  it("uses case-insensitive flag", () => {
    expect(hasCaseInsensitiveYes("YES!")).toBe(true);
    expect(hasCaseInsensitiveYes("no")).toBe(false);
  });
});
`,
      instructions: taskInstr(
        30,
        1,
        "Flags lab",
        "Use the \`i\` flag for case-insensitive matching.",
        ["Literal vs RegExp constructor."],
        ["1. Implement with \`/yes/i\` or equivalent."],
      ),
    },
    {
      index: 2,
      folder: "task-02-digit-letter-classes",
      pkgName: "day-30-task-02-digit-letter-classes",
      srcFile: "classesLab.js",
      testFile: "classesLab.test.js",
      evalTitle: "Character classes",
      src: `export function isThreeDigits(s) {
  // TODO(Day30-task02): return true iff string matches exactly three ASCII digits ^\\d{3}$
  return false;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { isThreeDigits } from "../src/classesLab.js";

describe("isThreeDigits", () => {
  it("matches exactly three digits", () => {
    expect(isThreeDigits("909")).toBe(true);
    expect(isThreeDigits("90")).toBe(false);
    expect(isThreeDigits("9090")).toBe(false);
  });
});
`,
      instructions: taskInstr(
        30,
        2,
        "Character classes",
        "Anchor and digit class practice.",
        ["Use \`^\` and \`$\` for full-string matches."],
        ["1. Implement \`^\\\\d{3}$\` behavior."],
      ),
    },
    {
      index: 3,
      folder: "task-03-quantifiers-basics",
      pkgName: "day-30-task-03-quantifiers-basics",
      srcFile: "quantLab.js",
      testFile: "quantLab.test.js",
      evalTitle: "Quantifiers",
      src: `export function splitCommaList(s) {
  // TODO(Day30-task03): split on commas with optional surrounding spaces: /\\s*,\\s*/ and filter empty tokens
  return [];
}
`,
      test: `import { describe, expect, it } from "vitest";
import { splitCommaList } from "../src/quantLab.js";

describe("splitCommaList", () => {
  it("splits comma lists", () => {
    expect(splitCommaList("a, b ,c")).toEqual(["a", "b", "c"]);
  });
});
`,
      instructions: taskInstr(
        30,
        3,
        "Quantifiers",
        "Split using regex with optional whitespace.",
        ["Practice \`+\` / \`*\` around separators."],
        ["1. Trim tokens after split."],
      ),
    },
    {
      index: 4,
      folder: "task-04-extract-yaml-ish-keys-challenge",
      pkgName: "day-30-task-04-extract-yaml-ish-keys-challenge",
      srcFile: "yamlKeys.js",
      testFile: "yamlKeys.test.js",
      evalTitle: "YAML-ish keys",
      src: `export function parseKeyValueLines(text) {
  // TODO(Day30-task04): for each line "key: value" (trim), return object mapping keys to trimmed values; ignore empty lines
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { parseKeyValueLines } from "../src/yamlKeys.js";

describe("parseKeyValueLines", () => {
  it("parses lines", () => {
    expect(parseKeyValueLines("a: 1\\nb: two")).toEqual({ a: "1", b: "two" });
  });
});
`,
      instructions: taskInstr(
        30,
        4,
        "YAML-ish keys challenge",
        "Line-based parsing with a simple \`/^([^:]+):\\s*(.+)$/\` style regex per line.",
        ["Combine regex with line splitting."],
        ["1. Return a plain object."],
      ),
    },
  ],
});

writeDay({
  day: 31,
  readme: dayReadme(31, "ES2015 Collections & Objects: `Map`, `Set`, `Symbol`, and Object utilities", [
    "Use **`Map`/`Set`** for collections with non-string keys or uniqueness.",
    "Apply **`Object.fromEntries`** / **`Object.entries`** patterns.",
    "Introduce **`Symbol`** as opaque keys (lightweight exercise).",
  ], [
    "task-01-map-frequency-count",
    "task-02-set-unique-normalized",
    "task-03-symbol-description-key",
    "task-04-weakmap-metadata-challenge",
  ]),
  theory: `# Day 31 — ES2015 Collections & Objects

**Primary theme:** \`Map\`, \`Set\`, \`Symbol\`, and object utilities  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Instruction alignment:** Maps to *ES2015 intermediate: Object.keys/values; computed props; getters/setters; Symbol; Set/Map/WeakSet/WeakMap*.

---

## Overview

Maps and sets are purpose-built collections. Symbols can act as unique property keys. WeakMaps can attach metadata to objects without leaking memory when objects are GC’d.

---

## Further reading

- MDN: [\`Map\`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map)
- MDN: [\`Set\`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set)

`,
  tasks: [
    {
      index: 1,
      folder: "task-01-map-frequency-count",
      pkgName: "day-31-task-01-map-frequency-count",
      srcFile: "freqMap.js",
      testFile: "freqMap.test.js",
      evalTitle: "Map frequencies",
      src: `export function countTokens(tokens) {
  // TODO(Day31-task01): tokens is string[]; return Map from lowercased trimmed token -> count (ignore empty strings)
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { countTokens } from "../src/freqMap.js";

describe("countTokens", () => {
  it("counts with Map", () => {
    const m = countTokens(["A", "a", "b", ""]);
    expect(m.get("a")).toBe(2);
    expect(m.get("b")).toBe(1);
  });
});
`,
      instructions: taskInstr(
        31,
        1,
        "Map frequency count",
        "Use \`Map\` to tally string tokens.",
        ["Practice \`map.get\` / \`set\` patterns."],
        ["1. Normalize tokens to lowercase."],
      ),
    },
    {
      index: 2,
      folder: "task-02-set-unique-normalized",
      pkgName: "day-31-task-02-set-unique-normalized",
      srcFile: "uniqueSet.js",
      testFile: "uniqueSet.test.js",
      evalTitle: "Set uniqueness",
      src: `export function uniqueSorted(nums) {
  // TODO(Day31-task02): return sorted unique finite numbers from array (use Set)
  return [];
}
`,
      test: `import { describe, expect, it } from "vitest";
import { uniqueSorted } from "../src/uniqueSet.js";

describe("uniqueSorted", () => {
  it("dedupes", () => {
    expect(uniqueSorted([3, 1, 3, 2])).toEqual([1, 2, 3]);
  });
});
`,
      instructions: taskInstr(
        31,
        2,
        "Set + sort",
        "Use \`Set\` to remove duplicates, then sort.",
        ["Set iteration + array sort."],
        ["1. Ignore non-finite numbers."],
      ),
    },
    {
      index: 3,
      folder: "task-03-symbol-description-key",
      pkgName: "day-31-task-03-symbol-description-key",
      srcFile: "symLab.js",
      testFile: "symLab.test.js",
      evalTitle: "Symbol keys",
      src: `export function buildSecretBag() {
  // TODO(Day31-task03): return { set(kind, value){...}, get(kind){...}} using a Map keyed by Symbol.for("kind:" + kind)
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { buildSecretBag } from "../src/symLab.js";

describe("buildSecretBag", () => {
  it("stores by symbol key", () => {
    const bag = buildSecretBag();
    bag.set("token", "abc");
    expect(bag.get("token")).toBe("abc");
  });
});
`,
      instructions: taskInstr(
        31,
        3,
        "Symbol.for keys",
        "Use \`Symbol.for\` to build stable symbol keys per string kind.",
        ["Lightweight Symbol practice."],
        ["1. Internally store in a \`Map\`."],
      ),
    },
    {
      index: 4,
      folder: "task-04-weakmap-metadata-challenge",
      pkgName: "day-31-task-04-weakmap-metadata-challenge",
      srcFile: "metaWeak.js",
      testFile: "metaWeak.test.js",
      evalTitle: "WeakMap metadata",
      src: `export function createObjectMetadata() {
  // TODO(Day31-task04): return { tag(obj, label){...}, read(obj){...}} backed by WeakMap (label string)
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { createObjectMetadata } from "../src/metaWeak.js";

describe("WeakMap metadata", () => {
  it("tags objects", () => {
    const m = createObjectMetadata();
    const o = {};
    m.tag(o, "first");
    expect(m.read(o)).toBe("first");
  });
});
`,
      instructions: taskInstr(
        31,
        4,
        "WeakMap challenge",
        "Attach metadata to arbitrary objects without mutating them.",
        ["WeakMap for side metadata."],
        ["1. \`read\` returns undefined if never tagged."],
      ),
    },
  ],
});

writeDay({
  day: 32,
  readme: dayReadme(32, "Strict Mode & Errors: `try/catch`, Custom Errors", [
    "Describe effects of **strict mode** relevant to debugging.",
    "Use **\`try/catch/finally\`** for controlled error handling.",
    "Create **subclasses of \`Error\`** with extra fields.",
  ], [
    "task-01-strict-function-this",
    "task-02-try-parse-json",
    "task-03-custom-validation-error",
    "task-04-result-type-challenge",
  ]),
  theory: `# Day 32 — Strict Mode & Errors

**Primary theme:** Strict mode basics, structured errors, and \`try/catch/finally\`  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Instruction alignment:** Maps to *Strict mode* and *Errors: try/catch/finally, throw, Error, custom errors*.

---

## Overview

Strict mode catches more mistakes and changes some silent failures into throws. Structured error types (\`class MyError extends Error\`) improve diagnostics in libraries and APIs.

---

## Further reading

- MDN: [\`try...catch\`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/try...catch)
- MDN: [Strict mode](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode)

`,
  tasks: [
    {
      index: 1,
      folder: "task-01-strict-function-this",
      pkgName: "day-32-task-01-strict-function-this",
      srcFile: "strictThis.js",
      testFile: "strictThis.test.js",
      evalTitle: "Strict this",
      src: `export function standaloneThisType() {
  // TODO(Day32-task01): In strict mode, return typeof this for a standalone function invoked as (function(){ return this; })()
  return "object";
}
`,
      test: `import { describe, expect, it } from "vitest";
import { standaloneThisType } from "../src/strictThis.js";

describe("standaloneThisType", () => {
  it("is undefined in strict IIFE", () => {
    expect(standaloneThisType()).toBe("undefined");
  });
});
`,
      instructions: taskInstr(
        32,
        1,
        "Strict standalone this",
        "Observe strict-mode \`this\` in a standalone function call.",
        ["Connect strict mode to safer defaults."],
        ["1. File already includes directive—do not remove."],
      ),
    },
    {
      index: 2,
      folder: "task-02-try-parse-json",
      pkgName: "day-32-task-02-try-parse-json",
      srcFile: "safeJson.js",
      testFile: "safeJson.test.js",
      evalTitle: "try/catch JSON",
      src: `export function parseJsonSafe(text, fallback = null) {
  // TODO(Day32-task02): try JSON.parse; on SyntaxError return fallback; if text not string return fallback
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { parseJsonSafe } from "../src/safeJson.js";

describe("parseJsonSafe", () => {
  it("parses valid json", () => {
    expect(parseJsonSafe('{"a":1}')).toEqual({ a: 1 });
  });

  it("returns fallback on invalid", () => {
    expect(parseJsonSafe("{", 1)).toBe(1);
  });
});
`,
      instructions: taskInstr(
        32,
        2,
        "Safe JSON parse",
        "Wrap \`JSON.parse\` with \`try/catch\`.",
        ["Handle \`SyntaxError\` specifically if you like—but tests only require fallback behavior."],
        ["1. Non-strings return fallback."],
      ),
    },
    {
      index: 3,
      folder: "task-03-custom-validation-error",
      pkgName: "day-32-task-03-custom-validation-error",
      srcFile: "validationError.js",
      testFile: "validationError.test.js",
      evalTitle: "Custom Error",
      src: `export class ValidationError extends Error {
  constructor(message, field) {
    // TODO(Day32-task03): super(message); set this.field = field; set this.name = "ValidationError"
    super();
    this.field = "";
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { ValidationError } from "../src/validationError.js";

describe("ValidationError", () => {
  it("carries field", () => {
    const e = new ValidationError("bad", "email");
    expect(e).toBeInstanceOf(Error);
    expect(e.field).toBe("email");
    expect(e.name).toBe("ValidationError");
  });
});
`,
      instructions: taskInstr(
        32,
        3,
        "Custom ValidationError",
        "Subclass \`Error\` with an extra property.",
        ["Custom errors for API validation."],
        ["1. Call \`super(message)\`.", "2. Set \`name\` for clearer stacks."],
      ),
    },
    {
      index: 4,
      folder: "task-04-result-type-challenge",
      pkgName: "day-32-task-04-result-type-challenge",
      srcFile: "result.js",
      testFile: "result.test.js",
      evalTitle: "Result type",
      src: `export function divide(a, b) {
  // TODO(Day32-task04): if b===0 return { ok:false, error:"division by zero" }; else { ok:true, value:a/b }
  return { ok: false, error: "TODO" };
}
`,
      test: `import { describe, expect, it } from "vitest";
import { divide } from "../src/result.js";

describe("divide", () => {
  it("returns ok result", () => {
    expect(divide(10, 2)).toEqual({ ok: true, value: 5 });
  });

  it("returns error result", () => {
    expect(divide(1, 0)).toEqual({ ok: false, error: "division by zero" });
  });
});
`,
      instructions: taskInstr(
        32,
        4,
        "Result type challenge",
        "Avoid throwing for expected failures—return a tagged result object.",
        ["Error handling without exceptions."],
        ["1. Preserve exact error string in tests."],
      ),
    },
  ],
});

writeDay({
  day: 33,
  readme: dayReadme(33, "Regex Advanced + Promises: Groups, Chaining, and Errors", [
    "Use **non-greedy** quantifiers and **capturing groups**.",
    "Create Promises with **executors** and handle resolve/reject.",
    "Chain \`.then\` / \`.catch\` and propagate errors predictably.",
  ], [
    "task-01-non-greedy-match",
    "task-02-capture-group-replace",
    "task-03-promise-constructor-basics",
    "task-04-promise-chain-challenge",
  ]),
  theory: `# Day 33 — Regex Advanced + Promises

**Primary theme:** Greedy/lazy matching, groups, Promise creation/chaining  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Instruction alignment:** Maps to *Regex advanced + Promises*.

---

## Overview

Non-greedy quantifiers stop as early as possible—useful for HTML-ish parsing tasks (still prefer real parsers in production). Promises represent future values; chaining sequences async work while letting errors propagate to \`.catch\`.

---

## Further reading

- MDN: [Promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- MDN: [Quantifiers](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions/Quantifiers)

`,
  tasks: [
    {
      index: 1,
      folder: "task-01-non-greedy-match",
      pkgName: "day-33-task-01-non-greedy-match",
      srcFile: "lazyLab.js",
      testFile: "lazyLab.test.js",
      evalTitle: "Non-greedy",
      src: `export function firstTagContents(html) {
  // TODO(Day33-task01): return first capture of <tag>...</tag> using non-greedy /[a-z]+/ inner; assume simple lowercase tags, input like "<div>hi</div><div>bye</div>"
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { firstTagContents } from "../src/lazyLab.js";

describe("firstTagContents", () => {
  it("non-greedy first match", () => {
    expect(firstTagContents("<div>hi</div><div>bye</div>")).toBe("hi");
  });
});
`,
      instructions: taskInstr(
        33,
        1,
        "Non-greedy match",
        "Use \`*?\` / \`+?\` to avoid swallowing multiple tags.",
        ["Greedy vs lazy behavior."],
        ["1. Return inner text of first tag only."],
      ),
    },
    {
      index: 2,
      folder: "task-02-capture-group-replace",
      pkgName: "day-33-task-02-capture-group-replace",
      srcFile: "replaceGroups.js",
      testFile: "replaceGroups.test.js",
      evalTitle: "Capture groups",
      src: `export function redactEmails(text) {
  // TODO(Day33-task02): replace emails like user@host.tld with <redacted:host> using String.replace + capture groups
    return text;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { redactEmails } from "../src/replaceGroups.js";

describe("redactEmails", () => {
  it("uses capture groups", () => {
    expect(redactEmails("mail ada@example.com end")).toBe("mail <redacted:example.com> end");
  });
});
`,
      instructions: taskInstr(
        33,
        2,
        "Capture group replace",
        "Use regex captures in replacement strings.",
        ["Practice \`$1\` style replacements."],
        ["1. Only basic email shape required by tests."],
      ),
    },
    {
      index: 3,
      folder: "task-03-promise-constructor-basics",
      pkgName: "day-33-task-03-promise-constructor-basics",
      srcFile: "defer.js",
      testFile: "defer.test.js",
      evalTitle: "Deferred promise",
      src: `export function createDeferred() {
  // TODO(Day33-task03): return { promise, resolve, reject } wrapping new Promise((res,rej)=>{...})
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { createDeferred } from "../src/defer.js";

describe("createDeferred", () => {
  it("resolves externally", async () => {
    const d = createDeferred();
    d.resolve(7);
    await expect(d.promise).resolves.toBe(7);
  });
});
`,
      instructions: taskInstr(
        33,
        3,
        "Deferred promise",
        "Expose \`resolve\`/\`reject\` for a hand-rolled async API.",
        ["Promise executor pattern."],
        ["1. Store resolver functions from executor."],
      ),
    },
    {
      index: 4,
      folder: "task-04-promise-chain-challenge",
      pkgName: "day-33-task-04-promise-chain-challenge",
      srcFile: "chain.js",
      testFile: "chain.test.js",
      evalTitle: "Promise chain",
      src: `export function fetchThenDoubleLater(n) {
  // TODO(Day33-task04): return Promise that resolves to (n*2) after microtask: use Promise.resolve(n).then(x=>x*2)
  return Promise.resolve(null);
}
`,
      test: `import { describe, expect, it } from "vitest";
import { fetchThenDoubleLater } from "../src/chain.js";

describe("fetchThenDoubleLater", () => {
  it("chains then", async () => {
    await expect(fetchThenDoubleLater(5)).resolves.toBe(10);
  });
});
`,
      instructions: taskInstr(
        33,
        4,
        "Promise chain challenge",
        "Practice \`.then\` chaining starting from \`Promise.resolve\`.",
        ["Basic async composition without async/await required."],
        ["1. Return a Promise per tests."],
      ),
    },
  ],
});

copyFileSync(
  join(ROOT, "Day 29/practical-tasks/task-01-class-animal-speak/src/animal.js"),
  join(ROOT, "Day 29/practical-tasks/task-02-extends-dog-super/src/animal.js"),
);

console.log("Generated Days 29–33");
