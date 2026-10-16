package com.javaprep.day35.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.orm.ObjectOptimisticLockingFailureException;

@SpringBootTest
class VersionAndAuditingTest {

    @Autowired
    StockService service;

    @Test
    void newProductStartsAtVersionZeroWithAuditTimestamps() {
        Product p = service.create("Pen", 10);
        assertThat(p.getVersion()).isZero();
        assertThat(p.getCreatedAt()).isNotNull();
        assertThat(p.getUpdatedAt()).isNotNull();
    }

    @Test
    void everyUpdateBumpsVersionAndLastModified() throws Exception {
        Product p = service.create("Pen", 10);
        Thread.sleep(5);
        Product after = service.adjust(p.getId(), -3);
        assertThat(after.getStock()).isEqualTo(7);
        assertThat(after.getVersion()).isEqualTo(1);
        assertThat(after.getUpdatedAt()).isAfter(p.getUpdatedAt());
        assertThat(after.getCreatedAt()).isEqualTo(service.get(p.getId()).getCreatedAt());
    }

    @Test
    void staleDetachedCopyIsRejected() {
        Product stale = service.create("Pen", 10);
        service.adjust(stale.getId(), 5);                 // someone else updates: version 1
        stale.setName("Renamed");
        assertThatThrownBy(() -> service.saveDetached(stale)).isInstanceOf(ObjectOptimisticLockingFailureException.class);
        assertThat(service.get(stale.getId()).getName()).isEqualTo("Pen");
    }

    @Test
    void freshCopyCanBeSaved() {
        Product p = service.create("Pen", 10);
        Product fresh = service.get(p.getId());
        fresh.setName("Pencil");
        Product saved = service.saveDetached(fresh);
        assertThat(saved.getName()).isEqualTo("Pencil");
        assertThat(saved.getVersion()).isEqualTo(1);
    }

    @Test
    void businessRuleKeepsStockNonNegative() {
        Product p = service.create("Pen", 2);
        assertThatThrownBy(() -> service.adjust(p.getId(), -3)).isInstanceOf(IllegalStateException.class).hasMessage("Stock cannot be negative");
        assertThat(service.get(p.getId()).getStock()).isEqualTo(2);
    }
}
