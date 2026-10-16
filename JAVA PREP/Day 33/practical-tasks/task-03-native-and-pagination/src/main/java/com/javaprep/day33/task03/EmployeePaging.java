package com.javaprep.day33.task03;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Slice;
import org.springframework.stereotype.Component;

@Component
public class EmployeePaging {

    private final EmployeeRepository repository;

    public EmployeePaging(EmployeeRepository repository) {
        this.repository = repository;
    }

    public Page<Employee> department(String department, Pageable pageable) {
        // TODO(Day33-task03): delegate to findByDepartment
        throw new UnsupportedOperationException("TODO(Day33-task03): delegate to findByDepartment");
    }

    public Slice<Employee> activeSlice(Pageable pageable) {
        // TODO(Day33-task03): delegate to findByActiveTrue
        throw new UnsupportedOperationException("TODO(Day33-task03): delegate to findByActiveTrue");
    }

    public List<DeptCount> headcounts() {
        // TODO(Day33-task03): delegate to headcountNative
        throw new UnsupportedOperationException("TODO(Day33-task03): delegate to headcountNative");
    }

    public Page<Employee> wellPaid(BigDecimal min, Pageable pageable) {
        // TODO(Day33-task03): delegate to wellPaid
        throw new UnsupportedOperationException("TODO(Day33-task03): delegate to wellPaid");
    }

    /** Human readable summary for a page, e.g. "page 2/3 (5 items total)" for page index 1. */
    public static String describe(Page<?> page) {
        // TODO(Day33-task03): return page <number+1>/<totalPages> (<totalElements> items total)
        throw new UnsupportedOperationException("TODO(Day33-task03): return page <number+1>/<totalPages> (<totalElements> items total)");
    }
}
