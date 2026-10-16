package com.javaprep.day25.task01;

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

class SchemaConstraintsTest {

    private Connection c;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "Day25-task01");
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
    void tablesExist() throws Exception {
        DatabaseMetaData md = c.getMetaData();
        List<String> names = new ArrayList<>();
        try (ResultSet rs = md.getTables(null, null, "%", new String[] {"TABLE"})) {
            while (rs.next()) {
                names.add(rs.getString("TABLE_NAME").toLowerCase());
            }
        }
        assertThat(names).contains("customers", "products", "orders");
    }

    @Test
    void emailMustBeUnique() throws Exception {
        exec("insert into customers(email, full_name) values ('a@x.io', 'A')");
        assertThatThrownBy(() -> exec("insert into customers(email, full_name) values ('a@x.io', 'B')"))
                .isInstanceOf(SQLException.class);
    }

    @Test
    void fullNameIsRequired() {
        assertThatThrownBy(() -> exec("insert into customers(email, full_name) values ('n@x.io', null)"))
                .isInstanceOf(SQLException.class);
    }

    @Test
    void createdAtDefaultsToNow() throws Exception {
        exec("insert into customers(email, full_name) values ('d@x.io', 'D')");
        assertThat(SqlLab.scalar(c, "select count(*) from customers where created_at is not null")).isEqualTo(1);
    }

    @Test
    void priceCannotBeNegativeAndSkuIsUnique() throws Exception {
        assertThatThrownBy(() -> exec("insert into products(sku, name, price_cents) values ('S1', 'Bad', -1)"))
                .isInstanceOf(SQLException.class);
        exec("insert into products(sku, name, price_cents) values ('S1', 'Ok', 0)");
        assertThatThrownBy(() -> exec("insert into products(sku, name, price_cents) values ('S1', 'Dup', 5)"))
                .isInstanceOf(SQLException.class);
    }

    @Test
    void orderForeignKeyAndStatusRules() throws Exception {
        assertThatThrownBy(() -> exec("insert into orders(customer_id) values (999)")).isInstanceOf(SQLException.class);
        exec("insert into customers(email, full_name) values ('o@x.io', 'O')");
        exec("insert into orders(customer_id) values (1)");
        assertThat(SqlLab.query(c, "select status from orders").get(0).get(0)).isEqualTo("NEW");
        assertThatThrownBy(() -> exec("insert into orders(customer_id, status) values (1, 'BOGUS')"))
                .isInstanceOf(SQLException.class);
    }

    @Test
    void seedAndAnswersWork() throws Exception {
        SqlLab.runScript(c, "sql/seed.sql", "Day25-task01");
        Map<String, String> answers = SqlLab.namedBlocks("sql/answers.sql", "Day25-task01");
        assertThat(SqlLab.scalar(c, answers.get("q_customer_count"))).isEqualTo(3);
        assertThat(SqlLab.query(c, answers.get("q_cheapest_product")).get(0).get(0)).isEqualTo("Mouse");
    }
}
