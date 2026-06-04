import { describe, expect, it } from "vitest";
import { firstTagContents } from "../src/lazyLab.js";

describe("firstTagContents", () => {
  it("non-greedy first match", () => {
    expect(firstTagContents("<div>hi</div><div>bye</div>")).toBe("hi");
  });
});
