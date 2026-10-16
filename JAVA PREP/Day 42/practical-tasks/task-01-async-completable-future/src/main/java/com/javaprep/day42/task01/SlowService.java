package com.javaprep.day42.task01;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicReference;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

@Service
public class SlowService {

    private final AtomicReference<String> lastThread = new AtomicReference<>();

    public String lastThread() {
        return lastThread.get();
    }

    /** Runs on the async executor and reports the name of the thread that executed it. */
    // TODO(Day42-task01): run asynchronously (@Async)
    public CompletableFuture<String> threadName() {
        // TODO(Day42-task01): return a completed future with Thread.currentThread().getName()
        throw new UnsupportedOperationException("TODO(Day42-task01): return a completed future with Thread.currentThread().getName()");
    }

    /** Simulates slow work (about 50 ms) and returns n * n. */
    // TODO(Day42-task01): run asynchronously (@Async)
    public CompletableFuture<Integer> square(int n) {
        // TODO(Day42-task01): sleep ~50 ms (restore the interrupt flag when interrupted) and complete with n*n
        throw new UnsupportedOperationException("TODO(Day42-task01): sleep ~50 ms (restore the interrupt flag when interrupted) and complete with n*n");
    }

    /** Returns a FAILED future with IllegalStateException("async boom") (do not throw). */
    // TODO(Day42-task01): run asynchronously (@Async)
    public CompletableFuture<Integer> failing() {
        // TODO(Day42-task01): failedFuture
        throw new UnsupportedOperationException("TODO(Day42-task01): failedFuture");
    }

    /** Fire-and-forget: stores the executing thread name in lastThread, then counts the latch down. */
    // TODO(Day42-task01): run asynchronously (@Async)
    public void fireAndForget(CountDownLatch latch) {
        // TODO(Day42-task01): record the thread name and count down
        throw new UnsupportedOperationException("TODO(Day42-task01): record the thread name and count down");
    }
}
