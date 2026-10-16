package com.javaprep.day33.task04;

import java.math.BigDecimal;

/** Class-based (DTO) projection. */
public record EmployeeRow(String name, BigDecimal salary) {
}
