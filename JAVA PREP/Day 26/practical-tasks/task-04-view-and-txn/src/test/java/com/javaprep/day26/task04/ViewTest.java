package com.javaprep.day26.task04;

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

class ViewTest {

    private Connection c;
    private Map<String, String> q;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "Day26-task04");
        SqlLab.runScript(c, "sql/seed.sql", "Day26-task04");
        q = SqlLab.namedBlocks("sql/answers.sql", "Day26-task04");
        c.setAutoCommit(false);
        SqlLab.update(c, q.get("create_view_order_totals"));
        c.commit();
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
    void viewExposesOneRowPerOrder() throws Exception {
        assertThat(SqlLab.scalar(c, "select count(*) from order_totals")).isEqualTo(3);
        assertThat(flat(SqlLab.query(c, "select order_id, total_cents from order_totals order by order_id")))
                .containsExactly("1:11000", "2:3000", "3:14000");
    }

    @Test
    void bigOrdersQueryUsesTheView() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("q_big_orders")))).containsExactly("1:11000", "3:14000");
    }

    @Test
    void domainCountsUseStringFunctions() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("q_domain_counts")))).containsExactly("x.io:2", "y.io:1");
    }

    @Test
    void viewReflectsNewDataAndRollbackWorks() throws Exception {
        SqlLab.update(c, "insert into orders values (4, 2)");
        SqlLab.update(c, "insert into order_items values (4, 'Z', 1, 20000)");
        assertThat(SqlLab.scalar(c, "select count(*) from order_totals")).isEqualTo(4);
        c.rollback();
        assertThat(SqlLab.scalar(c, "select count(*) from order_totals")).isEqualTo(3);
    }
}
