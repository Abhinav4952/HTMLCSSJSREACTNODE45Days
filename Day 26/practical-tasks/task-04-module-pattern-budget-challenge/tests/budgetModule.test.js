import { describe, expect, it } from "vitest";
import { createBudget } from "../src/budgetModule.js";

describe("createBudget", () => {
  it("deposits and reads balance", () => {
    const b = createBudget(10);
    expect(b.balance()).toBe(10);
    expect(b.deposit(5)).toBe(15);
  });

  it("withdraws up to available funds", () => {
    const b = createBudget(10);
    expect(b.withdraw(4)).toBe(4);
    expect(b.balance()).toBe(6);
    expect(b.withdraw(100)).toBe(6);
    expect(b.balance()).toBe(0);
  });

  it("ignores invalid amounts", () => {
    const b = createBudget(0);
    b.deposit(-5);
    b.deposit(Number.NaN);
    expect(b.balance()).toBe(0);
  });
});
