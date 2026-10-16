package com.javaprep.day28.task03;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class LifecycleTest {

    @Test
    void initAndDestroyRecordEvents() {
        LifecycleRecorder rec = new LifecycleRecorder();
        LifecycleBean bean = new LifecycleBean(rec);
        bean.init();
        bean.close();
        assertThat(rec.events()).containsExactly("ctor", "init", "destroy");
    }

    @Test
    void containerCallsCallbacksInOrder() {
        AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(LifecycleConfig.class);
        LifecycleRecorder rec = ctx.getBean(LifecycleRecorder.class);
        assertThat(rec.events()).containsExactly("ctor", "init");
        ctx.close();
        assertThat(rec.events()).containsExactly("ctor", "init", "destroy");
    }

    @Test
    void singletonIsSharedPrototypeIsNot() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(LifecycleConfig.class)) {
            assertThat(ctx.getBean(LifecycleRecorder.class)).isSameAs(ctx.getBean(LifecycleRecorder.class));
            ReportBuilder a = ctx.getBean(ReportBuilder.class);
            ReportBuilder b = ctx.getBean(ReportBuilder.class);
            assertThat(a).isNotSameAs(b);
            assertThat(a.append("x").build()).isEqualTo("x\n");
            assertThat(b.build()).isEmpty();
        }
    }
}
