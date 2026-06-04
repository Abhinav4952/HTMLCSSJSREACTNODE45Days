import { describe, expect, it } from "vitest";
import { fetchThenDoubleLater } from "../src/chain.js";

describe("fetchThenDoubleLater", () => {
  it("chains then", async () => {
    await expect(fetchThenDoubleLater(5)).resolves.toBe(10);
  });
});
