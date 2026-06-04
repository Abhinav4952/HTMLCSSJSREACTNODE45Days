import { describe, expect, it } from "vitest";
import { bindGetter, strictStandaloneThisType } from "../src/strictThisChallenge.js";

describe("strictStandaloneThisType", () => {
  it("shows undefined this in strict standalone calls", () => {
    expect(strictStandaloneThisType()).toBe("undefined");
  });
});

describe("bindGetter", () => {
  it("fixes lost context for extracted methods", () => {
    const view = {
      title: "Docs",
      getHeading() {
        return `== ${this.title} ==`;
      },
    };
    const safe = bindGetter(view.getHeading, view);
    expect(safe()).toBe("== Docs ==");
  });
});
