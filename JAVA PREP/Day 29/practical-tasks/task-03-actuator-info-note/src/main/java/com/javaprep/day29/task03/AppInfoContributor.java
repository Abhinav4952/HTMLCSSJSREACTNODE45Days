package com.javaprep.day29.task03;

import java.util.Map;
import org.springframework.boot.actuate.info.Info;
import org.springframework.boot.actuate.info.InfoContributor;

/** Adds an "app" section (name + version) to the /actuator/info response. */
public class AppInfoContributor implements InfoContributor {

    private final String name;
    private final String version;

    public AppInfoContributor(String name, String version) {
        this.name = name;
        this.version = version;
    }

    @Override
    public void contribute(Info.Builder builder) {
        // TODO(Day29-task03): add a detail "app" whose value is a Map with keys "name" and "version"
        throw new UnsupportedOperationException("TODO(Day29-task03): implement contribute");
    }

    /** The URL path where the info endpoint is exposed by default. */
    public static String infoEndpointPath() {
        // TODO(Day29-task03): return "/actuator/info"
        throw new UnsupportedOperationException("TODO(Day29-task03): implement infoEndpointPath");
    }

    /** The property line that exposes health and info over HTTP, exactly: management.endpoints.web.exposure.include=health,info */
    public static String exposureProperty() {
        // TODO(Day29-task03): return the property line
        throw new UnsupportedOperationException("TODO(Day29-task03): implement exposureProperty");
    }
}
