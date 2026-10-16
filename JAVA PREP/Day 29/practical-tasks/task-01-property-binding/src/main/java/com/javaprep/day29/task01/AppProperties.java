package com.javaprep.day29.task01;

import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.context.properties.ConfigurationProperties;

/** Binds {@code app.*} properties (relaxed binding: app.max-users, app.maxUsers, APP_MAXUSERS all map to maxUsers). */
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    private String name;
    private int maxUsers;
    private List<String> features = new ArrayList<>();
    private final Security security = new Security();

    // TODO(Day29-task01): add getters and setters for name, maxUsers and features (JavaBean binding needs setters),
    //              and a getter for the nested security object

    public static class Security {
        private boolean enabled;
        private String token;

        // TODO(Day29-task01): add getters and setters for enabled and token
    }

    /** "<name> (<maxUsers> users, <features.size()> features)" e.g. "demo (5 users, 2 features)". */
    public String summary() {
        // TODO(Day29-task01): build the summary from the bound values
        throw new UnsupportedOperationException("TODO(Day29-task01): implement summary");
    }
}
