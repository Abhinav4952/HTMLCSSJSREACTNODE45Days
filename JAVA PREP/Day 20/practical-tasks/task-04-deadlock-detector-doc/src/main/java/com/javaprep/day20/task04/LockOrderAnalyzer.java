package com.javaprep.day20.task04;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import java.util.SortedSet;
import java.util.TreeSet;

/** Static analysis of lock acquisition orders. Each inner list is one thread's lock order. */
public final class LockOrderAnalyzer {

    private LockOrderAnalyzer() {
    }

    public static SortedSet<String> conflictingPairs(List<List<String>> threadLockOrders) {
        // TODO(Day20-task04): collect every (x before y) relation per thread (first occurrence only); report 'A<->B' (A < B alphabetically) when both (x,y) and (y,x) occur in different threads
        throw new UnsupportedOperationException("TODO(Day20-task04): conflictingPairs");
    }

    public static boolean hasOrderingRisk(List<List<String>> threadLockOrders) {
        // TODO(Day20-task04): true when conflictingPairs is not empty
        throw new UnsupportedOperationException("TODO(Day20-task04): hasOrderingRisk");
    }

    public static List<String> coffmanConditions() {
        // TODO(Day20-task04): return exactly: 'Mutual exclusion', 'Hold and wait', 'No preemption', 'Circular wait' (in this order)
        throw new UnsupportedOperationException("TODO(Day20-task04): coffmanConditions");
    }

    public static String advice(List<List<String>> threadLockOrders) {
        // TODO(Day20-task04): 'No lock-ordering conflicts found.' when safe; otherwise mention each pair and recommend a 'global order' listing all lock names alphabetically
        throw new UnsupportedOperationException("TODO(Day20-task04): advice");
    }
}
