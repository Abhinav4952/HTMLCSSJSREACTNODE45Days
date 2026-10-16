package com.javaprep.day43.task02;

import java.util.concurrent.atomic.AtomicInteger;

/** PROVIDED. Simulated downstream: fails the first {@code failures} calls, then answers "ok". */
public class FlakyDownstream {

    private final int failures;
    private final AtomicInteger calls = new AtomicInteger();

    public FlakyDownstream(int failures) {
        this.failures = failures;
    }

    public String call() {
        if (calls.incrementAndGet() <= failures) {
            throw new DownstreamException("downstream failure #" + calls.get());
        }
        return "ok";
    }

    public int calls() {
        return calls.get();
    }
}
