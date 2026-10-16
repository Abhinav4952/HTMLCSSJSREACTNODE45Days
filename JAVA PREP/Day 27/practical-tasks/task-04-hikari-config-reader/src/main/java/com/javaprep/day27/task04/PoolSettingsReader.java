package com.javaprep.day27.task04;

import com.zaxxer.hikari.HikariConfig;
import java.util.Properties;

/** Reads datasource settings the way Spring Boot/Hikari expect them. */
public final class PoolSettingsReader {

    private PoolSettingsReader() {
    }

    /** PROVIDED value object. */
    public record PoolSettings(String jdbcUrl, String username, String password, int maximumPoolSize,
                               int minimumIdle, long connectionTimeoutMs) {
    }

    /**
     * Keys: jdbcUrl (required, non-blank), username, password (default ""), maximumPoolSize (default 10, must be &gt;= 1),
     * minimumIdle (default = maximumPoolSize, must be 0..maximumPoolSize), connectionTimeoutMs (default 30000, must be &gt;= 250).
     * Any violation (including non-numeric numbers) -> IllegalArgumentException whose message names the key.
     */
    public static PoolSettings read(Properties props) {
        // TODO(Day27-task04): parse + validate as documented
        throw new UnsupportedOperationException("TODO(Day27-task04): implement read");
    }

    /** Copies the settings into a HikariConfig (jdbcUrl, username, password, maximumPoolSize, minimumIdle, connectionTimeout). */
    public static HikariConfig toHikariConfig(PoolSettings s) {
        // TODO(Day27-task04): populate and return a HikariConfig
        throw new UnsupportedOperationException("TODO(Day27-task04): implement toHikariConfig");
    }

    /**
     * Log-safe one-liner, exactly: {@code jdbcUrl=<url>; user=<user>; password=****; max=<n>; minIdle=<n>; timeoutMs=<n>}.
     * The real password must never appear.
     */
    public static String maskedSummary(PoolSettings s) {
        // TODO(Day27-task04): build the masked summary string
        throw new UnsupportedOperationException("TODO(Day27-task04): implement maskedSummary");
    }
}
