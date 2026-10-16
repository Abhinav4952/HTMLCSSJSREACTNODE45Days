package com.javaprep.day40.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class AspectOrderingTest {

    AnnotationConfigApplicationContext ctx;
    PaymentService service;
    CallRecorder recorder;

    @BeforeEach
    void start() {
        ctx = new AnnotationConfigApplicationContext(AopConfig.class);
        service = ctx.getBean(PaymentService.class);
        recorder = ctx.getBean(CallRecorder.class);
        recorder.clear();
    }

    @AfterEach
    void stop() {
        ctx.close();
    }

    @Test
    void classBasedProxyBecausePaymentServiceHasNoInterface() {
        assertThat(AopUtils.isCglibProxy(service)).isTrue();
    }

    @Test
    void successOrderIsOnionShaped() {
        assertThat(service.pay("alice")).isEqualTo("paid:alice");
        assertThat(recorder.events()).containsExactly("security:in", "tx:begin", "pay:alice", "tx:commit", "security:out");
    }

    @Test
    void failureRollsBackInsideSecurity() {
        assertThatThrownBy(() -> service.pay("bad")).isInstanceOf(IllegalStateException.class).hasMessage("declined");
        assertThat(recorder.events()).containsExactly("security:in", "tx:begin", "pay:bad", "tx:rollback", "security:out");
    }
}
