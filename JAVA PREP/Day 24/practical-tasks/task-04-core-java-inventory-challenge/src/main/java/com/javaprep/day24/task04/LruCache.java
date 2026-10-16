package com.javaprep.day24.task04;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Least-recently-used cache built on an access-ordered LinkedHashMap. */
public final class LruCache<K, V> {

    private final Map<K, V> map;

    public LruCache(int capacity) {
        // TODO(Day24-task04): capacity <= 0 -> IllegalArgumentException; create new LinkedHashMap<>(16, 0.75f, true) overriding removeEldestEntry to evict when size() > capacity
        throw new UnsupportedOperationException("TODO(Day24-task04): constructor");
    }

    public V get(K key) {
        // TODO(Day24-task04): return map.get(key) (null when absent); access order makes it the most recently used
        throw new UnsupportedOperationException("TODO(Day24-task04): get");
    }

    public void put(K key, V value) {
        // TODO(Day24-task04): map.put(key, value); an overwrite also refreshes the key
        throw new UnsupportedOperationException("TODO(Day24-task04): put");
    }

    public int size() {
        return map.size();
    }

    public List<K> keys() {
        // TODO(Day24-task04): a new ArrayList of the key set: eldest (least recently used) first
        throw new UnsupportedOperationException("TODO(Day24-task04): keys");
    }
}
