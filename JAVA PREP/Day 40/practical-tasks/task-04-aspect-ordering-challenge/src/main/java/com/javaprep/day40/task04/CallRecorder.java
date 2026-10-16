package com.javaprep.day40.task04;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.springframework.stereotype.Component;

/** PROVIDED: collects events so tests can observe advice execution order. */
@Component
public class CallRecorder {
    private final List<String> events = Collections.synchronizedList(new ArrayList<>());

    public void add(String event) {
        events.add(event);
    }

    public List<String> events() {
        return List.copyOf(events);
    }

    public void clear() {
        events.clear();
    }
}
