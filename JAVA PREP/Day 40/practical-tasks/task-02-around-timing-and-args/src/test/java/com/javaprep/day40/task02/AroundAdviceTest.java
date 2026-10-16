package com.javaprep.day40.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class AroundAdviceTest {

    AnnotationConfigApplicationContext ctx;
    ReportService reports;
    TextService text;
    MetricsRegistry metrics;

    @BeforeEach
    void start() {
        ctx = new AnnotationConfigApplicationContext(AopConfig.class);
        reports = ctx.getBean(ReportService.class);
        text = ctx.getBean(TextService.class);
        metrics = ctx.getBean(MetricsRegistry.class);
    }

    @AfterEach
    void stop() {
        ctx.close();
    }

    @Test
    void timedMethodIsMeasuredAndResultPassesThrough() throws Exception {
        assertThat(reports.build()).isEqualTo("report");
        assertThat(metrics.count("build")).isEqualTo(1);
        assertThat(metrics.totalNanos("build")).isGreaterThanOrEqualTo(4_000_000L);
    }

    @Test
    void exceptionsAreRecordedAndRethrownUnchanged() {
        assertThatThrownBy(() -> reports.explode()).isInstanceOf(IllegalArgumentException.class).hasMessage("bad report");
        assertThat(metrics.count("explode")).isEqualTo(1);
    }

    @Test
    void untimedMethodsAreNotRecorded() {
        reports.untimed();
        assertThat(metrics.count("untimed")).isZero();
    }

    @Test
    void stringArgumentsAreTrimmedByAroundAdvice() {
        assertThat(text.shout("  hi  ")).isEqualTo("HI!");
        assertThat(text.echo("\t x \n")).isEqualTo("x");
    }

    @Test
    void otherSignaturesAreUntouched() {
        assertThat(text.twice(21)).isEqualTo(42);
    }
}
