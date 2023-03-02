import { validatePassword } from "@components/user/userValidation";

import { describe, it, expect } from "vitest";

describe("userValidation", () => {
  it("should validate a password", () => {
    expect(validatePassword("password", "")).toEqual({
      valid: false,
      message: "Please enter a password with at least 12 characters",
    });
  });
});
