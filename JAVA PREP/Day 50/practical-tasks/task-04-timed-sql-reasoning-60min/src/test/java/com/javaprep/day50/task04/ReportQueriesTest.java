package com.javaprep.day50.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ReportQueriesTest {

    private Connection conn;

    @BeforeEach
    void setUp() throws Exception {
        conn = DriverManager.getConnection("jdbc:h2:mem:day50t4_" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1", "sa", "");
        try (Statement st = conn.createStatement()) {
            st.execute("create table customers (id int primary key, name varchar(50) not null)");
            st.execute("create table orders (id int primary key, customer_id int not null, total_cents bigint not null, status varchar(10) not null)");
            st.execute("insert into customers values (1,'Alice'),(2,'Bob'),(3,'Cara'),(4,'Dan'),(5,'Eve')");
            st.execute("insert into orders values (1,1,1000,'PAID'),(2,1,2500,'PAID'),(3,2,500,'PAID'),(4,2,9000,'CANCELLED'),"
                    + "(5,3,1200,'PAID'),(6,5,700,'CANCELLED'),(7,5,300,'NEW')");
        }
    }

    @AfterEach
    void tearDown() throws Exception {
        conn.close();
    }

    @Test
    void topCustomersByPaidTotal() throws Exception {
        List<String> rows = new ArrayList<>();
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery(ReportQueries.topCustomersSql())) {
            while (rs.next()) {
                rows.add(rs.getString(1) + "=" + rs.getLong(2));
            }
        }
        assertThat(rows).containsExactly("Alice=3500", "Cara=1200");
    }

    @Test
    void customersWithoutPaidOrders() throws Exception {
        List<String> names = new ArrayList<>();
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery(ReportQueries.customersWithoutPaidOrdersSql())) {
            while (rs.next()) {
                names.add(rs.getString(1));
            }
        }
        assertThat(names).containsExactly("Dan", "Eve");
    }

    @Test
    void antiJoinUsesNotExists() {
        assertThat(ReportQueries.customersWithoutPaidOrdersSql().toLowerCase()).contains("not exists").doesNotContain("not in");
    }

    @Test
    void supportingIndexIsCreatedWithTheExpectedName() throws Exception {
        try (Statement st = conn.createStatement()) {
            st.execute(ReportQueries.supportingIndexDdl());
        }
        boolean found = false;
        try (ResultSet rs = conn.getMetaData().getIndexInfo(null, null, "ORDERS", false, false)) {
            while (rs.next()) {
                String name = rs.getString("INDEX_NAME");
                if (name != null && name.equalsIgnoreCase("idx_orders_customer_status")) {
                    found = true;
                }
            }
        }
        assertThat(found).isTrue();
    }
}
