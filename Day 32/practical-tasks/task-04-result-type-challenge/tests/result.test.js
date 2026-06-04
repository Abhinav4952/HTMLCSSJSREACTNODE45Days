import { describe, expect, it } from "vitest";
import { divide } from "../src/result.js";

describe("divide", () => {
  it("returns ok result", () => {
    expect(divide(10, 2)).toEqual({ ok: true, value: 5 });
  });

  it("returns error result", () => {
    expect(divide(1, 0)).toEqual({ ok: false, error: "division by zero" });
  });
});
