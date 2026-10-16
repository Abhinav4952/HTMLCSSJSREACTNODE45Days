package com.javaprep.day28.task01;

import org.springframework.stereotype.Repository;

/** PROVIDED bean: a trivial repository returning "Hello". */
@Repository
public class InMemoryMessageRepository implements MessageRepository {
    @Override
    public String greetingPrefix() {
        return "Hello";
    }
}
