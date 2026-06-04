import { describe, expect, it } from "vitest";
import { createIndexHandlers } from "../src/loopClosureHandlers.js";

describe("createIndexHandlers", () => {
  it("captures per-iteration index", () => {
    const fns = createIndexHandlers(3);
    expect(fns.map((f) => f())).toEqual([0, 1, 2]);
  });

  it("allows empty list", () => {
    expect(createIndexHandlers(0)).toEqual([]);
  });

  it("rejects invalid counts", () => {
    expect(createIndexHandlers(-1)).toBeNull();
    expect(createIndexHandlers(3.5)).toBeNull();
  });
});
