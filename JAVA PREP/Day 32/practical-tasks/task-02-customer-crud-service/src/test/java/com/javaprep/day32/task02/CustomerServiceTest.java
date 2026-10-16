package com.javaprep.day32.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.NoSuchElementException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(CustomerService.class)
class CustomerServiceTest {

    @Autowired
    CustomerService service;
    @Autowired
    CustomerRepository repository;
    @Autowired
    TestEntityManager em;

    @Test
    void createAssignsId() {
        Customer c = service.create("Ann", "ann@x.io");
        assertThat(c.getId()).isNotNull();
        assertThat(repository.findById(c.getId())).isPresent();
    }

    @Test
    void getUnknownThrows() {
        assertThatThrownBy(() -> service.get(404L)).isInstanceOf(NoSuchElementException.class).hasMessage("Customer 404 not found");
    }

    @Test
    void renameUsesDirtyChecking() {
        Customer c = service.create("Ann", "ann@x.io");
        service.rename(c.getId(), "Anna");
        em.flush();
        em.clear();
        assertThat(repository.findById(c.getId()).orElseThrow().getName()).isEqualTo("Anna");
    }

    @Test
    void renameUnknownThrows() {
        assertThatThrownBy(() -> service.rename(1000L, "x")).isInstanceOf(NoSuchElementException.class);
    }

    @Test
    void deleteRemovesRow() {
        Customer c = service.create("Ann", "ann@x.io");
        service.delete(c.getId());
        assertThat(service.count()).isZero();
        assertThatThrownBy(() -> service.delete(c.getId())).isInstanceOf(NoSuchElementException.class);
    }

    @Test
    void allAndCount() {
        service.create("A", "a@x");
        service.create("B", "b@x");
        assertThat(service.all()).extracting(Customer::getName).containsExactlyInAnyOrder("A", "B");
        assertThat(service.count()).isEqualTo(2);
    }
}
