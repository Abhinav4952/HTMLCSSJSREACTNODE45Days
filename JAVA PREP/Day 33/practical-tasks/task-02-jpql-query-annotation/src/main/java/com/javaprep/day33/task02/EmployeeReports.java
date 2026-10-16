package com.javaprep.day33.task02;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
public class EmployeeReports {

    private final EmployeeRepository repository;

    public EmployeeReports(EmployeeRepository repository) {
        this.repository = repository;
    }

    public List<Employee> search(String q) {
        // TODO(Day33-task02): delegate to repository.search
        throw new UnsupportedOperationException("TODO(Day33-task02): delegate to repository.search");
    }

    public List<Employee> aboveAverage() {
        // TODO(Day33-task02): delegate to repository.aboveAverage
        throw new UnsupportedOperationException("TODO(Day33-task02): delegate to repository.aboveAverage");
    }

    /** @return number of employees updated */
    @Transactional
    public int giveRaise(String department, BigDecimal factor) {
        // TODO(Day33-task02): delegate to repository.raise
        throw new UnsupportedOperationException("TODO(Day33-task02): delegate to repository.raise");
    }

    public List<DeptTotal> payroll() {
        // TODO(Day33-task02): delegate to repository.payroll
        throw new UnsupportedOperationException("TODO(Day33-task02): delegate to repository.payroll");
    }
}
