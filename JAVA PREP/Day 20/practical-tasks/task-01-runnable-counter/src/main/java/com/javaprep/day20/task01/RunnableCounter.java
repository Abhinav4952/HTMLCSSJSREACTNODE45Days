package com.javaprep.day20.task01;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;

/** Thread basics. */
public final class RunnableCounter {

    private RunnableCounter() {
    }

    public static Runnable incrementTask(Counter counter, int times) {
        // TODO(Day20-task01): return a Runnable that calls counter.increment() exactly times times
        throw new UnsupportedOperationException("TODO(Day20-task01): incrementTask");
    }

    public static int runConcurrently(Counter counter, int threads, int perThread) throws InterruptedException {
        // TODO(Day20-task01): validate (threads > 0, perThread >= 0), start threads named counter-0.. each running incrementTask, join ALL of them, then return counter.get()
        throw new UnsupportedOperationException("TODO(Day20-task01): runConcurrently");
    }

    public static Thread startNamed(String name, Runnable task) {
        // TODO(Day20-task01): create a Thread with the given name for the task, start it, and return it
        throw new UnsupportedOperationException("TODO(Day20-task01): startNamed");
    }

    public static String executedByWithRun() {
        // TODO(Day20-task01): create a thread named 'worker' whose task records Thread.currentThread().getName(), call run() directly (NOT start) and return the recorded name
        throw new UnsupportedOperationException("TODO(Day20-task01): executedByWithRun");
    }

    public static String executedByWithStart(String name) throws InterruptedException {
        // TODO(Day20-task01): same task but on a Thread called name started with start(); join it and return the recorded name
        throw new UnsupportedOperationException("TODO(Day20-task01): executedByWithStart");
    }
}
