package com.javaprep.day26.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;

class IndexAdvisorTest {

    @Test
    void compositeIndexPutsEqualityBeforeRange() {
        assertThat(IndexAdvisor.recommendIndex("orders", List.of("customer_id", "status"), "created_at"))
                .isEqualTo("CREATE INDEX idx_orders_customer_id_status_created_at ON orders (customer_id, status, created_at)");
    }

    @Test
    void rangeColumnIsOptional() {
        assertThat(IndexAdvisor.recommendIndex("users", List.of("email"), null))
                .isEqualTo("CREATE INDEX idx_users_email ON users (email)");
    }

    @Test
    void onlyRangeColumn() {
        assertThat(IndexAdvisor.recommendIndex("logs", List.of(), "created_at"))
                .isEqualTo("CREATE INDEX idx_logs_created_at ON logs (created_at)");
    }

    @Test
    void nothingToIndexIsRejected() {
        assertThatThrownBy(() -> IndexAdvisor.recommendIndex("t", List.of(), null))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void uniqueIndex() {
        assertThat(IndexAdvisor.recommendUniqueIndex("users", "email"))
                .isEqualTo("CREATE UNIQUE INDEX uq_users_email ON users (email)");
    }

    @Test
    void sargability() {
        assertThat(IndexAdvisor.isIndexUsable("status = 'NEW'")).isTrue();
        assertThat(IndexAdvisor.isIndexUsable("email LIKE 'ana%'")).isTrue();
        assertThat(IndexAdvisor.isIndexUsable("created_at > '2024-01-01'")).isTrue();
        assertThat(IndexAdvisor.isIndexUsable("email LIKE '%gmail.com'")).isFalse();
        assertThat(IndexAdvisor.isIndexUsable("  LOWER(email) = 'a@x.io'")).isFalse();
    }

    @Test
    void planClassification() {
        assertThat(IndexAdvisor.classifyPlan("SELECT * FROM PUBLIC.ORDERS /* PUBLIC.ORDERS.tableScan */"))
                .isEqualTo("FULL_SCAN");
        assertThat(IndexAdvisor.classifyPlan("SELECT * FROM PUBLIC.ORDERS /* PUBLIC.IDX_ORDERS_STATUS: STATUS = 'NEW' */"))
                .isEqualTo("INDEX_SCAN");
        assertThat(IndexAdvisor.classifyPlan("something else")).isEqualTo("UNKNOWN");
    }
}
