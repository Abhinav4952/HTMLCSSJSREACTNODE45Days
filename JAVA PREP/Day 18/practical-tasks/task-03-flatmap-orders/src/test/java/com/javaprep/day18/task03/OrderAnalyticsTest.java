package com.javaprep.day18.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.within;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class OrderAnalyticsTest {

    private static final List<Order> ORDERS = List.of(
            new Order("o1", List.of(new LineItem("B", 1, 10.0), new LineItem("A", 2, 2.5))),
            new Order("o2", null),
            new Order("o3", List.of(new LineItem("A", 3, 2.5), new LineItem("C", 5, 1.0))),
            new Order("o4", List.of()));

    @Test
    void r1_allSkusDistinctSorted() {
        assertThat(OrderAnalytics.allSkus(ORDERS)).containsExactly("A", "B", "C");
        assertThat(OrderAnalytics.allSkus(List.of())).isEmpty();
    }

    @Test
    void r2_totalUnits() {
        assertThat(OrderAnalytics.totalUnits(ORDERS)).isEqualTo(11);
        assertThat(OrderAnalytics.totalUnits(List.of())).isZero();
    }

    @Test
    void r3_totalRevenue() {
        assertThat(OrderAnalytics.totalRevenue(ORDERS)).isCloseTo(10.0 + 5.0 + 7.5 + 5.0, within(1e-9));
        assertThat(OrderAnalytics.totalRevenue(List.of(new Order("x", null)))).isZero();
    }

    @Test
    void r4_unitsBySku() {
        var units = OrderAnalytics.unitsBySku(ORDERS);
        assertThat(new ArrayList<>(units.keySet())).containsExactly("A", "B", "C");
        assertThat(units.get("A")).isEqualTo(5);
        assertThat(units.get("B")).isEqualTo(1);
        assertThat(units.get("C")).isEqualTo(5);
    }

    @Test
    void r5_bestSellerTieBreaksAlphabetically() {
        assertThat(OrderAnalytics.bestSellerSku(ORDERS)).contains("A");
        List<Order> single = List.of(new Order("o", List.of(new LineItem("Z", 9, 1.0), new LineItem("Y", 1, 1.0))));
        assertThat(OrderAnalytics.bestSellerSku(single)).contains("Z");
        assertThat(OrderAnalytics.bestSellerSku(List.of(new Order("e", null)))).isEmpty();
        assertThat(OrderAnalytics.bestSellerSku(List.of())).isEmpty();
    }

    @Test
    void r6_flattenWords() {
        assertThat(OrderAnalytics.flattenWords(List.of("to be", "  or   not ", "", "  "))).containsExactly("to", "be", "or", "not");
        assertThat(OrderAnalytics.flattenWords(List.of())).isEmpty();
    }

    @Test
    void r7_nullItemListsAreEmpty() {
        List<Order> onlyNull = List.of(new Order("a", null), new Order("b", null));
        assertThat(OrderAnalytics.allSkus(onlyNull)).isEmpty();
        assertThat(OrderAnalytics.totalUnits(onlyNull)).isZero();
        assertThat(OrderAnalytics.unitsBySku(onlyNull)).isEmpty();
    }
}
