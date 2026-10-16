package com.javaprep.day25.task03;

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

class NormalizationTest {

    private Connection c;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/raw.sql", "Day25-task03");
        SqlLab.runScript(c, "sql/schema.sql", "Day25-task03");
        SqlLab.runScript(c, "sql/seed.sql", "Day25-task03");
    }

    @AfterEach
    void tearDown() throws Exception {
        c.close();
    }

    private void exec(String sql) throws SQLException {
        try (Statement st = c.createStatement()) {
            st.execute(sql);
        }
    }

    @Test
    void dataWasSplitWithoutDuplicates() throws Exception {
        assertThat(SqlLab.scalar(c, "select count(*) from customers")).isEqualTo(2);
        assertThat(SqlLab.scalar(c, "select count(*) from products")).isEqualTo(3);
        assertThat(SqlLab.scalar(c, "select count(*) from orders")).isEqualTo(3);
        assertThat(SqlLab.scalar(c, "select count(*) from order_lines")).isEqualTo(5);
    }

    @Test
    void ordersKeepOriginalIdsAndLinkToCustomers() throws Exception {
        assertThat(SqlLab.scalar(c, "select count(*) from orders o join customers c on c.id = o.customer_id "
                + "where o.id = 3 and c.email = 'ana@x.io'")).isEqualTo(1);
    }

    @Test
    void compositeKeyPreventsDuplicateLines() throws Exception {
        long skuA = SqlLab.scalar(c, "select id from products where sku = 'SKU-A'");
        assertThatThrownBy(() -> exec("insert into order_lines(order_id, product_id, qty) values (1, " + skuA + ", 1)"))
                .isInstanceOf(SQLException.class);
    }

    @Test
    void quantityMustBePositiveAndKeysEnforced() throws Exception {
        long skuA = SqlLab.scalar(c, "select id from products where sku = 'SKU-A'");
        assertThatThrownBy(() -> exec("insert into order_lines(order_id, product_id, qty) values (3, " + skuA + ", 0)"))
                .isInstanceOf(SQLException.class);
        assertThatThrownBy(() -> exec("insert into order_lines(order_id, product_id, qty) values (99, " + skuA + ", 1)"))
                .isInstanceOf(SQLException.class);
        assertThatThrownBy(() -> exec("insert into customers(email, name) values ('ana@x.io', 'Dup')"))
                .isInstanceOf(SQLException.class);
    }

    @Test
    void totalsPerCustomer() throws Exception {
        String sql = SqlLab.namedBlocks("sql/answers.sql", "Day25-task03").get("q_total_by_customer");
        List<List<Object>> rows = SqlLab.query(c, sql);
        assertThat(rows).hasSize(2);
        assertThat(rows.get(0).get(0)).isEqualTo("ana@x.io");
        assertThat(((Number) rows.get(0).get(1)).longValue()).isEqualTo(49000);
        assertThat(rows.get(1).get(0)).isEqualTo("bob@x.io");
        assertThat(((Number) rows.get(1).get(1)).longValue()).isEqualTo(25000);
    }
}
