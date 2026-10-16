package com.javaprep.day37.task02;

import java.util.List;

public record UserRecord(String username, String passwordHash, List<String> roles, boolean enabled) {
}
