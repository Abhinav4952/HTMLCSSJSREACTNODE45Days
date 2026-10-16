package com.javaprep.day45.task02;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/** PROVIDED (do not edit). Thread-safe collector the listeners write to and the tests wait on. */
public class ReceivedEvents {

    private final List<String> items = new CopyOnWriteArrayList<>();

    public void add(String item) {
        items.add(item);
    }

    public List<String> snapshot() {
        return List.copyOf(items);
    }

    /** Polls until at least {@code count} items arrived or the timeout elapsed. */
    public boolean awaitCount(int count, Duration timeout) {
        long deadline = System.nanoTime() + timeout.toNanos();
        while (System.nanoTime() < deadline) {
            if (items.size() >= count) {
                return true;
            }
            try {
                Thread.sleep(25);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
        return items.size() >= count;
    }
}
