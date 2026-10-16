package com.javaprep.day33.task03;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Slice;
import org.springframework.data.domain.Sort;

@DataJpaTest
@Import(EmployeePaging.class)
class PagingAndNativeTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeePaging paging;

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

    @Test
    void firstPageSortedBySalaryDescending() {
        Page<Employee> p = paging.department("Eng", PageRequest.of(0, 2, Sort.by("salary").descending()));
        assertThat(p.getContent()).extracting(Employee::getName).containsExactly("Ann", "Bob");
        assertThat(p.getTotalElements()).isEqualTo(3);
        assertThat(p.getTotalPages()).isEqualTo(2);
        assertThat(p.hasNext()).isTrue();
    }

    @Test
    void lastPage() {
        Page<Employee> p = paging.department("Eng", PageRequest.of(1, 2, Sort.by("salary").descending()));
        assertThat(p.getContent()).extracting(Employee::getName).containsExactly("Cid");
        assertThat(p.isLast()).isTrue();
    }

    @Test
    void sliceKnowsOnlyWhetherThereIsMore() {
        Slice<Employee> s = paging.activeSlice(PageRequest.of(0, 3, Sort.by("name")));
        assertThat(s.getContent()).extracting(Employee::getName).containsExactly("Ann", "Bob", "Dee");
        assertThat(s.hasNext()).isTrue();
        assertThat(paging.activeSlice(PageRequest.of(1, 3, Sort.by("name"))).hasNext()).isFalse();
    }

    @Test
    void nativeAggregateThroughProjection() {
        List<DeptCount> counts = paging.headcounts();
        assertThat(counts).extracting(DeptCount::getDepartment).containsExactly("Eng", "HR", "Ops");
        assertThat(counts).extracting(DeptCount::getHeadcount).containsExactly(3L, 1L, 2L);
    }

    @Test
    void nativePagedQueryUsesCountQuery() {
        Page<Employee> p = paging.wellPaid(new BigDecimal("60"), PageRequest.of(0, 3));
        assertThat(p.getTotalElements()).isEqualTo(4);
        assertThat(p.getContent()).hasSize(3);
        assertThat(paging.wellPaid(new BigDecimal("60"), PageRequest.of(1, 3)).getContent()).hasSize(1);
    }

    @Test
    void describeFormatsPageInfo() {
        Page<Employee> p = paging.department("Eng", PageRequest.of(1, 2));
        assertThat(EmployeePaging.describe(p)).isEqualTo("page 2/2 (3 items total)");
    }
}
