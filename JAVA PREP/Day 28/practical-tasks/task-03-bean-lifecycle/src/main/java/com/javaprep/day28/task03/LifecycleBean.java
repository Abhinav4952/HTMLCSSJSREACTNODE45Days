package com.javaprep.day28.task03;

import org.springframework.stereotype.Component;

@Component
public class LifecycleBean {

    private final LifecycleRecorder recorder;

    public LifecycleBean(LifecycleRecorder recorder) {
        this.recorder = recorder;
        recorder.record("ctor");
    }

    // TODO(Day28-task03): run this after dependency injection (@PostConstruct) and record "init"
    public void init() {
        throw new UnsupportedOperationException("TODO(Day28-task03): implement init");
    }

    // TODO(Day28-task03): run this on context shutdown (@PreDestroy) and record "destroy"
    public void close() {
        throw new UnsupportedOperationException("TODO(Day28-task03): implement close");
    }
}
