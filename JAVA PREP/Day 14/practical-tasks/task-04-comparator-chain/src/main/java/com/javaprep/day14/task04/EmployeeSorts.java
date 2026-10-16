package com.javaprep.day14.task04;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/** Comparator factories. */
public final class EmployeeSorts {

    private EmployeeSorts() {
    }

    public static Comparator<Employee> byDeptThenSalaryDescThenName() {
        // TODO(Day14-task04): dept ascending, then salary descending, then name ascending, built with Comparator.comparing/thenComparing (no subtraction)
        throw new UnsupportedOperationException("TODO(Day14-task04): byDeptThenSalaryDescThenName");
    }

    public static Comparator<String> byNameIgnoreCaseNullsLast() {
        // TODO(Day14-task04): case-insensitive String comparator that sorts null last
        throw new UnsupportedOperationException("TODO(Day14-task04): byNameIgnoreCaseNullsLast");
    }

    public static <T> Comparator<T> chain(List<Comparator<T>> comparators) {
        // TODO(Day14-task04): combine comparators so that later ones only break ties of earlier ones; empty list -> everything equal
        throw new UnsupportedOperationException("TODO(Day14-task04): chain");
    }

    public static <T> List<T> sortedCopy(List<T> input, Comparator<? super T> comparator) {
        // TODO(Day14-task04): return a new ArrayList sorted with comparator (stable); do not modify input
        throw new UnsupportedOperationException("TODO(Day14-task04): sortedCopy");
    }
}
