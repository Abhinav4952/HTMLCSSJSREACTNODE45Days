package com.javaprep.day26.task02;

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

class GroupByTest {

    private Connection c;
    private Map<String, String> q;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "Day26-task02");
        SqlLab.runScript(c, "sql/seed.sql", "Day26-task02");
        q = SqlLab.namedBlocks("sql/answers.sql", "Day26-task02");
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
    void totalsByRegion() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("total_by_region")))).containsExactly("APAC:12000", "EU:13000", "US:5500");
    }

    @Test
    void saleCountByRegion() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("count_by_region")))).containsExactly("APAC:1", "EU:3", "US:2");
    }

    @Test
    void havingFiltersGroups() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("regions_over_10000")))).containsExactly("APAC", "EU");
    }

    @Test
    void topRep() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("top_rep")))).containsExactly("di:12000");
    }

    @Test
    void averageIsRoundedDown() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("avg_sale_eu")))).containsExactly("4333");
    }
}
