package com.javaprep.day33.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(EmployeeReports.class)
class JpqlQueriesTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeeReports reports;

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
    void searchIgnoresCaseAndOrdersByName() {
        assertThat(reports.search("E")).extracting(Employee::getName).containsExactly("Dee", "Eve");
        assertThat(reports.search("zzz")).isEmpty();
    }

    @Test
    void aboveAverageUsesSubquery() {
        // average is 66.666...
        assertThat(reports.aboveAverage()).extracting(Employee::getName).containsExactly("Ann", "Bob", "Dee");
    }

    @Test
    void bulkRaiseUpdatesRowsAndRefreshesContext() {
        int updated = reports.giveRaise("Ops", new BigDecimal("1.10"));
        assertThat(updated).isEqualTo(2);
        List<Employee> ops = repository.findAll().stream().filter(e -> e.getDepartment().equals("Ops")).toList();
        assertThat(ops).extracting(Employee::getSalary).usingComparatorForType(BigDecimal::compareTo, BigDecimal.class)
                .containsExactlyInAnyOrder(new BigDecimal("77.00"), new BigDecimal("55.00"));
    }

    @Test
    void raiseForUnknownDepartmentUpdatesNothing() {
        assertThat(reports.giveRaise("Nope", new BigDecimal("2"))).isZero();
    }

    @Test
    void payrollGroupsByDepartment() {
        List<DeptTotal> totals = reports.payroll();
        assertThat(totals).extracting(DeptTotal::getDepartment).containsExactly("Eng", "HR", "Ops");
        assertThat(totals.get(0).getTotal()).isEqualByComparingTo("240");
        assertThat(totals.get(2).getTotal()).isEqualByComparingTo("120");
    }
}
