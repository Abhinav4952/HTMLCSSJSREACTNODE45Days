import { describe, expect, it } from "vitest";
import { createDeferred } from "../src/defer.js";

describe("createDeferred", () => {
  it("resolves externally", async () => {
    const d = createDeferred();
    d.resolve(7);
    await expect(d.promise).resolves.toBe(7);
  });
});
