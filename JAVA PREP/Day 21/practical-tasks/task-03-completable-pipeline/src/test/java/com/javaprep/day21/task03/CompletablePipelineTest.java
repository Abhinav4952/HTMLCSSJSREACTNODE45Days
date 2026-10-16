package com.javaprep.day21.task03;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(20)
class CompletablePipelineTest {

    /** Runs tasks on the calling thread so the tests are deterministic. */
    private static final Executor DIRECT = Runnable::run;

    @Test
    void r1_pipelineTransformsText() throws Exception {
        assertThat(CompletablePipeline.pipeline(() -> "  hello ", DIRECT).get(5, TimeUnit.SECONDS)).isEqualTo("HELLO");
    }

    @Test
    void r1_pipelinePropagatesSourceFailure() {
        CompletableFuture<String> f = CompletablePipeline.pipeline(() -> {
            throw new IllegalStateException("source down");
        }, DIRECT);
        assertThat(f.isCompletedExceptionally()).isTrue();
    }

    @Test
    void r2_combineSums() {
        CompletableFuture<Integer> a = CompletableFuture.completedFuture(20);
        CompletableFuture<Integer> b = CompletableFuture.supplyAsync(() -> 22);
        assertThat(CompletablePipeline.combine(a, b).join()).isEqualTo(42);
    }

    @Test
    void r2_combineWaitsForBoth() {
        CompletableFuture<Integer> a = new CompletableFuture<>();
        CompletableFuture<Integer> b = CompletableFuture.completedFuture(1);
        CompletableFuture<Integer> sum = CompletablePipeline.combine(a, b);
        assertThat(sum.isDone()).isFalse();
        a.complete(9);
        assertThat(sum.join()).isEqualTo(10);
    }

    @Test
    void r3_allInOrderKeepsInputOrder() {
        CompletableFuture<Integer> first = new CompletableFuture<>();
        CompletableFuture<Integer> second = CompletableFuture.completedFuture(2);
        CompletableFuture<Integer> third = CompletableFuture.completedFuture(3);
        CompletableFuture<List<Integer>> all = CompletablePipeline.allInOrder(List.of(first, second, third));
        assertThat(all.isDone()).isFalse();
        first.complete(1);
        assertThat(all.join()).containsExactly(1, 2, 3);
    }

    @Test
    void r3_allInOrderEmpty() {
        assertThat(CompletablePipeline.allInOrder(List.of()).join()).isEmpty();
    }

    @Test
    void r4_fallbackOnFailureAndNoFallbackOnSuccess() {
        assertThat(CompletablePipeline.withFallback(() -> 5, DIRECT, -1).join()).isEqualTo(5);
        assertThat(CompletablePipeline.withFallback(() -> {
            throw new IllegalStateException("x");
        }, DIRECT, -1).join()).isEqualTo(-1);
    }

    @Test
    void r5_chainComposesDependentCalls() {
        CompletableFuture<String> email = CompletablePipeline.chain("42",
                id -> CompletableFuture.completedFuture("user-" + id),
                user -> CompletableFuture.completedFuture(user + "@example.org"));
        assertThat(email.join()).isEqualTo("user-42@example.org");
    }

    @Test
    void r5_chainFailsWhenFirstLookupFails() {
        CompletableFuture<String> email = CompletablePipeline.chain("x",
                id -> CompletableFuture.failedFuture(new IllegalArgumentException("no such user")),
                user -> CompletableFuture.completedFuture(user + "@example.org"));
        assertThat(email.isCompletedExceptionally()).isTrue();
    }

    @Test
    void r6_timeoutUsesTheDefault() {
        CompletableFuture<Integer> never = new CompletableFuture<>();
        assertThat(CompletablePipeline.withTimeout(never, 50, -1).join()).isEqualTo(-1);
        CompletableFuture<Integer> quick = CompletableFuture.completedFuture(8);
        assertThat(CompletablePipeline.withTimeout(quick, 50, -1).join()).isEqualTo(8);
    }

    @Test
    void r7_describeUnwrapsCompletionException() {
        assertThat(CompletablePipeline.describe(CompletableFuture.completedFuture(5)).join()).isEqualTo("ok:5");
        CompletableFuture<Integer> direct = CompletableFuture.failedFuture(new IllegalStateException("x"));
        assertThat(CompletablePipeline.describe(direct).join()).isEqualTo("error:IllegalStateException");
        CompletableFuture<Integer> derived = CompletableFuture.<Integer>supplyAsync(() -> {
            throw new IllegalArgumentException("y");
        }, DIRECT).thenApply(v -> v + 1);
        assertThat(CompletablePipeline.describe(derived).join()).isEqualTo("error:IllegalArgumentException");
    }
}
