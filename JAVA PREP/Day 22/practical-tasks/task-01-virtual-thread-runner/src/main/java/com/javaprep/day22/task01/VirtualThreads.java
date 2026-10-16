package com.javaprep.day22.task01;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.Semaphore;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.atomic.AtomicInteger;

/** Helpers around Java 21 virtual threads. */
public final class VirtualThreads {

    /** Result of {@link #runLimited(int, int, long)}. */
    public record Stats(int completed, int peakConcurrency) {
    }

    private VirtualThreads() {
    }

    public static Thread start(String name, Runnable body) {
        // TODO(Day22-task01): Thread.ofVirtual().name(name).start(body) and return the started thread
        throw new UnsupportedOperationException("TODO(Day22-task01): start");
    }

    public static boolean isVirtual(Thread thread) {
        // TODO(Day22-task01): return thread.isVirtual()
        throw new UnsupportedOperationException("TODO(Day22-task01): isVirtual");
    }

    public static <T> List<T> runAll(List<Callable<T>> tasks) throws InterruptedException, ExecutionException {
        // TODO(Day22-task01): try-with-resources on Executors.newVirtualThreadPerTaskExecutor(); submit every task, then collect future.get() in input order
        throw new UnsupportedOperationException("TODO(Day22-task01): runAll");
    }

    public static ThreadFactory factory(String prefix) {
        // TODO(Day22-task01): Thread.ofVirtual().name(prefix, 0).factory() so names are prefix0, prefix1, ...
        throw new UnsupportedOperationException("TODO(Day22-task01): factory");
    }

    public static Stats runLimited(int tasks, int permits, long sleepMillis) {
        // TODO(Day22-task01): IllegalArgumentException if permits <= 0 or tasks < 0; Semaphore(permits); one virtual thread per task: acquire, bump running/peak (AtomicInteger), sleep, decrement, completed++, release in finally; close the executor to wait
        throw new UnsupportedOperationException("TODO(Day22-task01): runLimited");
    }
}
