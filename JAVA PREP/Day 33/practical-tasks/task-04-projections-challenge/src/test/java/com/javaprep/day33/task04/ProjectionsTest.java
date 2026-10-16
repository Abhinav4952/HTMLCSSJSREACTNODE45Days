package com.javaprep.day33.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(EmployeeProjections.class)
class ProjectionsTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeeProjections projections;

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
    void closedProjectionCarriesOnlyTwoValues() {
        List<EmployeeSummary> s = projections.activeSummaries();
        assertThat(s).extracting(EmployeeSummary::getName).containsExactly("Ann", "Bob", "Dee", "Eve");
        assertThat(s.get(0).getDepartment()).isEqualTo("Eng");
    }

    @Test
    void openProjectionComputesLabel() {
        assertThat(projections.labels("Ops")).containsExactly("Dee (Ops)", "Eve (Ops)");
    }

    @Test
    void constructorExpressionBuildsDtos() {
        List<EmployeeRow> rows = projections.rows("Eng");
        assertThat(rows).extracting(EmployeeRow::name).containsExactly("Ann", "Bob", "Cid");
        assertThat(rows.get(0).salary()).isEqualByComparingTo("100");
    }

    @Test
    void dynamicProjectionChoosesTypeAtCallSite() {
        assertThat(projections.byDepartment("HR", EmployeeSummary.class)).extracting(EmployeeSummary::getName).containsExactly("Fay");
        assertThat(projections.byDepartment("HR", Employee.class)).hasSize(1).first().isInstanceOf(Employee.class);
        assertThat(projections.byDepartment("Eng", EmployeeRow.class)).extracting(EmployeeRow::name).containsExactly("Ann", "Bob", "Cid");
    }
}
