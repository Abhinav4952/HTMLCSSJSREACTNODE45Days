package com.javaprep.day40.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class AdviceTypesTest {

    AnnotationConfigApplicationContext ctx;
    OrderService service;
    CallRecorder recorder;

    @BeforeEach
    void start() {
        ctx = new AnnotationConfigApplicationContext(AopConfig.class);
        service = ctx.getBean(OrderService.class);
        recorder = ctx.getBean(CallRecorder.class);
        recorder.clear();
    }

    @AfterEach
    void stop() {
        ctx.close();
    }

    @Test
    void serviceIsProxied() {
        assertThat(AopUtils.isAopProxy(service)).isTrue();
    }

    @Test
    void normalCallRunsBeforeReturnedAndFinally() {
        assertThat(service.place("pen")).isEqualTo("order:pen");
        assertThat(recorder.events()).containsExactly("before:place", "returned:place=order:pen", "finally:place");
    }

    @Test
    void failingCallRunsBeforeThrewAndFinally() {
        assertThatThrownBy(() -> service.fail()).isInstanceOf(IllegalStateException.class).hasMessage("boom");
        assertThat(recorder.events()).containsExactly("before:fail", "threw:fail:IllegalStateException", "finally:fail");
    }

    @Test
    void adviceDoesNotRunForOtherBeans() {
        recorder.add("manual");
        assertThat(recorder.events()).containsExactly("manual");
    }
}
