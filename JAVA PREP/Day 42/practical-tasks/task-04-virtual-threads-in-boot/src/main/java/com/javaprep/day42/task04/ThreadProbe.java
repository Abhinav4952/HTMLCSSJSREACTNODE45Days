package com.javaprep.day42.task04;

import java.util.concurrent.CompletableFuture;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

/** PROVIDED: reports whether @Async work runs on a virtual thread. */
@Service
public class ThreadProbe {

    @Async
    public CompletableFuture<Boolean> runsOnVirtualThread() {
        return CompletableFuture.completedFuture(Thread.currentThread().isVirtual());
    }

    @Async
    public CompletableFuture<String> workerName() {
        return CompletableFuture.completedFuture(Thread.currentThread().getName());
    }
}
