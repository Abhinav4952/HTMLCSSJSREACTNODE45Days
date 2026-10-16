package com.javaprep.day28.task03;

import org.springframework.stereotype.Component;

// TODO(Day28-task03): every injection/lookup must get a NEW instance (prototype scope)
@Component
public class ReportBuilder {
    private final StringBuilder content = new StringBuilder();

    public ReportBuilder append(String line) {
        content.append(line).append('\n');
        return this;
    }

    public String build() {
        return content.toString();
    }
}
