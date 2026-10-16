package com.javaprep.day26.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class JoinsTest {

    private Connection c;
    private Map<String, String> q;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "Day26-task01");
        SqlLab.runScript(c, "sql/seed.sql", "Day26-task01");
        q = SqlLab.namedBlocks("sql/answers.sql", "Day26-task01");
    }

    @AfterEach
    void tearDown() throws Exception {
        c.close();
    }

    private static List<String> flat(List<List<Object>> rows) {
        List<String> out = new ArrayList<>();
        for (List<Object> r : rows) {
            List<String> cols = new ArrayList<>();
            for (Object o : r) {
                cols.add(String.valueOf(o instanceof Number n && !(o instanceof Double) ? n.longValue() : o));
            }
            out.add(String.join(":", cols));
        }
        return out;
    }

    @Test
    void innerJoinOnlyMatchedPairs() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("inner_join")))).containsExactly("Ana:Eng", "Bo:Eng", "Cy:Sales");
    }

    @Test
    void leftJoinFindsEmployeesWithoutDepartment() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("left_unassigned")))).containsExactly("Di");
    }

    @Test
    void departmentsWithoutEmployees() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("dept_without_employees")))).containsExactly("Legal");
    }

    @Test
    void selfJoinManagers() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("self_join_manager")))).containsExactly("Bo:Ana", "Cy:Ana", "Di:Ana");
    }

    @Test
    void fullOuterRowCount() throws Exception {
        assertThat(SqlLab.scalar(c, q.get("full_outer_row_count"))).isEqualTo(5);
    }
}
