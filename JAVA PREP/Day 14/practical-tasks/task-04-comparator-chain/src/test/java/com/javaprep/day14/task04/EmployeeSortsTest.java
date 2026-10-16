package com.javaprep.day14.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import org.junit.jupiter.api.Test;

class EmployeeSortsTest {

    private static final Employee ZED = new Employee("Zed", "ENG", 30, 100);
    private static final Employee AMY = new Employee("Amy", "ENG", 41, 120);
    private static final Employee BOB = new Employee("Bob", "HR", 25, 90);
    private static final Employee ANN = new Employee("Ann", "ENG", 29, 100);
    private static final Employee CAL = new Employee("Cal", "AUD", 50, 70);

    @Test
    void r1_deptThenSalaryDescThenName() {
        List<Employee> list = new ArrayList<>(List.of(BOB, ZED, AMY, ANN, CAL));
        list.sort(EmployeeSorts.byDeptThenSalaryDescThenName());
        assertThat(list).containsExactly(CAL, AMY, ANN, ZED, BOB);
    }

    @Test
    void r1_comparatorIsSymmetric() {
        Comparator<Employee> c = EmployeeSorts.byDeptThenSalaryDescThenName();
        assertThat(c.compare(AMY, ZED)).isNegative();
        assertThat(c.compare(ZED, AMY)).isPositive();
        assertThat(c.compare(ZED, new Employee("Zed", "ENG", 99, 100))).isZero();
    }

    @Test
    void r2_nameIgnoreCaseNullsLast() {
        List<String> names = new ArrayList<>(Arrays.asList("bob", null, "Alice", "CAROL", "alice"));
        names.sort(EmployeeSorts.byNameIgnoreCaseNullsLast());
        assertThat(names.subList(0, 4)).extracting(String::toLowerCase).containsExactly("alice", "alice", "bob", "carol");
        assertThat(names.get(4)).isNull();
    }

    @Test
    void r3_chainAppliesComparatorsInOrder() {
        Comparator<Employee> byAge = Comparator.comparingInt(Employee::age);
        Comparator<Employee> byDept = Comparator.comparing(Employee::dept);
        Comparator<Employee> chained = EmployeeSorts.chain(List.of(byDept, byAge));
        List<Employee> list = new ArrayList<>(List.of(BOB, AMY, ZED, CAL));
        list.sort(chained);
        assertThat(list).containsExactly(CAL, ZED, AMY, BOB);
    }

    @Test
    void r3_emptyChainTreatsEverythingEqual() {
        Comparator<String> none = EmployeeSorts.chain(List.of());
        assertThat(none.compare("a", "b")).isZero();
        List<String> list = new ArrayList<>(List.of("b", "a", "c"));
        list.sort(none);
        assertThat(list).containsExactly("b", "a", "c");
    }

    @Test
    void r4_sortedCopyLeavesInputUntouched() {
        List<Employee> input = new ArrayList<>(List.of(BOB, AMY, CAL));
        List<Employee> sorted = EmployeeSorts.sortedCopy(input, EmployeeSorts.byDeptThenSalaryDescThenName());
        assertThat(sorted).containsExactly(CAL, AMY, BOB);
        assertThat(input).containsExactly(BOB, AMY, CAL);
        assertThat(sorted).isNotSameAs(input);
    }

    @Test
    void r4_sortIsStable() {
        Employee first = new Employee("Same", "X", 1, 1);
        Employee second = new Employee("Same", "X", 2, 1);
        Employee third = new Employee("Same", "X", 3, 1);
        List<Employee> sorted = EmployeeSorts.sortedCopy(List.of(first, second, third), EmployeeSorts.byDeptThenSalaryDescThenName());
        assertThat(sorted).containsExactly(first, second, third);
    }
}
