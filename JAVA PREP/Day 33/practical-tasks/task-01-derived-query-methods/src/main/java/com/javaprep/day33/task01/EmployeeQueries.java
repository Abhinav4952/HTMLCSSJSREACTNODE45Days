package com.javaprep.day33.task01;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

/** Facade the tests call. Each method must delegate to ONE derived query on the repository. */
@Component
public class EmployeeQueries {

    private final EmployeeRepository repository;

    public EmployeeQueries(EmployeeRepository repository) {
        this.repository = repository;
    }

    public List<Employee> inDepartment(String department) {
        // TODO(Day33-task01): delegate to findByDepartment
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to findByDepartment");
    }

    public List<Employee> activeIn(String department) {
        // TODO(Day33-task01): delegate to findByDepartmentAndActiveTrue
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to findByDepartmentAndActiveTrue");
    }

    /** Highest salary first. */
    public List<Employee> earningAtLeast(BigDecimal min) {
        // TODO(Day33-task01): delegate to findBySalaryGreaterThanEqualOrderBySalaryDesc
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to findBySalaryGreaterThanEqualOrderBySalaryDesc");
    }

    public List<Employee> nameContains(String fragment) {
        // TODO(Day33-task01): delegate to findByNameContainingIgnoreCase
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to findByNameContainingIgnoreCase");
    }

    public long headcount(String department) {
        // TODO(Day33-task01): delegate to countByDepartment
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to countByDepartment");
    }

    public boolean nameTaken(String name) {
        // TODO(Day33-task01): delegate to existsByNameIgnoreCase
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to existsByNameIgnoreCase");
    }

    public List<Employee> topTwoPaid() {
        // TODO(Day33-task01): delegate to findTop2ByOrderBySalaryDesc
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to findTop2ByOrderBySalaryDesc");
    }

    /** Inclusive on both ends. */
    public List<Employee> hiredBetween(LocalDate from, LocalDate to) {
        // TODO(Day33-task01): delegate to findByHiredOnBetween
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to findByHiredOnBetween");
    }

    @Transactional
    public long purgeInactive() {
        // TODO(Day33-task01): delegate to deleteByActiveFalse and return the number of deleted rows
        throw new UnsupportedOperationException("TODO(Day33-task01): delegate to deleteByActiveFalse and return the number of deleted rows");
    }
}
