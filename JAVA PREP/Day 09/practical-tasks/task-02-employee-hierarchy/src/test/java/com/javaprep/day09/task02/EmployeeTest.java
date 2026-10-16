package com.javaprep.day09.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.List;

class EmployeeTest {

    @Test
    @DisplayName("Employee pays base")
    void employee() {
        assertThat(new Employee("Ann", 1000.0).pay()).isEqualTo(1000.0);
    }

    @Test
    @DisplayName("Manager pays base + bonus")
    void manager() {
        assertThat(new Manager("Bob", 2000.0, 500.0).pay()).isEqualTo(2500.0);
        assertThat(new Manager("Zed", 2000.0, 0.0).pay()).isEqualTo(2000.0);
    }

    @Test
    @DisplayName("polymorphic payroll total")
    void payroll() {
        List<Employee> staff = List.of(new Employee("Ann", 1000.0), new Manager("Bob", 2000.0, 500.0));
        double total = staff.stream().mapToDouble(Employee::pay).sum();
        assertThat(total).isEqualTo(3500.0);
        assertThat(staff.get(1)).isInstanceOf(Employee.class);
    }
}
