import { mkdirSync, writeFileSync } from "node:fs";
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
  return `# Evaluation Criteria — Day ${day} — Task ${String(task).padStart(2, "0")} — ${title}

## Scope

Graded: candidate \`src/\` edits vs Vitest tests.

## Weighting (100 points)

| Category | Points | Description |
|----------|-------:|-------------|
| Correctness | 40 | \`npm test\` passes |
| Code quality | 20 | Readable, small functions |
| Requirements coverage | 25 | Meets TASK_INSTRUCTIONS |
| Docs / readability | 15 | Matches JSDoc / brief |

## Pass / fail gates

- Any test failure.
- Candidate edits autograder files (unless task explicitly allows).

## AI-assisted grading prompt (optional)

\`\`\`markdown
## AI grading prompt (paste into your grader)
Context: \`Day ${String(day).padStart(2, "0")}/practical-tasks/task-${String(task).padStart(2, "0")}-...\`.
Verify \`npm test\` passes; summarize blockers.
\`\`\`
`;
}

function taskInstr(day, task, title, summary, goals, impl, constraints = "Do not edit tests.") {
  const d = String(day).padStart(2, "0");
  const t = String(task).padStart(2, "0");
  const implText = Array.isArray(impl) ? impl.join("\n\n") : impl;
  return `# Task ${task} — ${title}

## Summary

${summary}

## Learning goals

${goals.map((g) => `- ${g}`).join("\n")}

## Provided files

- \`package.json\`, \`.npmrc\`
- \`src/\` (your work), \`tests/\` (read-only)

## Prerequisites

- Day ${d} theory file.

## What you will implement

${implText}

## Constraints

- ${constraints}

## How to run and verify

\`\`\`bash
cd "Day ${d}/practical-tasks/task-${t}-<this-folder-slug>"
npm install
npm test
\`\`\`

## \`TODO\` map

| TODO | Done means |
|------|------------|
| See \`src/\` | All \`TODO(Day${d}-task${t})\` resolved |

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

- Prior JavaScript days through **Day ${day - 1}** (see theory cross-links).

## How to use this folder

1. Read \`DAY-${d}-THEORY-AND-REFERENCE.md\`.
2. Complete tasks in \`practical-tasks/\` in order (\`npm install\` → \`npm test\`).

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

/* -------------------------------------------------------------------------- */
/* Day 27 — OOP                                                             */
/* -------------------------------------------------------------------------- */

writeDay({
  day: 27,
  readme: dayReadme(27, "OOP in JavaScript: Constructors, Fields, `#`, and `static`", [
    "Use **constructor functions** or **classes** to initialize instance state.",
    "Apply **public instance fields** and **private `#` fields** appropriately.",
    "Declare **`static`** utilities that belong to the type, not instances.",
    "Contrast **per-instance** vs **per-class** state.",
  ], [
    "task-01-class-counter-fields",
    "task-02-private-hash-balance",
    "task-03-static-factory-parser",
    "task-04-bank-account-challenge",
  ]),
  theory: `# Day 27 — OOP in JavaScript: Constructors, Fields, \`#\`, and \`static\`

**Primary theme:** Object-oriented idioms in JS—constructors, instance vs private fields, static members  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Related tasks:** \`task-01-class-counter-fields\`, \`task-02-private-hash-balance\`, \`task-03-static-factory-parser\`, \`task-04-bank-account-challenge\`  
**Instruction alignment:** Maps to *OOP: constructors; public/private/static* from the master topic list.

---

## Overview

JavaScript’s OOP model is **prototypal**, but **ES2015 classes** give familiar syntax. **Private fields** (\`#x\`) enforce encapsulation at the language level, while \`static\` methods model type-level utilities (factories, parsers) without allocating instances.

---

## Day roadmap

1. Constructors and \`new\`
2. Instance fields vs methods
3. Private fields \`#\`
4. \`static\` members
5. Common mistakes & debugging
6. Further reading (MDN)
7. Glossary
8. Answers (self-test)

---

## Constructors and \`new\`

### What it is

A **constructor** initializes an object’s state. With \`class\`, \`constructor(...)\` runs on \`new\`.

#### Examples

\`\`\`js
class Point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}
\`\`\`

#### Quick checks

1. What does \`new\` return if \`constructor\` returns a plain object?

---

## Private fields \`#\`

### What it is

Fields prefixed with \`#\` are **lexically private** to the class body—no runtime escape hatch from outside.

#### Quick checks

1. Can subclasses access a base class’s \`#field\` directly?

---

## \`static\` members

### What it is

\`static\` methods/properties live on the **constructor**, not each instance.

#### Quick checks

1. Inside a static method, what does \`this\` refer to?

---

## Common mistakes & debugging

- Forgetting \`new\` (strict mode class constructors throw if mis-called).
- Trying to read private fields from tests (you should test **behavior**, not internals).

---

## Further reading

- MDN: [Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes)
- MDN: [Private features](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Private_class_fields)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Instance** | Object created by \`new\`. |
| **Static** | Belongs to the class function itself. |

---

## Answers (self-test)

1. If constructor returns an object, **that object** becomes the result of \`new\` (rare pattern).
2. **Subclasses** cannot access base \`#fields\` directly.
3. **Static \`this\`:** typically the class constructor itself.
`,
  tasks: [
    {
      index: 1,
      folder: "task-01-class-counter-fields",
      pkgName: "day-27-task-01-class-counter-fields",
      srcFile: "counterClass.js",
      testFile: "counterClass.test.js",
      evalTitle: "Class Counter Fields",
      src: `export class StepCounter {
  count = 0;
  step = 1;

  constructor(step = 1) {
    // TODO(Day27-task01): assign this.step if step is a finite number > 0, else keep default 1
  }

  tick(times = 1) {
    // TODO(Day27-task01): increment count by step * times when times is a finite integer >= 0
    return this.count;
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { StepCounter } from "../src/counterClass.js";

describe("StepCounter", () => {
  it("uses instance fields", () => {
    const c = new StepCounter(2);
    expect(c.tick()).toBe(2);
    expect(c.tick(2)).toBe(6);
  });

  it("ignores invalid constructor step", () => {
    const c = new StepCounter(-1);
    expect(c.step).toBe(1);
  });
});
`,
      instructions: taskInstr(
        27,
        1,
        "Class + instance fields",
        "Implement \`StepCounter\` with public fields \`count\` and \`step\`.",
        ["Practice class fields and constructor initialization."],
        ["1. \`constructor(step)\` sets \`this.step\` when valid.", "2. \`tick(times)\` increments \`count\` by \`step * times\`."],
      ),
    },
    {
      index: 2,
      folder: "task-02-private-hash-balance",
      pkgName: "day-27-task-02-private-hash-balance",
      srcFile: "vault.js",
      testFile: "vault.test.js",
      evalTitle: "Private balance",
      src: `export class Vault {
  #balance = 0;

  constructor(opening = 0) {
    // TODO(Day27-task02): set #balance to opening if finite number, else 0
  }

  get balance() {
    // TODO(Day27-task02): return #balance
    return Number.NaN;
  }

  deposit(amount) {
    // TODO(Day27-task02): add finite positive amount; return new balance
    return this.#balance;
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { Vault } from "../src/vault.js";

describe("Vault", () => {
  it("deposits", () => {
    const v = new Vault(10);
    expect(v.balance).toBe(10);
    expect(v.deposit(5)).toBe(15);
  });

  it("rejects bad opening", () => {
    const v = new Vault(Number.NaN);
    expect(v.balance).toBe(0);
  });
});
`,
      instructions: taskInstr(
        27,
        2,
        "Private `#` balance",
        "Use **private fields** for balance; expose read-only \`balance\` getter.",
        ["Practice private fields and getters."],
        ["1. Private \`#balance\` initialized in constructor.", "2. \`deposit\` updates balance for finite positive amounts."],
      ),
    },
    {
      index: 3,
      folder: "task-03-static-factory-parser",
      pkgName: "day-27-task-03-static-factory-parser",
      srcFile: "token.js",
      testFile: "token.test.js",
      evalTitle: "Static factory",
      src: `export class Token {
  static fromString(s) {
    // TODO(Day27-task03): if s is string "kind:value", return new Token(kind, value) trimmed; else null
    return null;
  }

  constructor(kind, value) {
    this.kind = kind;
    this.value = value;
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { Token } from "../src/token.js";

describe("Token.fromString", () => {
  it("parses", () => {
    const t = Token.fromString("  name : Ada ");
    expect(t).toBeInstanceOf(Token);
    expect(t.kind).toBe("name");
    expect(t.value).toBe("Ada");
  });

  it("rejects bad input", () => {
    expect(Token.fromString("nocolon")).toBeNull();
  });
});
`,
      instructions: taskInstr(
        27,
        3,
        "Static factory parser",
        "Implement a **static** parser that constructs instances.",
        ["Use \`static\` methods for alternative constructors."],
        ["1. \`Token.fromString\` returns \`new Token(kind, value)\` or \`null\`."],
      ),
    },
    {
      index: 4,
      folder: "task-04-bank-account-challenge",
      pkgName: "day-27-task-04-bank-account-challenge",
      srcFile: "bankAccount.js",
      testFile: "bankAccount.test.js",
      evalTitle: "Bank account challenge",
      src: `export class BankAccount {
  #balance = 0;
  static count = 0;

  constructor(opening = 0) {
    // TODO(Day27-task04): initialize #balance (finite number else 0); increment static count
  }

  withdraw(amount) {
    // TODO(Day27-task04): finite positive; cannot go below 0; return amount actually withdrawn
    return 0;
  }

  static created() {
    // TODO(Day27-task04): return how many accounts were constructed
    return 0;
  }
}
`,
      test: `import { describe, expect, it } from "vitest";
import { BankAccount } from "../src/bankAccount.js";

describe("BankAccount challenge", () => {
  it("tracks static construction count", () => {
    const start = BankAccount.created();
    const a = new BankAccount(10);
    const b = new BankAccount();
    expect(BankAccount.created()).toBe(start + 2);
    expect(a.withdraw(3)).toBe(3);
    expect(a.withdraw(100)).toBe(7);
  });
});
`,
      instructions: taskInstr(
        27,
        4,
        "Bank account challenge",
        "Combine **private balance**, **withdraw rules**, and a **static** construction counter.",
        ["Integrate static and private fields in one small type."],
        ["1. \`BankAccount.created()\` returns number of \`new\` calls tracked.", "2. \`withdraw\` caps at available funds."],
      ),
    },
  ],
});

/* -------------------------------------------------------------------------- */
/* Day 28 — Prototypes                                                        */
/* -------------------------------------------------------------------------- */

writeDay({
  day: 28,
  readme: dayReadme(28, "Prototypes: `Object.create`, Chains, and `instanceof`", [
    "Explain **prototype links** created by \`Object.create\` and constructors.",
    "Use **delegation** to share behavior without copying methods onto every object.",
    "Apply \`instanceof\` with the mental model of **constructor.prototype** checks.",
  ], [
    "task-01-object-create-delegation",
    "task-02-prototype-chain-lookup",
    "task-03-instanceof-constructors",
    "task-04-delegate-chain-challenge",
  ]),
  theory: `# Day 28 — Prototypes: \`Object.create\`, Chains, and \`instanceof\`

**Primary theme:** Prototype chain lookup and delegation  
**Estimated study time:** 2–4 hours theory + 4–8 hours tasks  
**Instruction alignment:** Maps to *Prototypal inheritance: prototypes, constructor patterns, \`instanceof\`*.

---

## Overview

Each object may link to a **prototype** object for property/method lookup. \`Object.create(proto)\` sets \`[[Prototype]]\` explicitly. \`instanceof\` asks whether \`Constructor.prototype\` appears in an object’s chain.

---

## Day roadmap

1. \`[[Prototype]]\` vs \`prototype\` property
2. \`Object.create\`
3. \`instanceof\`
4. Common mistakes
5. Further reading (MDN)
6. Answers

---

## \`Object.create\`

### What it is

Creates a new object with a specified prototype.

#### Examples

\`\`\`js
const base = { hi() { return "hi"; } };
const child = Object.create(base);
\`\`\`

#### Quick checks

1. Does \`Object.create(null)\` have a prototype?

---

## \`instanceof\`

### What it is

\`obj instanceof C\` checks the prototype chain for \`C.prototype\`.

#### Quick checks

1. Can \`instanceof\` lie if \`prototype\` is reassigned?

---

## Further reading

- MDN: [\`Object.create\`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/create)
- MDN: [\`instanceof\`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/instanceof)

---

## Answers (self-test)

1. **\`Object.create(null)\`:** no ordinary prototype (good for dictionaries).
2. **Reassigned \`prototype\`:** yes, \`instanceof\` can become inconsistent—avoid mutating \`prototype\` after instances exist.
`,
  tasks: [
    {
      index: 1,
      folder: "task-01-object-create-delegation",
      pkgName: "day-28-task-01-object-create-delegation",
      srcFile: "delegateNoise.js",
      testFile: "delegateNoise.test.js",
      evalTitle: "Object.create delegation",
      src: `const noiseMethods = {
  label() {
    return this.kind;
  },
};

export function createNoisyThing(kind) {
  // TODO(Day28-task01): return Object.create(noiseMethods) with own property kind (string)
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { createNoisyThing } from "../src/delegateNoise.js";

describe("createNoisyThing", () => {
  it("delegates label()", () => {
    const dog = createNoisyThing("dog");
    expect(dog.label()).toBe("dog");
  });
});
`,
      instructions: taskInstr(
        28,
        1,
        "Delegation with Object.create",
        "Use \`Object.create\` to share methods via the prototype chain.",
        ["Prototype delegation vs copying properties."],
        ["1. Returned object inherits \`label\` from \`noiseMethods\`.", "2. Each instance stores its own \`kind\`."],
      ),
    },
    {
      index: 2,
      folder: "task-02-prototype-chain-lookup",
      pkgName: "day-28-task-02-prototype-chain-lookup",
      srcFile: "chainLookup.js",
      testFile: "chainLookup.test.js",
      evalTitle: "Prototype chain",
      src: `export function readInherited(obj, key) {
  // TODO(Day28-task02): walk prototype chain (Object.getPrototypeOf) until own property key found or null proto; return value or undefined
  return undefined;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { readInherited } from "../src/chainLookup.js";

describe("readInherited", () => {
  it("finds own before inherited", () => {
    const base = { a: 1 };
    const child = Object.assign(Object.create(base), { b: 2 });
    expect(readInherited(child, "b")).toBe(2);
    expect(readInherited(child, "a")).toBe(1);
  });
});
`,
      instructions: taskInstr(
        28,
        2,
        "Prototype chain lookup",
        "Implement a tiny manual lookup along \`[[Prototype]]\`.",
        ["Practice \`Object.getPrototypeOf\`."],
        ["1. Return first own property match walking from \`obj\` outward."],
      ),
    },
    {
      index: 3,
      folder: "task-03-instanceof-constructors",
      pkgName: "day-28-task-03-instanceof-constructors",
      srcFile: "boxes.js",
      testFile: "boxes.test.js",
      evalTitle: "instanceof",
      src: `export function Box(value) {
  if (!(this instanceof Box)) {
    return new Box(value);
  }
  this.value = value;
}

export function isBox(x) {
  // TODO(Day28-task03): return boolean instanceof Box
  return false;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { Box, isBox } from "../src/boxes.js";

describe("Box + instanceof", () => {
  it("works with new", () => {
    expect(isBox(new Box(1))).toBe(true);
  });

  it("callable without new", () => {
    expect(isBox(Box(2))).toBe(true);
  });
});
`,
      instructions: taskInstr(
        28,
        3,
        "`instanceof` with constructors",
        "Guarded constructor pattern + \`instanceof\` check.",
        ["Understand \`new\` vs call-without-\`new\` guard."],
        ["1. \`isBox\` uses \`instanceof\`."],
      ),
    },
    {
      index: 4,
      folder: "task-04-delegate-chain-challenge",
      pkgName: "day-28-task-04-delegate-chain-challenge",
      srcFile: "composeProtos.js",
      testFile: "composeProtos.test.js",
      evalTitle: "Delegate chain challenge",
      src: `export function composeDefaults(base, defaults) {
  // TODO(Day28-task04): return Object.create(base) then assign own enumerable keys from defaults object (shallow)
  return null;
}
`,
      test: `import { describe, expect, it } from "vitest";
import { composeDefaults } from "../src/composeProtos.js";

describe("composeDefaults", () => {
  it("inherits missing keys from base", () => {
    const base = { a: 1, b: 2 };
    const obj = composeDefaults(base, { b: 9, c: 3 });
    expect(obj.b).toBe(9);
    expect(obj.a).toBe(1);
    expect(Object.prototype.hasOwnProperty.call(obj, "a")).toBe(false);
  });
});
`,
      instructions: taskInstr(
        28,
        4,
        "Compose prototypes challenge",
        "Combine \`Object.create\` with shallow own properties for overrides.",
        ["Prototype + own properties precedence."],
        ["1. Returned object uses \`base\` as prototype.", "2. Assign defaults as own properties."],
      ),
    },
  ],
});

console.log("Generated Days 27–28");
