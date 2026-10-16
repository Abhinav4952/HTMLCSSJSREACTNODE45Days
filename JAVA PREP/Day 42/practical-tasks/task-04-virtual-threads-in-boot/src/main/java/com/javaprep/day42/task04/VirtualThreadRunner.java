package com.javaprep.day42.task04;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ThreadFactory;

public final class VirtualThreadRunner {

    private VirtualThreadRunner() {
    }

    /** Runs all callables, each on its OWN virtual thread (newVirtualThreadPerTaskExecutor); results in input order. */
    public static <T> List<T> runAll(List<Callable<T>> tasks) throws InterruptedException, ExecutionException {
        // TODO(Day42-task04): use try-with-resources on the executor, invokeAll, then collect future.get() in order
        throw new UnsupportedOperationException("TODO(Day42-task04): use try-with-resources on the executor, invokeAll, then collect future.get() in order");
    }

    /** ThreadFactory creating UNSTARTED virtual threads named prefix0, prefix1, ... */
    public static ThreadFactory namedFactory(String prefix) {
        // TODO(Day42-task04): Thread.ofVirtual().name(prefix, 0).factory()
        throw new UnsupportedOperationException("TODO(Day42-task04): Thread.ofVirtual().name(prefix, 0).factory()");
    }

    /** True when the current thread is virtual. */
    public static boolean onVirtualThread() {
        // TODO(Day42-task04): ask the current thread
        throw new UnsupportedOperationException("TODO(Day42-task04): ask the current thread");
    }
}
