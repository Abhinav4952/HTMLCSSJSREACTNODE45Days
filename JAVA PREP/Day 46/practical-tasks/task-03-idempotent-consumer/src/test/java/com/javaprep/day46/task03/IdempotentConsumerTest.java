package com.javaprep.day46.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class IdempotentConsumerTest {

    private Connection conn;
    private IdempotentConsumer consumer;
    private final AtomicInteger effects = new AtomicInteger();

    @BeforeEach
    void setUp() throws Exception {
        conn = DriverManager.getConnection("jdbc:h2:mem:day46t3_" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1", "sa", "");
        try (Statement st = conn.createStatement()) {
            st.execute(Schema.PROCESSED_EVENTS);
        }
        consumer = new IdempotentConsumer(conn);
    }

    @AfterEach
    void tearDown() throws Exception {
        conn.close();
    }

    private int storedEvents() throws Exception {
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery("select count(*) from processed_events")) {
            rs.next();
            return rs.getInt(1);
        }
    }

    @Test
    void firstDeliveryRunsTheSideEffect() throws Exception {
        assertThat(consumer.processOnce("e-1", effects::incrementAndGet)).isTrue();
        assertThat(effects.get()).isEqualTo(1);
        assertThat(storedEvents()).isEqualTo(1);
    }

    @Test
    void duplicateDeliveryIsSkipped() {
        consumer.processOnce("e-1", effects::incrementAndGet);
        assertThat(consumer.processOnce("e-1", effects::incrementAndGet)).isFalse();
        assertThat(effects.get()).isEqualTo(1);
    }

    @Test
    void differentEventsAreBothProcessed() {
        consumer.processOnce("e-1", effects::incrementAndGet);
        consumer.processOnce("e-2", effects::incrementAndGet);
        assertThat(effects.get()).isEqualTo(2);
    }

    @Test
    void failedSideEffectRollsBackSoRetryWorks() throws Exception {
        assertThatThrownBy(() -> consumer.processOnce("e-1", () -> {
            throw new IllegalStateException("boom");
        })).isInstanceOf(IllegalStateException.class).hasMessage("boom");
        assertThat(storedEvents()).isZero();
        assertThat(consumer.processOnce("e-1", effects::incrementAndGet)).isTrue();
        assertThat(effects.get()).isEqualTo(1);
    }

    @Test
    void autoCommitIsRestored() throws Exception {
        consumer.processOnce("e-1", effects::incrementAndGet);
        assertThat(conn.getAutoCommit()).isTrue();
        consumer.processOnce("e-1", effects::incrementAndGet);
        assertThat(conn.getAutoCommit()).isTrue();
    }
}
