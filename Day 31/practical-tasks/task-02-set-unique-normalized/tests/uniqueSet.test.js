import { describe, expect, it } from "vitest";
import { uniqueSorted } from "../src/uniqueSet.js";

describe("uniqueSorted", () => {
  it("dedupes", () => {
    expect(uniqueSorted([3, 1, 3, 2])).toEqual([1, 2, 3]);
  });
});
