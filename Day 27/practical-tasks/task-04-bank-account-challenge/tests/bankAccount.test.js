import { describe, expect, it } from "vitest";
import { BankAccount } from "../src/bankAccount.js";

describe("BankAccount challenge", () => {
  it("tracks static construction count", () => {
    const start = BankAccount.created();
    const a = new BankAccount(10);
    const b = new BankAccount();
    expect(BankAccount.created()).toBe(start + 2);
    expect(a.withdraw(3)).toBe(3);
    expect(a.withdraw(100)).toBe(7);
  });
});
