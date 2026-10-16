package com.javaprep.day33.task04;

/** Closed interface projection: Spring Data selects only these two columns. */
public interface EmployeeSummary {
    String getName();

    String getDepartment();
}
