package com.javaprep.day42.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.lang.reflect.Method;
import java.time.Duration;
import java.time.LocalDateTime;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.scheduling.annotation.ScheduledAnnotationBeanPostProcessor;
import org.springframework.scheduling.config.CronTask;
import org.springframework.scheduling.config.FixedDelayTask;
import org.springframework.scheduling.config.FixedRateTask;
import org.springframework.scheduling.config.Task;
import org.springframework.scheduling.support.CronExpression;

@SpringBootTest(properties = "jobs.refresh-rate=120000")
class SchedulingTest {

    @Autowired
    ScheduledAnnotationBeanPostProcessor processor;
    @Autowired
    Jobs jobs;

    private List<Task> tasks() {
        return processor.getScheduledTasks().stream().map(t -> t.getTask()).toList();
    }

    @Test
    void threeTasksAreRegistered() {
        assertThat(tasks()).hasSize(3);
    }

    @Test
    void fixedDelayTask() {
        FixedDelayTask t = tasks().stream().filter(FixedDelayTask.class::isInstance).map(FixedDelayTask.class::cast).findFirst().orElseThrow();
        assertThat(t.getIntervalDuration()).isEqualTo(Duration.ofSeconds(5));
        assertThat(t.getInitialDelayDuration()).isEqualTo(Duration.ofSeconds(60));
        assertThat(t.toString()).contains("heartbeat");
    }

    @Test
    void cronTaskAtTwoAmUtc() {
        CronTask t = tasks().stream().filter(CronTask.class::isInstance).map(CronTask.class::cast).findFirst().orElseThrow();
        assertThat(t.getExpression()).isEqualTo("0 0 2 * * *");
        assertThat(CronExpression.parse(t.getExpression()).next(LocalDateTime.of(2025, 1, 1, 12, 0))).isEqualTo(LocalDateTime.of(2025, 1, 2, 2, 0));
        assertThat(t.toString()).contains("nightlyCleanup");
    }

    @Test
    void fixedRateComesFromThePropertyPlaceholder() {
        FixedRateTask t = tasks().stream().filter(FixedRateTask.class::isInstance).map(FixedRateTask.class::cast).findFirst().orElseThrow();
        assertThat(t.getIntervalDuration()).isEqualTo(Duration.ofMillis(120000));
        assertThat(t.toString()).contains("refresh");
    }

    @Test
    void jobBodiesDoRealWork() {
        int b = jobs.beats();
        int c = jobs.cleanups();
        int r = jobs.refreshes();
        jobs.heartbeat();
        jobs.nightlyCleanup();
        jobs.refresh();
        jobs.refresh();
        assertThat(jobs.beats()).isEqualTo(b + 1);
        assertThat(jobs.cleanups()).isEqualTo(c + 1);
        assertThat(jobs.refreshes()).isEqualTo(r + 2);
    }

    @Test
    void methodsCarryScheduledAnnotations() throws Exception {
        Method m = Jobs.class.getMethod("nightlyCleanup");
        var s = m.getAnnotation(org.springframework.scheduling.annotation.Scheduled.class);
        assertThat(s).isNotNull();
        assertThat(s.zone()).isEqualTo("UTC");
    }
}
