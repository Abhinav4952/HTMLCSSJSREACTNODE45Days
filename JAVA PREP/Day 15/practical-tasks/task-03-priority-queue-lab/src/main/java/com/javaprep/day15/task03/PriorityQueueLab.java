package com.javaprep.day15.task03;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Deque;
import java.util.List;
import java.util.PriorityQueue;

/** Queue, Deque, and PriorityQueue exercises. */
public final class PriorityQueueLab {

    private PriorityQueueLab() {
    }

    public static List<String> processOrder(List<Job> jobs) {
        // TODO(Day15-task03): offer all jobs into a PriorityQueue (priority desc, then id asc) and poll them into a list of ids
        throw new UnsupportedOperationException("TODO(Day15-task03): processOrder");
    }

    public static List<Integer> kSmallest(List<Integer> values, int k) {
        // TODO(Day15-task03): keep a max-heap of at most k items (evict the largest), then return them in ascending order; k <= 0 gives an empty list
        throw new UnsupportedOperationException("TODO(Day15-task03): kSmallest");
    }

    public static boolean isBalanced(String text) {
        // TODO(Day15-task03): use an ArrayDeque as a stack: push openers, pop and match on closers; ignore other characters; true only if the stack ends empty
        throw new UnsupportedOperationException("TODO(Day15-task03): isBalanced");
    }

    public static <T> List<T> rotateLeft(List<T> items, int k) {
        // TODO(Day15-task03): load items into an ArrayDeque, move the head to the tail (k mod size) times, return a new list; empty list gives empty list
        throw new UnsupportedOperationException("TODO(Day15-task03): rotateLeft");
    }
}
