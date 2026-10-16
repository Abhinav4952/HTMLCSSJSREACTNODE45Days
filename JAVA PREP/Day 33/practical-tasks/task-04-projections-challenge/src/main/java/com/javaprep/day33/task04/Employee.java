package com.javaprep.day33.task04;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "employees")
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String department;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal salary;

    @Column(nullable = false)
    private boolean active;

    @Column(name = "hired_on", nullable = false)
    private LocalDate hiredOn;

    protected Employee() {
    }

    public Employee(String name, String department, String salary, boolean active, String hiredOn) {
        this.name = name;
        this.department = department;
        this.salary = new BigDecimal(salary);
        this.active = active;
        this.hiredOn = LocalDate.parse(hiredOn);
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDepartment() {
        return department;
    }

    public BigDecimal getSalary() {
        return salary;
    }

    public boolean isActive() {
        return active;
    }

    public LocalDate getHiredOn() {
        return hiredOn;
    }
}
