import { describe, expect, it } from "vitest";
import {
  blendRgbOver,
  compareSpecificityParts,
  compoundSpecificityParts,
  effectiveNestedOpacity,
} from "../src/cascadeLab.js";

describe("compoundSpecificityParts", () => {
  it("parses type-only selectors", () => {
    expect(compoundSpecificityParts("div")).toEqual({ ids: 0, classes: 0, types: 1 });
    expect(compoundSpecificityParts("article")).toEqual({ ids: 0, classes: 0, types: 1 });
  });

  it("parses class-only compounds", () => {
    expect(compoundSpecificityParts(".btn")).toEqual({ ids: 0, classes: 1, types: 0 });
    expect(compoundSpecificityParts(".btn.primary")).toEqual({ ids: 0, classes: 2, types: 0 });
  });

  it("parses mixed compounds in different token orders", () => {
    expect(compoundSpecificityParts("p.note.meta#x")).toEqual({ ids: 1, classes: 2, types: 1 });
    expect(compoundSpecificityParts("#app.hero")).toEqual({ ids: 1, classes: 1, types: 0 });
  });

  it("returns null for invalid lab strings", () => {
    expect(compoundSpecificityParts("")).toBeNull();
    expect(compoundSpecificityParts("   ")).toBeNull();
    expect(compoundSpecificityParts(null)).toBeNull();
    expect(compoundSpecificityParts(12)).toBeNull();
    expect(compoundSpecificityParts("div .a")).toBeNull(); // spaces / combinators
    expect(compoundSpecificityParts("div>a")).toBeNull();
    expect(compoundSpecificityParts("DIV")).toBeNull(); // uppercase tag not allowed in lab grammar
    expect(compoundSpecificityParts("div:hover")).toBeNull(); // pseudo not allowed
    expect(compoundSpecificityParts("div#")).toBeNull();
    expect(compoundSpecificityParts("div.")).toBeNull();
  });
});

describe("compareSpecificityParts", () => {
  it("compares ids first", () => {
    expect(
      compareSpecificityParts(
        { ids: 1, classes: 0, types: 0 },
        { ids: 0, classes: 99, types: 99 },
      ),
    ).toBe(1);
    expect(
      compareSpecificityParts(
        { ids: 0, classes: 99, types: 99 },
        { ids: 1, classes: 0, types: 0 },
      ),
    ).toBe(-1);
  });

  it("compares classes when ids tie", () => {
    expect(
      compareSpecificityParts(
        { ids: 1, classes: 2, types: 1 },
        { ids: 1, classes: 3, types: 0 },
      ),
    ).toBe(-1);
    expect(
      compareSpecificityParts(
        { ids: 1, classes: 3, types: 0 },
        { ids: 1, classes: 2, types: 1 },
      ),
    ).toBe(1);
  });

  it("compares types when ids and classes tie", () => {
    expect(
      compareSpecificityParts(
        { ids: 0, classes: 1, types: 2 },
        { ids: 0, classes: 1, types: 1 },
      ),
    ).toBe(1);
  });

  it("returns 0 on full tie", () => {
    expect(
      compareSpecificityParts(
        { ids: 1, classes: 1, types: 1 },
        { ids: 1, classes: 1, types: 1 },
      ),
    ).toBe(0);
  });
});

describe("effectiveNestedOpacity", () => {
  it("multiplies nested opacities", () => {
    expect(effectiveNestedOpacity(0.5, 0.5)).toBeCloseTo(0.25);
    expect(effectiveNestedOpacity(1, 0.25)).toBeCloseTo(0.25);
  });

  it("allows 0 and 1 bounds", () => {
    expect(effectiveNestedOpacity(0, 1)).toBe(0);
    expect(effectiveNestedOpacity(1, 1)).toBe(1);
  });

  it("returns NaN for out-of-range or non-finite inputs", () => {
    expect(effectiveNestedOpacity(1.1, 0.5)).toBeNaN();
    expect(effectiveNestedOpacity(-0.01, 0.5)).toBeNaN();
    expect(effectiveNestedOpacity(0.5, NaN)).toBeNaN();
    expect(effectiveNestedOpacity(Number.POSITIVE_INFINITY, 0.5)).toBeNaN();
  });
});

describe("blendRgbOver", () => {
  it("blends solid colors with alpha", () => {
    expect(blendRgbOver([0, 0, 0], [255, 255, 255], 0.5)).toEqual([128, 128, 128]);
  });

  it("rounds to nearest integer channel", () => {
    expect(blendRgbOver([0, 0, 255], [255, 0, 0], 0.3333333333)).toEqual([85, 0, 170]);
  });

  it("returns bottom/top unchanged at alpha extremes", () => {
    expect(blendRgbOver([1, 2, 3], [9, 8, 7], 0)).toEqual([1, 2, 3]);
    expect(blendRgbOver([1, 2, 3], [9, 8, 7], 1)).toEqual([9, 8, 7]);
  });

  it("returns null for invalid rgb arrays or alpha", () => {
    expect(blendRgbOver(null, [0, 0, 0], 0.5)).toBeNull();
    expect(blendRgbOver([0, 0], [0, 0, 0], 0.5)).toBeNull();
    expect(blendRgbOver([0, 0, 0], [0, 0, 0], 1.01)).toBeNull();
    expect(blendRgbOver([0, 0, 0], [0, 0, 0], -0.01)).toBeNull();
    expect(blendRgbOver([0, 0, NaN], [0, 0, 0], 0.5)).toBeNull();
    expect(blendRgbOver([0.5, 0, 0], [0, 0, 0], 0.5)).toBeNull(); // non-integers
  });
});
