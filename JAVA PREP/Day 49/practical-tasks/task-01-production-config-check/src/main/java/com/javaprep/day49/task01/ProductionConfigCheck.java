package com.javaprep.day49.task01;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Fail-fast validation of the environment a production deployment starts with. */
public class ProductionConfigCheck {

    /**
     * Returns problems in THIS order (empty list = OK):
     * <ol>
     *   <li>for each of DB_URL, DB_USERNAME, DB_PASSWORD, JWT_SECRET (in that order) missing or blank: "MISSING:KEY"</li>
     *   <li>DB_URL present but not starting with "jdbc:postgresql://": "BAD_DB_URL"</li>
     *   <li>DB_PASSWORD present and (case-insensitively) one of password, postgres, changeme, admin: "WEAK:DB_PASSWORD"</li>
     *   <li>JWT_SECRET present but shorter than 32 characters: "WEAK:JWT_SECRET"</li>
     *   <li>SPRING_PROFILES_ACTIVE not exactly "prod" (missing counts): "PROFILE_NOT_PROD"</li>
     * </ol>
     */
    public List<String> problems(Map<String, String> env) {
        // TODO(Day49-task01): apply the rules in the stated order
        throw new UnsupportedOperationException("TODO(Day49-task01): implement problems");
    }
}
