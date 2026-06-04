import { describe, expect, it } from "vitest";
import { ledgerBalance } from "../src/reduceLab.js";

describe("ledgerBalance", () => {
  it("sums credits and subtracts debits", () => {
    expect(
      ledgerBalance([
        { kind: "credit", amount: 10 },
        { kind: "debit", amount: 3 },
        { kind: "credit", amount: 2 },
      ]),
    ).toBe(9);
  });

  it("ignores invalid rows", () => {
    expect(
      ledgerBalance([
        { kind: "credit", amount: 5 },
        { kind: "loan", amount: 99 },
        { kind: "debit", amount: -1 },
        { kind: "debit", amount: Number.NaN },
        null,
        "x",
      ]),
    ).toBe(5);
  });

  it("rejects non-arrays", () => {
    expect(ledgerBalance(null)).toBeNull();
  });
});
