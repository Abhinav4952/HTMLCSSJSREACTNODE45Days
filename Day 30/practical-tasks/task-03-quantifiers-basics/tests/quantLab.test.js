import { describe, expect, it } from "vitest";
import { splitCommaList } from "../src/quantLab.js";

describe("splitCommaList", () => {
  it("splits comma lists", () => {
    expect(splitCommaList("a, b ,c")).toEqual(["a", "b", "c"]);
  });
});
