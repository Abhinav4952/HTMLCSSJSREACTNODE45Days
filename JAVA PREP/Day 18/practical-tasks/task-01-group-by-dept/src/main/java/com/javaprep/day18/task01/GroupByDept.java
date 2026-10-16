package com.javaprep.day18.task01;

import java.util.Comparator;
import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.stream.Collectors;

/** Department reports built with groupingBy. */
public final class GroupByDept {

    private GroupByDept() {
    }

    public static SortedMap<String, List<String>> namesByDept(List<Emp> emps) {
        // TODO(Day18-task01): groupingBy(dept, TreeMap::new, mapping(name, toList()))
        throw new UnsupportedOperationException("TODO(Day18-task01): namesByDept");
    }

    public static SortedMap<String, Double> totalSalaryByDept(List<Emp> emps) {
        // TODO(Day18-task01): groupingBy(dept, TreeMap::new, summingDouble(salary))
        throw new UnsupportedOperationException("TODO(Day18-task01): totalSalaryByDept");
    }

    public static SortedMap<String, Double> averageSalaryByDept(List<Emp> emps) {
        // TODO(Day18-task01): groupingBy(dept, TreeMap::new, averagingDouble(salary))
        throw new UnsupportedOperationException("TODO(Day18-task01): averageSalaryByDept");
    }

    public static SortedMap<String, Long> headcountByDept(List<Emp> emps) {
        // TODO(Day18-task01): groupingBy(dept, TreeMap::new, counting())
        throw new UnsupportedOperationException("TODO(Day18-task01): headcountByDept");
    }

    public static SortedMap<String, String> topEarnerByDept(List<Emp> emps) {
        // TODO(Day18-task01): groupingBy(dept, TreeMap::new, collectingAndThen(maxBy(by salary), optional -> optional.orElseThrow().name())); first listed wins ties
        throw new UnsupportedOperationException("TODO(Day18-task01): topEarnerByDept");
    }
}
