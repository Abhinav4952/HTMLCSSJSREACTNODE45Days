import { describe, expect, it } from "vitest";
import { labeler, maxWithApply, renderWithHost } from "../src/callApplyLab.js";

describe("renderWithHost", () => {
  it("borrows labeler.render via call", () => {
    const host = { brand: "acme", version: 7 };
    expect(renderWithHost(host)).toBe("acme-7");
    expect(labeler.render.call(host)).toBe("acme-7");
  });
});

describe("maxWithApply", () => {
  it("uses apply with Math.max", () => {
    expect(maxWithApply([3, 9, 2])).toBe(9);
  });
});
