package com.javaprep.day37.task02;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/** PROVIDED in-memory user table. */
public class UserStore {
    private final Map<String, UserRecord> users = new HashMap<>();

    public UserStore add(UserRecord user) {
        users.put(user.username().toLowerCase(), user);
        return this;
    }

    public Optional<UserRecord> find(String username) {
        return Optional.ofNullable(username == null ? null : users.get(username.toLowerCase()));
    }
}
