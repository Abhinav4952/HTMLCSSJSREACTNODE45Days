import { describe, expect, it } from "vitest";
import { ValidationError } from "../src/validationError.js";

describe("ValidationError", () => {
  it("carries field", () => {
    const e = new ValidationError("bad", "email");
    expect(e).toBeInstanceOf(Error);
    expect(e.field).toBe("email");
    expect(e.name).toBe("ValidationError");
  });
});
