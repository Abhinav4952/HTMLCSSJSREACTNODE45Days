package com.javaprep.day41.task03;

import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.stereotype.Component;

/** PROVIDED: pretend work queue statistics (capacity 100). */
@Component
public class QueueStats {
    private final AtomicInteger depth = new AtomicInteger();

    public int getDepth() {
        return depth.get();
    }

    public void setDepth(int value) {
        depth.set(value);
    }
}
