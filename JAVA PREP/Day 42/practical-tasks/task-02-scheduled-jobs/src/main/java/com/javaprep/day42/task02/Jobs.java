package com.javaprep.day42.task02;

import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class Jobs {

    private final AtomicInteger beats = new AtomicInteger();
    private final AtomicInteger cleanups = new AtomicInteger();
    private final AtomicInteger refreshes = new AtomicInteger();

    public int beats() {
        return beats.get();
    }

    public int cleanups() {
        return cleanups.get();
    }

    public int refreshes() {
        return refreshes.get();
    }

    /** Every 5 seconds measured from the END of the previous run (fixedDelay = 5000), first run after 60 seconds (initialDelay = 60000). */
    // TODO(Day42-task02): @Scheduled(fixedDelay = 5000, initialDelay = 60000)
    public void heartbeat() {
        // TODO(Day42-task02): count a beat
        throw new UnsupportedOperationException("TODO(Day42-task02): count a beat");
    }

    /** Every day at 02:00 UTC (cron = "0 0 2 * * *", zone = "UTC"). */
    // TODO(Day42-task02): @Scheduled with the cron expression and zone UTC
    public void nightlyCleanup() {
        // TODO(Day42-task02): count a cleanup
        throw new UnsupportedOperationException("TODO(Day42-task02): count a cleanup");
    }

    /** Fixed RATE taken from the property jobs.refresh-rate (milliseconds, default 60000), first run after 60 seconds. */
    // TODO(Day42-task02): @Scheduled(fixedRateString = "${jobs.refresh-rate:60000}", initialDelay = 60000)
    public void refresh() {
        // TODO(Day42-task02): count a refresh
        throw new UnsupportedOperationException("TODO(Day42-task02): count a refresh");
    }
}
