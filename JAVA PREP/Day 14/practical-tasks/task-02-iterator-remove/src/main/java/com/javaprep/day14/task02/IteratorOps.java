package com.javaprep.day14.task02;

import java.util.ArrayList;
import java.util.Collection;
import java.util.ConcurrentModificationException;
import java.util.Iterator;
import java.util.List;
import java.util.ListIterator;
import java.util.function.Predicate;

/** Iterator-based mutation helpers. */
public final class IteratorOps {

    private IteratorOps() {
    }

    public static int removeNegatives(List<Integer> list) {
        // TODO(Day14-task02): remove every negative value in place via Iterator.remove() and return the number removed
        throw new UnsupportedOperationException("TODO(Day14-task02): removeNegatives");
    }

    public static <T> int removeMatching(Collection<T> collection, Predicate<? super T> predicate) {
        // TODO(Day14-task02): remove every element matching predicate in place using an explicit Iterator (not removeIf); return the count
        throw new UnsupportedOperationException("TODO(Day14-task02): removeMatching");
    }

    public static void duplicateEvens(List<Integer> list) {
        // TODO(Day14-task02): using a ListIterator, insert a copy immediately after every even value (e.g. [1,2,3,4] -> [1,2,2,3,4,4])
        throw new UnsupportedOperationException("TODO(Day14-task02): duplicateEvens");
    }

    public static boolean forEachRemovalThrows(List<String> input, String toRemove) {
        // TODO(Day14-task02): copy input into an ArrayList, remove toRemove inside a for-each, return true if ConcurrentModificationException was thrown else false
        throw new UnsupportedOperationException("TODO(Day14-task02): forEachRemovalThrows");
    }
}
