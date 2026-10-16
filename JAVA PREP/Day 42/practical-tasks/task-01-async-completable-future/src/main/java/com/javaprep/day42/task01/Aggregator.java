package com.javaprep.day42.task01;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import org.springframework.stereotype.Component;

/** Calls the async service THROUGH the proxy (separate bean) so @Async really applies. */
@Component
public class Aggregator {

    private final SlowService slow;

    public Aggregator(SlowService slow) {
        this.slow = slow;
    }

    /** Starts all squares first (so they overlap), then waits for all of them and sums the results. */
    public int sumOfSquares(List<Integer> numbers) {
        // TODO(Day42-task01): start every future before joining any; allOf(...).join(); sum
        throw new UnsupportedOperationException("TODO(Day42-task01): start every future before joining any; allOf(...).join(); sum");
    }
}
