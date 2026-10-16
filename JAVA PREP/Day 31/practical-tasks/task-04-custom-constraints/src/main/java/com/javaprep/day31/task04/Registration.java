package com.javaprep.day31.task04;

import jakarta.validation.constraints.NotNull;

public record Registration(@NotNull @StrongPassword String password) {
}
