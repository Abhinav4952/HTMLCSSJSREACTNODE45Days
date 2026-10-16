package com.javaprep.day18.task03;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/** flatMap-based analytics. */
public final class OrderAnalytics {

    private OrderAnalytics() {
    }

    private static Stream<LineItem> lines(List<Order> orders) {
        return orders.stream().flatMap(o -> o.items() == null ? Stream.<LineItem>empty() : o.items().stream());
    }

    public static List<String> allSkus(List<Order> orders) {
        // TODO(Day18-task03): flatten to line items, map to sku, distinct, sorted
        throw new UnsupportedOperationException("TODO(Day18-task03): allSkus");
    }

    public static int totalUnits(List<Order> orders) {
        // TODO(Day18-task03): flatten and sum qty with mapToInt
        throw new UnsupportedOperationException("TODO(Day18-task03): totalUnits");
    }

    public static double totalRevenue(List<Order> orders) {
        // TODO(Day18-task03): flatten and sum qty * price with mapToDouble
        throw new UnsupportedOperationException("TODO(Day18-task03): totalRevenue");
    }

    public static SortedMap<String, Integer> unitsBySku(List<Order> orders) {
        // TODO(Day18-task03): groupingBy(sku, TreeMap::new, summingInt(qty)) over the flattened lines
        throw new UnsupportedOperationException("TODO(Day18-task03): unitsBySku");
    }

    public static Optional<String> bestSellerSku(List<Order> orders) {
        // TODO(Day18-task03): the SKU with most units; ties -> alphabetically first; Optional.empty() when there are no lines
        throw new UnsupportedOperationException("TODO(Day18-task03): bestSellerSku");
    }

    public static List<String> flattenWords(List<String> sentences) {
        // TODO(Day18-task03): flatMap each sentence to its whitespace-separated words, dropping empty tokens
        throw new UnsupportedOperationException("TODO(Day18-task03): flattenWords");
    }
}
