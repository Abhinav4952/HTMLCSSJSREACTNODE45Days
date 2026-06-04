import { describe, expect, it } from "vitest";
import { redactEmails } from "../src/replaceGroups.js";

describe("redactEmails", () => {
  it("uses capture groups", () => {
    expect(redactEmails("mail ada@example.com end")).toBe("mail <redacted:example.com> end");
  });
});
