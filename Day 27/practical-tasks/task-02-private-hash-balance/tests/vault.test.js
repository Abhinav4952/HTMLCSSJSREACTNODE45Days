import { describe, expect, it } from "vitest";
import { Vault } from "../src/vault.js";

describe("Vault", () => {
  it("deposits", () => {
    const v = new Vault(10);
    expect(v.balance).toBe(10);
    expect(v.deposit(5)).toBe(15);
  });

  it("rejects bad opening", () => {
    const v = new Vault(Number.NaN);
    expect(v.balance).toBe(0);
  });
});
