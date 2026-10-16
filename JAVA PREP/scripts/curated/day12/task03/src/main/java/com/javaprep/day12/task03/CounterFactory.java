package com.javaprep.day12.task03;

public class CounterFactory {

    /** Nested counter; each instance has independent state. */
    public static class Counter {

        private int value;

        Counter(int start) {
            this.value = start;
        }

        // TODO(Day12-task03): return the current value
        public int value() {
            throw new UnsupportedOperationException("TODO(Day12-task03): implement Counter.value");
        }

        // TODO(Day12-task03): add 1 and return the NEW value
        public int increment() {
            throw new UnsupportedOperationException("TODO(Day12-task03): implement Counter.increment");
        }
    }

    // TODO(Day12-task03): return a new Counter starting at `start`
    public static Counter newCounter(int start) {
        throw new UnsupportedOperationException("TODO(Day12-task03): implement newCounter");
    }
}
