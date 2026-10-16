package com.javaprep.day33.task01;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(EmployeeQueries.class)
class DerivedQueriesTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeeQueries queries;

    @BeforeEach
    void seed() {
        repository.saveAll(List.of(
                new Employee("Ann", "Eng", "100", true, "2020-01-10"),
                new Employee("Bob", "Eng", "80", true, "2021-05-01"),
                new Employee("Cid", "Eng", "60", false, "2019-03-03"),
                new Employee("Dee", "Ops", "70", true, "2022-07-07"),
                new Employee("Eve", "Ops", "50", true, "2018-02-02"),
                new Employee("Fay", "HR", "40", false, "2023-09-09")));
        repository.flush();
    }

    private static List<String> names(List<Employee> list) {
        return list.stream().map(Employee::getName).toList();
    }

    @Test
    void byDepartment() {
        assertThat(names(queries.inDepartment("Eng"))).containsExactlyInAnyOrder("Ann", "Bob", "Cid");
        assertThat(queries.inDepartment("Nope")).isEmpty();
    }

    @Test
    void byDepartmentAndActive() {
        assertThat(names(queries.activeIn("Eng"))).containsExactlyInAnyOrder("Ann", "Bob");
    }

    @Test
    void salaryThresholdOrderedDescending() {
        assertThat(names(queries.earningAtLeast(new BigDecimal("70")))).containsExactly("Ann", "Bob", "Dee");
    }

    @Test
    void nameContainsIgnoresCase() {
        assertThat(names(queries.nameContains("E"))).containsExactlyInAnyOrder("Dee", "Eve");
    }

    @Test
    void countAndExists() {
        assertThat(queries.headcount("Ops")).isEqualTo(2);
        assertThat(queries.nameTaken("aNN")).isTrue();
        assertThat(queries.nameTaken("Zed")).isFalse();
    }

    @Test
    void topTwo() {
        assertThat(names(queries.topTwoPaid())).containsExactly("Ann", "Bob");
    }

    @Test
    void hiredBetweenIsInclusive() {
        assertThat(names(queries.hiredBetween(LocalDate.parse("2019-03-03"), LocalDate.parse("2021-05-01"))))
                .containsExactlyInAnyOrder("Cid", "Ann", "Bob");
    }

    @Test
    void purgeInactiveReturnsCount() {
        assertThat(queries.purgeInactive()).isEqualTo(2);
        assertThat(repository.count()).isEqualTo(4);
    }
}
