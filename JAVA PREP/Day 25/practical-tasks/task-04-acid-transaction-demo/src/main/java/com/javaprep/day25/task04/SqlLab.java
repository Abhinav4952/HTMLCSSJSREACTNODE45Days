package com.javaprep.day25.task04;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

/**
 * PROVIDED helper (do not edit). Runs the learner's SQL files against an in-memory H2 database in
 * PostgreSQL mode.
 *
 * <ul>
 *   <li>{@code -- ...} lines are comments (including TODO markers).</li>
 *   <li>Statements are split on {@code ;} (do not put semicolons inside string literals).</li>
 *   <li>If a script contains no statements yet, an UnsupportedOperationException with the TODO tag is thrown.</li>
 *   <li>{@code answers.sql} is split into named blocks using marker lines like {@code -- @name}.</li>
 * </ul>
 */
public final class SqlLab {

    /** Base URL from the course spec; {@link #open()} appends a unique database name per test. */
    public static final String BASE_URL =
            "jdbc:h2:mem:day25;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DEFAULT_NULL_ORDERING=HIGH";

    private SqlLab() {
    }

    public static Connection open() throws SQLException {
        String url = BASE_URL.replace("mem:day25", "mem:day25_" + UUID.randomUUID().toString().replace("-", ""))
                + ";DB_CLOSE_DELAY=-1";
        return DriverManager.getConnection(url, "sa", "");
    }

    public static void runScript(Connection c, String path, String tag) throws SQLException, IOException {
        List<String> statements = statements(Files.readString(Path.of(path)));
        if (statements.isEmpty()) {
            throw new UnsupportedOperationException("TODO(" + tag + "): " + path + " has no SQL statements yet");
        }
        try (Statement st = c.createStatement()) {
            for (String s : statements) {
                st.execute(s);
            }
        }
    }

    /** Parses {@code -- @name} blocks; every block must contain one statement. */
    public static Map<String, String> namedBlocks(String path, String tag) throws IOException {
        Map<String, String> out = new LinkedHashMap<>();
        String current = null;
        StringBuilder body = new StringBuilder();
        for (String line : Files.readAllLines(Path.of(path))) {
            String t = line.trim();
            if (t.startsWith("-- @")) {
                if (current != null) {
                    out.put(current, body.toString().trim());
                }
                current = t.substring(4).trim();
                body.setLength(0);
            } else if (!t.startsWith("--") && current != null) {
                body.append(line).append('\n');
            }
        }
        if (current != null) {
            out.put(current, body.toString().trim());
        }
        for (Map.Entry<String, String> e : out.entrySet()) {
            if (e.getValue().isBlank()) {
                throw new UnsupportedOperationException("TODO(" + tag + "): block '" + e.getKey() + "' in " + path + " is empty");
            }
        }
        return out;
    }

    /** Executes a named block and returns rows (SELECT) as lists of values. */
    public static List<List<Object>> query(Connection c, String sql) throws SQLException {
        List<List<Object>> rows = new ArrayList<>();
        try (Statement st = c.createStatement(); ResultSet rs = st.executeQuery(stripSemicolon(sql))) {
            ResultSetMetaData md = rs.getMetaData();
            while (rs.next()) {
                List<Object> row = new ArrayList<>();
                for (int i = 1; i <= md.getColumnCount(); i++) {
                    row.add(rs.getObject(i));
                }
                rows.add(row);
            }
        }
        return rows;
    }

    public static int update(Connection c, String sql) throws SQLException {
        try (Statement st = c.createStatement()) {
            return st.executeUpdate(stripSemicolon(sql));
        }
    }

    public static long scalar(Connection c, String sql) throws SQLException {
        return ((Number) query(c, sql).get(0).get(0)).longValue();
    }

    private static String stripSemicolon(String sql) {
        String s = sql.trim();
        return s.endsWith(";") ? s.substring(0, s.length() - 1) : s;
    }

    static List<String> statements(String script) {
        StringBuilder cleaned = new StringBuilder();
        for (String line : script.split("\\R")) {
            if (!line.trim().startsWith("--")) {
                cleaned.append(line).append('\n');
            }
        }
        List<String> out = new ArrayList<>();
        for (String part : cleaned.toString().split(";")) {
            if (!part.isBlank()) {
                out.add(part.trim());
            }
        }
        return out;
    }
}
