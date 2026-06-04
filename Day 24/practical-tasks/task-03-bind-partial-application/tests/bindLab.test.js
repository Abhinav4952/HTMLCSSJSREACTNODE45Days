import { describe, expect, it } from "vitest";
import { bindFirstArg, bindMethod } from "../src/bindLab.js";

describe("bindFirstArg", () => {
  it("preserves remaining arity using bind", () => {
    const join = (a, b, c) => `${a}|${b}|${c}`;
    const leadA = bindFirstArg(join, "A");
    expect(leadA("B", "C")).toBe("A|B|C");
  });
});

describe("bindMethod", () => {
  it("binds a method to its object", () => {
    const counter = {
      n: 0,
      bump() {
        this.n += 1;
        return this.n;
      },
    };
    const safeBump = bindMethod(counter, "bump");
    expect(safeBump()).toBe(1);
    expect(counter.n).toBe(1);
  });
});
