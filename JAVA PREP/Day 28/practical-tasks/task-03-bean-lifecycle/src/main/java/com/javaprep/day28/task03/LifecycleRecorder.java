package com.javaprep.day28.task03;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.springframework.stereotype.Component;

/** PROVIDED: shared log of lifecycle events. */
@Component
public class LifecycleRecorder {
    private final List<String> events = Collections.synchronizedList(new ArrayList<>());

    public void record(String event) {
        events.add(event);
    }

    public List<String> events() {
        return List.copyOf(events);
    }
}
