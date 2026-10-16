package com.javaprep.day18.task01;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class GroupByDeptTest {

    private static final List<Emp> EMPS = List.of(
            new Emp("Ann", "ENG", 120),
            new Emp("Bob", "HR", 80),
            new Emp("Cy", "ENG", 100),
            new Emp("Di", "OPS", 70),
            new Emp("Eve", "HR", 80),
            new Emp("Flo", "ENG", 120));

    @Test
    void r1_namesByDeptSortedAndInInputOrder() {
        var names = GroupByDept.namesByDept(EMPS);
        assertThat(new ArrayList<>(names.keySet())).containsExactly("ENG", "HR", "OPS");
        assertThat(names.get("ENG")).containsExactly("Ann", "Cy", "Flo");
        assertThat(names.get("HR")).containsExactly("Bob", "Eve");
        assertThat(names.get("OPS")).containsExactly("Di");
    }

    @Test
    void r2_totalSalary() {
        var totals = GroupByDept.totalSalaryByDept(EMPS);
        assertThat(totals.get("ENG")).isEqualTo(340.0);
        assertThat(totals.get("HR")).isEqualTo(160.0);
        assertThat(totals.get("OPS")).isEqualTo(70.0);
    }

    @Test
    void r3_averageSalary() {
        var avg = GroupByDept.averageSalaryByDept(EMPS);
        assertThat(avg.get("ENG")).isCloseTo(113.3333, org.assertj.core.data.Offset.offset(0.001));
        assertThat(avg.get("HR")).isEqualTo(80.0);
    }

    @Test
    void r4_headcount() {
        var counts = GroupByDept.headcountByDept(EMPS);
        assertThat(counts.get("ENG")).isEqualTo(3L);
        assertThat(counts.get("HR")).isEqualTo(2L);
        assertThat(counts.get("OPS")).isEqualTo(1L);
        assertThat(counts).hasSize(3);
    }

    @Test
    void r5_topEarnerFirstWinsTies() {
        var top = GroupByDept.topEarnerByDept(EMPS);
        assertThat(top.get("ENG")).isEqualTo("Ann");
        assertThat(top.get("HR")).isEqualTo("Bob");
        assertThat(top.get("OPS")).isEqualTo("Di");
    }

    @Test
    void emptyInputGivesEmptyMaps() {
        assertThat(GroupByDept.namesByDept(List.of())).isEmpty();
        assertThat(GroupByDept.totalSalaryByDept(List.of())).isEmpty();
        assertThat(GroupByDept.averageSalaryByDept(List.of())).isEmpty();
        assertThat(GroupByDept.headcountByDept(List.of())).isEmpty();
        assertThat(GroupByDept.topEarnerByDept(List.of())).isEmpty();
    }
}
