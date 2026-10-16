package com.javaprep.day42.task03;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cache.CacheManager;

@SpringBootTest
class CachingTest {

    @Autowired
    PriceService service;
    @Autowired
    CacheManager cacheManager;

    @BeforeEach
    void clean() {
        cacheManager.getCacheNames().forEach(n -> cacheManager.getCache(n).clear());
        service.resetLoads();
    }

    @Test
    void cacheInfrastructureIsActive() {
        assertThat(AopUtils.isAopProxy(service)).isTrue();
        assertThat(cacheManager).isNotNull();
    }

    @Test
    void secondCallHitsTheCache() {
        assertThat(service.priceOf("pen")).isEqualTo(1.5);
        assertThat(service.priceOf("pen")).isEqualTo(1.5);
        assertThat(service.loads()).isEqualTo(1);
        assertThat(cacheManager.getCache("prices").get("pen")).isNotNull();
    }

    @Test
    void differentKeysAreCachedSeparately() {
        service.priceOf("pen");
        service.priceOf("book");
        service.priceOf("pen");
        assertThat(service.loads()).isEqualTo(2);
    }

    @Test
    void nullResultsAreNotCached() {
        assertThat(service.priceOf("ghost")).isNull();
        assertThat(service.priceOf("ghost")).isNull();
        assertThat(service.loads()).isEqualTo(2);
    }

    @Test
    void cachePutRefreshesTheEntryWithoutAnotherLoad() {
        service.priceOf("pen");
        service.setPrice("pen", 2.0);
        assertThat(service.priceOf("pen")).isEqualTo(2.0);
        assertThat(service.loads()).isEqualTo(1);
    }

    @Test
    void evictForcesReload() {
        service.priceOf("pen");
        service.evict("pen");
        service.priceOf("pen");
        assertThat(service.loads()).isEqualTo(2);
    }

    @Test
    void evictAllClearsEverything() {
        service.priceOf("pen");
        service.priceOf("book");
        service.evictAll();
        service.priceOf("pen");
        service.priceOf("book");
        assertThat(service.loads()).isEqualTo(4);
    }

    @Test
    void compositeSpelKey() {
        service.rate("EUR", "USD");
        service.rate("EUR", "USD");
        service.rate("USD", "EUR");
        assertThat(service.loads()).isEqualTo(2);
        assertThat(cacheManager.getCache("rates").get("EUR->USD")).isNotNull();
    }
}
