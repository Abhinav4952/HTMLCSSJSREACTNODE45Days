import { describe, expect, it } from "vitest";
import { buildSecretBag } from "../src/symLab.js";

describe("buildSecretBag", () => {
  it("stores by symbol key", () => {
    const bag = buildSecretBag();
    bag.set("token", "abc");
    expect(bag.get("token")).toBe("abc");
  });
});
