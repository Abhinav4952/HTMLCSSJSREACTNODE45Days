package com.javaprep.day31.task01;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Incoming payload. Rules: name not blank; email valid format; age 18..120; password at least 8 characters. */
public record CreateUserRequest(
        // TODO(Day31-task01): add @NotBlank
        String name,
        // TODO(Day31-task01): add @Email and @NotBlank
        String email,
        // TODO(Day31-task01): add @Min(18) and @Max(120)
        int age,
        // TODO(Day31-task01): add @Size(min = 8)
        String password) {
}
