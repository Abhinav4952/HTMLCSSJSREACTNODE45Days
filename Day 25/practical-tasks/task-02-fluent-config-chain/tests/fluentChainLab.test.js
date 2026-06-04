import { describe, expect, it } from "vitest";
import { createQueryBuilder } from "../src/fluentChainLab.js";

describe("createQueryBuilder", () => {
  it("chains select/from/build", () => {
    const sql = createQueryBuilder().select(["id", "name"]).from("users").build();
    expect(sql).toBe("SELECT id, name FROM users");
  });

  it("returns empty string when incomplete", () => {
    expect(createQueryBuilder().build()).toBe("");
  });
});
