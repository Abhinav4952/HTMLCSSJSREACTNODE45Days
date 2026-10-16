package com.javaprep.day39.task03;

import java.util.Optional;

public interface UserLookup {
    Optional<String> findEmail(long userId);
}
