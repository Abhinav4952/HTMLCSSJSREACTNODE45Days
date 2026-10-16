package com.javaprep.day42.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class AsyncTest {

    @Autowired
    SlowService service;
    @Autowired
    Aggregator aggregator;

    @Test
    void serviceIsProxiedForAsync() {
        assertThat(AopUtils.isAopProxy(service)).isTrue();
    }

    @Test
    void runsOnExecutorThread() throws Exception {
        String caller = Thread.currentThread().getName();
        String worker = service.threadName().get(5, TimeUnit.SECONDS);
        assertThat(worker).isNotEqualTo(caller).startsWith("task-");
    }

    @Test
    void futureCompletesWithValue() throws Exception {
        assertThat(service.square(7).get(5, TimeUnit.SECONDS)).isEqualTo(49);
    }

    @Test
    void failureTravelsInsideTheFuture() {
        assertThatThrownBy(() -> service.failing().get(5, TimeUnit.SECONDS))
                .isInstanceOf(ExecutionException.class).hasCauseInstanceOf(IllegalStateException.class).hasRootCauseMessage("async boom");
    }

    @Test
    void fireAndForgetRunsInBackground() throws Exception {
        CountDownLatch latch = new CountDownLatch(1);
        service.fireAndForget(latch);
        assertThat(latch.await(5, TimeUnit.SECONDS)).isTrue();
        assertThat(service.lastThread()).startsWith("task-").isNotEqualTo(Thread.currentThread().getName());
    }

    @Test
    void aggregatorCombinesFutures() {
        assertThat(aggregator.sumOfSquares(List.of(1, 2, 3, 4))).isEqualTo(30);
        assertThat(aggregator.sumOfSquares(List.of())).isZero();
    }
}
