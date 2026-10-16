package com.javaprep.day46.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

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

class OutboxTest {

    private Connection conn;
    private OrderService orders;
    private OutboxPoller poller;

    @BeforeEach
    void setUp() throws Exception {
        conn = DriverManager.getConnection("jdbc:h2:mem:day46t4_" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1", "sa", "");
        try (Statement st = conn.createStatement()) {
            for (String ddl : OutboxSchema.DDL) {
                st.execute(ddl);
            }
        }
        orders = new OrderService(conn);
        poller = new OutboxPoller(conn);
    }

    @AfterEach
    void tearDown() throws Exception {
        conn.close();
    }

    private int count(String table) throws Exception {
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery("select count(*) from " + table)) {
            rs.next();
            return rs.getInt(1);
        }
    }

    @Test
    void placeOrderWritesOrderAndOutboxRow() throws Exception {
        orders.placeOrder("o-1", "{\"id\":\"o-1\"}");
        assertThat(count("orders")).isEqualTo(1);
        assertThat(count("outbox")).isEqualTo(1);
        assertThat(conn.getAutoCommit()).isTrue();
    }

    @Test
    void failureRollsBackTheOrderToo() throws Exception {
        // outbox.payload is NOT NULL: the outbox insert fails after the order insert succeeded
        assertThatThrownBy(() -> orders.placeOrder("o-2", null)).isInstanceOf(IllegalStateException.class);
        assertThat(count("orders")).isZero();
        assertThat(count("outbox")).isZero();
        assertThat(conn.getAutoCommit()).isTrue();
    }

    @Test
    void pollerPublishesInOrderAndMarksRows() throws Exception {
        orders.placeOrder("o-1", "p1");
        orders.placeOrder("o-2", "p2");
        List<String> sent = new ArrayList<>();
        assertThat(poller.pollOnce((type, payload) -> sent.add(type + ":" + payload))).isEqualTo(2);
        assertThat(sent).containsExactly("OrderPlaced:p1", "OrderPlaced:p2");
        assertThat(poller.pollOnce((type, payload) -> sent.add("again"))).isZero();
    }

    @Test
    void failedPublishStopsAndRetriesLater() throws Exception {
        orders.placeOrder("o-1", "p1");
        orders.placeOrder("o-2", "p2");
        orders.placeOrder("o-3", "p3");
        List<String> sent = new ArrayList<>();
        int first = poller.pollOnce((type, payload) -> {
            if (payload.equals("p2")) {
                throw new IllegalStateException("broker down");
            }
            sent.add(payload);
        });
        assertThat(first).isEqualTo(1);
        assertThat(sent).containsExactly("p1");

        int second = poller.pollOnce((type, payload) -> sent.add(payload));
        assertThat(second).isEqualTo(2);
        assertThat(sent).containsExactly("p1", "p2", "p3");
    }
}
