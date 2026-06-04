import { describe, expect, it } from "vitest";
import { normalizeProfile, parsePair } from "../src/destructureLab.js";

describe("normalizeProfile", () => {
  it("renames email and defaults role", () => {
    expect(
      normalizeProfile({ email: " ada@example.com ", displayName: " Ada " }),
    ).toEqual({
      primaryEmail: "ada@example.com",
      displayName: "Ada",
      role: "viewer",
    });
  });

  it("honors explicit role", () => {
    expect(
      normalizeProfile({ email: "x@y.z", role: "admin" }),
    ).toEqual({
      primaryEmail: "x@y.z",
      displayName: "",
      role: "admin",
    });
  });

  it("rejects bad email", () => {
    expect(normalizeProfile({ email: "   " })).toBeNull();
  });
});

describe("parsePair", () => {
  it("splits and trims", () => {
    expect(parsePair(" a : b ")).toEqual({ left: "a", right: "b" });
  });

  it("defaults missing right side", () => {
    expect(parsePair("only")).toEqual({ left: "only", right: "" });
  });
});
