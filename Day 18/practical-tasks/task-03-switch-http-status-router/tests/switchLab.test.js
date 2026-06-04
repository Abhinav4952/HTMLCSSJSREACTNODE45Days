import { describe, expect, it } from "vitest";
import { httpStatusFamily } from "../src/switchLab.js";

describe("httpStatusFamily", () => {
  it("buckets common codes", () => {
    expect(httpStatusFamily(102)).toBe("informational");
    expect(httpStatusFamily(200)).toBe("success");
    expect(httpStatusFamily(204)).toBe("success");
    expect(httpStatusFamily(301)).toBe("redirect");
    expect(httpStatusFamily(404)).toBe("client_error");
    expect(httpStatusFamily(500)).toBe("server_error");
  });

  it("rejects non-integers and out-of-range codes", () => {
    expect(httpStatusFamily(99)).toBe("invalid");
    expect(httpStatusFamily(600)).toBe("invalid");
    expect(httpStatusFamily(200.5)).toBe("invalid");
    expect(httpStatusFamily(Number.NaN)).toBe("invalid");
    expect(httpStatusFamily(null)).toBe("invalid");
  });
});
