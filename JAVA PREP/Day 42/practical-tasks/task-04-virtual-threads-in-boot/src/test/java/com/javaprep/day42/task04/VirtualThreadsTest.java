package com.javaprep.day42.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.TimeUnit;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.env.Environment;

@SpringBootTest
class VirtualThreadsTest {

    @Autowired
    ThreadProbe probe;
    @Autowired
    Environment env;

    @Test
    void propertyEnablesVirtualThreads() {
        assertThat(env.getProperty("spring.threads.virtual.enabled", Boolean.class)).isTrue();
    }

    @Test
    void asyncWorkRunsOnVirtualThreads() throws Exception {
        assertThat(probe.runsOnVirtualThread().get(5, TimeUnit.SECONDS)).isTrue();
        assertThat(probe.workerName().get(5, TimeUnit.SECONDS)).startsWith("task-");
    }

    @Test
    void runAllKeepsInputOrderAndUsesVirtualThreads() throws Exception {
        List<Callable<String>> tasks = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            int n = i;
            tasks.add(() -> n + ":" + Thread.currentThread().isVirtual());
        }
        assertThat(VirtualThreadRunner.runAll(tasks)).containsExactly("0:true", "1:true", "2:true", "3:true", "4:true");
    }

    @Test
    void thousandsOfBlockingTasksAreCheap() throws Exception {
        List<Callable<Integer>> tasks = IntStream.range(0, 2000).<Callable<Integer>>mapToObj(i -> () -> {
            Thread.sleep(Duration.ofMillis(200));
            return i;
        }).toList();
        long t0 = System.nanoTime();
        List<Integer> out = VirtualThreadRunner.runAll(tasks);
        long ms = (System.nanoTime() - t0) / 1_000_000;
        assertThat(out).hasSize(2000).startsWith(0, 1, 2);
        assertThat(ms).as("2000 x 200ms sleeps should overlap").isLessThan(5000);
    }

    @Test
    void namedFactoryCreatesNamedVirtualThreads() throws Exception {
        Thread t = VirtualThreadRunner.namedFactory("vt-").newThread(() -> { });
        assertThat(t.isVirtual()).isTrue();
        assertThat(t.getName()).isEqualTo("vt-0");
        assertThat(t.getState()).isEqualTo(Thread.State.NEW);
        Thread second = VirtualThreadRunner.namedFactory("vt-").newThread(() -> { });
        assertThat(second.getName()).isEqualTo("vt-0");
    }

    @Test
    void testThreadIsPlatformThread() {
        assertThat(VirtualThreadRunner.onVirtualThread()).isFalse();
    }
}
