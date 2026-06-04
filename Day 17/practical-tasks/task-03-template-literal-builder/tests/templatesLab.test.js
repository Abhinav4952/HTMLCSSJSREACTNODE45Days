import { describe, expect, it } from "vitest";
import { formatIssue } from "../src/templatesLab.js";

describe("formatIssue", () => {
  it("formats a multiline issue summary", () => {
    const text = formatIssue({
      id: 42,
      title: "Flaky canary",
      severity: "high",
      url: "https://example.com/issues/42",
    });

    expect(text).toBe(
      [
        "ISSUE 42: Flaky canary",
        "Severity: HIGH",
        "Link: https://example.com/issues/42",
        "",
      ].join("\n"),
    );
  });

  it("uppercases severity defensively", () => {
    const text = formatIssue({
      id: "OPS-1",
      title: "Disk pressure",
      severity: "Med",
      url: "https://status.example.com/OPS-1",
    });

    expect(text).toContain("Severity: MED");
  });
});
