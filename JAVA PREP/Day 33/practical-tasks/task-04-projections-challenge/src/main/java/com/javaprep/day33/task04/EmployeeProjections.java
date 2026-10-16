package com.javaprep.day33.task04;

import java.util.List;
import org.springframework.stereotype.Component;

@Component
public class EmployeeProjections {

    private final EmployeeRepository repository;

    public EmployeeProjections(EmployeeRepository repository) {
        this.repository = repository;
    }

    public List<EmployeeSummary> activeSummaries() {
        // TODO(Day33-task04): closed projection
        throw new UnsupportedOperationException("TODO(Day33-task04): closed projection");
    }

    public List<String> labels(String department) {
        // TODO(Day33-task04): open projection labels
        throw new UnsupportedOperationException("TODO(Day33-task04): open projection labels");
    }

    public List<EmployeeRow> rows(String department) {
        // TODO(Day33-task04): DTO projection via constructor expression
        throw new UnsupportedOperationException("TODO(Day33-task04): DTO projection via constructor expression");
    }

    public <T> List<T> byDepartment(String department, Class<T> type) {
        // TODO(Day33-task04): dynamic projection
        throw new UnsupportedOperationException("TODO(Day33-task04): dynamic projection");
    }
}
