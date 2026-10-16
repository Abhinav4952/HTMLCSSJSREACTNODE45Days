package com.javaprep.day42.task03;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.CachePut;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class PriceService {

    private final Map<String, Double> database = new ConcurrentHashMap<>(Map.of("pen", 1.5, "book", 12.0));
    private final AtomicInteger loads = new AtomicInteger();

    /** PROVIDED instrumentation: how many times the "slow" source was really hit. */
    public int loads() {
        return loads.get();
    }

    public void resetLoads() {
        loads.set(0);
    }

    /** Cache "prices", key = sku; unknown skus (null result) must NOT be cached. */
    // TODO(Day42-task03): @Cacheable in cache "prices", skip caching null results (unless = "#result == null")
    public Double priceOf(String sku) {
        loads.incrementAndGet();
        return database.get(sku);
    }

    /** Updates the source AND the cache entry for this sku (return value is stored under key sku). */
    // TODO(Day42-task03): @CachePut in cache "prices" with key "#sku"
    public Double setPrice(String sku, double price) {
        database.put(sku, price);
        return price;
    }

    /** Removes the cache entry of one sku. */
    // TODO(Day42-task03): @CacheEvict in cache "prices" with key "#sku"
    public void evict(String sku) {
    }

    /** Removes every entry of the cache "prices". */
    // TODO(Day42-task03): @CacheEvict in cache "prices" with allEntries = true
    public void evictAll() {
    }

    /** Cache "rates" with the composite key "<from>-><to>" built with SpEL. */
    // TODO(Day42-task03): @Cacheable in cache "rates" with key "#from + '->' + #to"
    public double rate(String from, String to) {
        loads.incrementAndGet();
        return from.equals(to) ? 1.0 : 0.9;
    }
}
