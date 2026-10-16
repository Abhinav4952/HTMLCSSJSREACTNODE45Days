package com.javaprep.day27.task02;

import java.util.List;
import javax.sql.DataSource;

/** Table: users(id BIGINT AUTO_INCREMENT PK, name VARCHAR(50), email VARCHAR(100)). */
public class SafeSearchDao {

    private final DataSource dataSource;

    public SafeSearchDao(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    /** PROVIDED — shows the VULNERABLE pattern. Never execute this string. */
    public static String buildUnsafeSql(String name) {
        return "SELECT id, name, email FROM users WHERE name = '" + name + "'";
    }

    /** Exact name match using a PreparedStatement parameter; ordered by id. */
    public List<User> findByName(String name) {
        // TODO(Day27-task02): prepared statement with a ? placeholder (no string concatenation)
        throw new UnsupportedOperationException("TODO(Day27-task02): implement findByName");
    }

    /**
     * Names starting with the prefix, ordered by name. The prefix is LITERAL text: '%' and '_' in the prefix must be
     * escaped (use LIKE ? ESCAPE '\\' and escape \\, % and _ with a backslash).
     */
    public List<User> findByNamePrefix(String prefix) {
        // TODO(Day27-task02): LIKE ? ESCAPE with an escaped prefix + "%"
        throw new UnsupportedOperationException("TODO(Day27-task02): implement findByNamePrefix");
    }

    /** Inserts a user and returns the generated id (Statement.RETURN_GENERATED_KEYS). */
    public long insertUser(String name, String email) {
        // TODO(Day27-task02): insert with a prepared statement and read the generated key
        throw new UnsupportedOperationException("TODO(Day27-task02): implement insertUser");
    }
}
