package com.javaprep.day21.task03;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CompletionException;
import java.util.concurrent.Executor;
import java.util.concurrent.TimeUnit;
import java.util.function.Function;
import java.util.function.Supplier;

/** CompletableFuture composition. */
public final class CompletablePipeline {

    private CompletablePipeline() {
    }

    public static CompletableFuture<String> pipeline(Supplier<String> source, Executor executor) {
        // TODO(Day21-task03): supplyAsync(source, executor) then thenApply(trim) then thenApply(toUpperCase)
        throw new UnsupportedOperationException("TODO(Day21-task03): pipeline");
    }

    public static CompletableFuture<Integer> combine(CompletableFuture<Integer> a, CompletableFuture<Integer> b) {
        // TODO(Day21-task03): a.thenCombine(b, Integer::sum)
        throw new UnsupportedOperationException("TODO(Day21-task03): combine");
    }

    public static CompletableFuture<List<Integer>> allInOrder(List<CompletableFuture<Integer>> futures) {
        // TODO(Day21-task03): CompletableFuture.allOf(...) then collect each future's join() preserving the input order (empty list gives an already completed empty result)
        throw new UnsupportedOperationException("TODO(Day21-task03): allInOrder");
    }

    public static CompletableFuture<Integer> withFallback(Supplier<Integer> risky, Executor executor, int fallback) {
        // TODO(Day21-task03): supplyAsync(risky, executor).exceptionally(ex -> fallback)
        throw new UnsupportedOperationException("TODO(Day21-task03): withFallback");
    }

    public static CompletableFuture<String> chain(String id,
                                                  Function<String, CompletableFuture<String>> lookupUser,
                                                  Function<String, CompletableFuture<String>> lookupEmail) {
        // TODO(Day21-task03): lookupUser.apply(id) then thenCompose(lookupEmail) - NOT thenApply (that would nest futures)
        throw new UnsupportedOperationException("TODO(Day21-task03): chain");
    }

    public static CompletableFuture<Integer> withTimeout(CompletableFuture<Integer> future, long millis, int defaultValue) {
        // TODO(Day21-task03): future.completeOnTimeout(defaultValue, millis, MILLISECONDS)
        throw new UnsupportedOperationException("TODO(Day21-task03): withTimeout");
    }

    public static CompletableFuture<String> describe(CompletableFuture<Integer> future) {
        // TODO(Day21-task03): handle((value, ex) -> ...): 'ok:<value>' or 'error:<SimpleName of the root exception>' unwrapping CompletionException
        throw new UnsupportedOperationException("TODO(Day21-task03): describe");
    }
}
