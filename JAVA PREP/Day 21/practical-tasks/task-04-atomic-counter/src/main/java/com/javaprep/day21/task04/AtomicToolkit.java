package com.javaprep.day21.task04;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.LongAdder;
import java.util.concurrent.locks.ReentrantReadWriteLock;

/** Small thread-safe building blocks. */
public final class AtomicToolkit {

    private AtomicToolkit() {
    }

    /** Counts hits using an AtomicLong. */
    public static final class HitCounter {
        private final AtomicLong hits = new AtomicLong();

        public void hit() {
            // TODO(Day21-task04): atomically increment the counter (incrementAndGet / getAndIncrement)
            throw new UnsupportedOperationException("TODO(Day21-task04): hit");
        }

        public long count() {
            // TODO(Day21-task04): return the current number of hits
            throw new UnsupportedOperationException("TODO(Day21-task04): count");
        }

        public long reset() {
            // TODO(Day21-task04): atomically set the counter to 0 and return the previous value (getAndSet)
            throw new UnsupportedOperationException("TODO(Day21-task04): reset");
        }
    }

    /** Tracks the maximum value using a compare-and-set loop. */
    public static final class MaxTracker {
        private final AtomicInteger max = new AtomicInteger(Integer.MIN_VALUE);

        public void offer(int value) {
            // TODO(Day21-task04): CAS loop: read current, return if value <= current, else compareAndSet(current, value) and retry on failure
            throw new UnsupportedOperationException("TODO(Day21-task04): offer");
        }

        public int get() {
            // TODO(Day21-task04): return the maximum seen so far (Integer.MIN_VALUE when nothing was offered)
            throw new UnsupportedOperationException("TODO(Day21-task04): get");
        }
    }

    /** Counts words from many threads using ConcurrentHashMap + LongAdder. */
    public static final class WordCounter {
        private final ConcurrentHashMap<String, LongAdder> counts = new ConcurrentHashMap<>();

        public void add(String word) {
            // TODO(Day21-task04): counts.computeIfAbsent(word, k -> new LongAdder()).increment() - no containsKey/put race
            throw new UnsupportedOperationException("TODO(Day21-task04): add");
        }

        public long count(String word) {
            // TODO(Day21-task04): the adder's sum for the word, or 0 when the word is unknown
            throw new UnsupportedOperationException("TODO(Day21-task04): count");
        }

        public Map<String, Long> snapshot() {
            // TODO(Day21-task04): return a NEW HashMap word -> sum() (a point-in-time copy, not a view)
            throw new UnsupportedOperationException("TODO(Day21-task04): snapshot");
        }
    }

    /** Read-mostly string registry guarded by a read/write lock. */
    public static final class Registry {
        private final Map<String, String> map = new HashMap<>();
        private final ReentrantReadWriteLock lock = new ReentrantReadWriteLock();

        public void put(String key, String value) {
            // TODO(Day21-task04): take the WRITE lock, put into the map, release in finally
            throw new UnsupportedOperationException("TODO(Day21-task04): put");
        }

        public String get(String key) {
            // TODO(Day21-task04): take the READ lock, read, release in finally
            throw new UnsupportedOperationException("TODO(Day21-task04): get");
        }

        public int size() {
            // TODO(Day21-task04): take the READ lock, return map.size(), release in finally
            throw new UnsupportedOperationException("TODO(Day21-task04): size");
        }
    }
}
