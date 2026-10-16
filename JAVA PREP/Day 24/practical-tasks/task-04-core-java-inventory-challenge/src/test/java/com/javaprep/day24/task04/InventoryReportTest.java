package com.javaprep.day24.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.IntStream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

@Timeout(30)
class InventoryReportTest {

    private static final String CSV = """
            sku,category,qty,priceCents
            # seasonal stock
            A-1,books,10,1050
            A-2, toys ,5,250

            bad line
            A-3,toys,x,100
            A-4,books,-1,100
            ,books,1,100
            A-5,games,0,5999
            A-6,games,2,1,extra
            """;

    private static Item item(String sku, String category, int qty, long price) {
        return new Item(sku, category, qty, price);
    }

    // ------------------------------------------------------------------ r1 Item
    @Test
    void r1_itemTrimsAndComputesValue() {
        Item i = item("  X-1 ", " books ", 3, 1_000);
        assertThat(i.sku()).isEqualTo("X-1");
        assertThat(i.category()).isEqualTo("books");
        assertThat(i.valueCents()).isEqualTo(3_000L);
        assertThat(item("big", "c", Integer.MAX_VALUE, 1_000).valueCents()).isEqualTo(Integer.MAX_VALUE * 1_000L);
        assertThat(item("a", "b", 1, 1)).isEqualTo(item("a", "b", 1, 1));
    }

    @Test
    void r1_itemValidation() {
        assertThatThrownBy(() -> item(null, "c", 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("sku");
        assertThatThrownBy(() -> item(" ", "c", 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("sku");
        assertThatThrownBy(() -> item("a", null, 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("category");
        assertThatThrownBy(() -> item("a", "", 1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("category");
        assertThatThrownBy(() -> item("a", "c", -1, 1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("qty");
        assertThatThrownBy(() -> item("a", "c", 1, -1)).isInstanceOf(IllegalArgumentException.class).hasMessageContaining("price");
        assertThat(item("a", "c", 0, 0).valueCents()).isZero();
    }

    // ------------------------------------------------------------------ r2 parseLine / parse
    @Test
    void r2_parseLineSuccess() {
        assertThat(InventoryReport.parseLine(7, "A-1,books,10,1050")).isEqualTo(new ParseResult.Ok(item("A-1", "books", 10, 1050)));
        assertThat(InventoryReport.parseLine(7, " B , c , 1 , 2 ")).isEqualTo(new ParseResult.Ok(item("B", "c", 1, 2)));
    }

    @Test
    void r2_parseLineFailuresNeverThrow() {
        ParseResult fields = InventoryReport.parseLine(5, "bad line");
        assertThat(fields).isEqualTo(new ParseResult.Failed(5, "expected 4 fields but found 1"));
        assertThat(InventoryReport.parseLine(6, "a,b,1,2,3")).isEqualTo(new ParseResult.Failed(6, "expected 4 fields but found 5"));

        assertThat(InventoryReport.parseLine(1, "a,b,x,2")).isInstanceOfSatisfying(ParseResult.Failed.class,
                f -> assertThat(f.reason()).startsWith("invalid number"));
        assertThat(InventoryReport.parseLine(1, "a,b,1,2.5")).isInstanceOf(ParseResult.Failed.class);
        assertThat(InventoryReport.parseLine(1, "a,b,99999999999,2")).isInstanceOf(ParseResult.Failed.class);
        assertThat(InventoryReport.parseLine(2, "a,b,-1,2")).isInstanceOfSatisfying(ParseResult.Failed.class,
                f -> assertThat(f.reason()).contains("qty"));
        assertThat(InventoryReport.parseLine(3, ",b,1,2")).isInstanceOfSatisfying(ParseResult.Failed.class,
                f -> assertThat(f.reason()).contains("sku"));
    }

    @Test
    void r2_parseSkipsNoiseAndNumbersPhysicalLines() {
        List<ParseResult> results = InventoryReport.parse(CSV);
        assertThat(results).hasSize(8);
        assertThat(results.get(0)).isEqualTo(new ParseResult.Ok(item("A-1", "books", 10, 1050)));
        assertThat(results.get(1)).isEqualTo(new ParseResult.Ok(item("A-2", "toys", 5, 250)));
        assertThat(results.get(2)).isEqualTo(new ParseResult.Failed(6, "expected 4 fields but found 1"));
        assertThat(results.get(3)).isInstanceOfSatisfying(ParseResult.Failed.class, f -> assertThat(f.lineNumber()).isEqualTo(7));
        assertThat(results.get(4)).isInstanceOfSatisfying(ParseResult.Failed.class, f -> assertThat(f.lineNumber()).isEqualTo(8));
        assertThat(results.get(5)).isInstanceOfSatisfying(ParseResult.Failed.class, f -> assertThat(f.lineNumber()).isEqualTo(9));
        assertThat(results.get(6)).isEqualTo(new ParseResult.Ok(item("A-5", "games", 0, 5999)));
        assertThat(results.get(7)).isEqualTo(new ParseResult.Failed(11, "expected 4 fields but found 5"));
    }

    @Test
    void r2_parseHandlesEmptyInput() {
        assertThat(InventoryReport.parse("")).isEmpty();
        assertThat(InventoryReport.parse(null)).isEmpty();
        assertThat(InventoryReport.parse("sku,category,qty,priceCents\n# only comments\n\n")).isEmpty();
    }

    // ------------------------------------------------------------------ r3 aggregation
    private static List<Item> sample() {
        return List.of(
                item("A-1", "books", 10, 1050),   // 10500
                item("A-2", "toys", 5, 250),      // 1250
                item("A-5", "games", 0, 5999),    // 0
                item("A-7", "books", 1, 9500),    // 9500
                item("A-8", "toys", 4, 250),      // 1000
                item("A-9", "toys", 1, 100));     // 100
    }

    @Test
    void r3_valueByCategoryIsSorted() {
        assertThat(InventoryReport.valueByCategory(sample())).containsExactly(
                Map.entry("books", 20_000L), Map.entry("games", 0L), Map.entry("toys", 2_350L));
        assertThat(InventoryReport.valueByCategory(List.of())).isEmpty();
    }

    @Test
    void r3_topNOrdersByValueThenSku() {
        assertThat(InventoryReport.topN(sample(), 3)).extracting(Item::sku).containsExactly("A-1", "A-7", "A-2");
        assertThat(InventoryReport.topN(sample(), 0)).isEmpty();
        assertThat(InventoryReport.topN(sample(), 100)).hasSize(6);
        List<Item> ties = List.of(item("b", "c", 1, 10), item("a", "c", 1, 10), item("c", "c", 2, 5));
        assertThat(InventoryReport.topN(ties, 3)).extracting(Item::sku).containsExactly("a", "b", "c");
        assertThatThrownBy(() -> InventoryReport.topN(sample(), -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_cheapestInStockIgnoresEmptyShelvesAndCase() {
        assertThat(InventoryReport.cheapestInStock(sample(), "TOYS")).map(Item::sku).contains("A-9");
        assertThat(InventoryReport.cheapestInStock(sample(), "books")).map(Item::sku).contains("A-1");
        assertThat(InventoryReport.cheapestInStock(sample(), "games")).as("only an out-of-stock item").isEmpty();
        assertThat(InventoryReport.cheapestInStock(sample(), "garden")).isEmpty();
        List<Item> tie = List.of(item("z", "c", 1, 5), item("m", "c", 1, 5));
        assertThat(InventoryReport.cheapestInStock(tie, "c")).map(Item::sku).contains("m");
    }

    // ------------------------------------------------------------------ r4 parallel total
    @Test
    void r4_parallelTotalMatchesSequentialSum() {
        List<Item> items = IntStream.range(0, 1_000).mapToObj(i -> item("sku-" + i, "c" + (i % 5), i, 3)).toList();
        long expected = items.stream().mapToLong(Item::valueCents).sum();
        assertThat(InventoryReport.parallelTotal(items, 7)).isEqualTo(expected);
        assertThat(InventoryReport.parallelTotal(items, 1)).isEqualTo(expected);
        assertThat(InventoryReport.parallelTotal(items, 5_000)).isEqualTo(expected);
        assertThat(InventoryReport.parallelTotal(List.of(), 3)).isZero();
    }

    @Test
    void r4_parallelTotalRejectsBadBatchSize() {
        assertThatThrownBy(() -> InventoryReport.parallelTotal(sample(), 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> InventoryReport.parallelTotal(sample(), -3)).isInstanceOf(IllegalArgumentException.class);
    }

    // ------------------------------------------------------------------ r5 formatting
    @ParameterizedTest(name = "{0} -> {1}")
    @CsvSource(delimiter = '|', value = {
            "0|$0.00", "5|$0.05", "99|$0.99", "100|$1.00", "1050|$10.50", "123456|$1,234.56", "123456789|$1,234,567.89",
            "-5|-$0.05", "-123456|-$1,234.56"
    })
    void r5_money(long cents, String expected) {
        assertThat(InventoryReport.money(cents)).isEqualTo(expected);
    }

    private static String row(String name, String money) {
        return name + " ".repeat(21 - name.length() - money.length()) + money;
    }

    @Test
    void r5_renderTable() {
        Map<String, Long> totals = new LinkedHashMap<>();
        totals.put("books", 1050L);
        totals.put("toys", 250L);
        assertThat(InventoryReport.render(totals)).isEqualTo(row("books", "$10.50") + "\n" + row("toys", "$2.50") + "\n" + row("TOTAL", "$13.00"));
        assertThat(InventoryReport.render(Map.of())).isEqualTo(row("TOTAL", "$0.00"));
    }

    @Test
    void r5_endToEnd() {
        List<Item> items = new ArrayList<>();
        for (ParseResult r : InventoryReport.parse(CSV)) {
            if (r instanceof ParseResult.Ok ok) {
                items.add(ok.item());
            }
        }
        assertThat(items).extracting(Item::sku).containsExactly("A-1", "A-2", "A-5");
        assertThat(InventoryReport.render(InventoryReport.valueByCategory(items)))
                .isEqualTo(row("books", "$105.00") + "\n" + row("games", "$0.00") + "\n" + row("toys", "$12.50") + "\n" + row("TOTAL", "$117.50"));
    }

    // ------------------------------------------------------------------ r6 LRU cache
    @Test
    void r6_evictsTheLeastRecentlyUsedEntry() {
        LruCache<String, Integer> cache = new LruCache<>(2);
        cache.put("a", 1);
        cache.put("b", 2);
        assertThat(cache.get("a")).isEqualTo(1);       // a is now most recently used
        cache.put("c", 3);                              // evicts b
        assertThat(cache.get("b")).isNull();
        assertThat(cache.keys()).containsExactly("a", "c");
        assertThat(cache.size()).isEqualTo(2);
    }

    @Test
    void r6_overwritingRefreshesAndKeepsSize() {
        LruCache<String, String> cache = new LruCache<>(3);
        cache.put("x", "1");
        cache.put("y", "2");
        cache.put("z", "3");
        cache.put("x", "one");                          // refresh x
        assertThat(cache.keys()).containsExactly("y", "z", "x");
        cache.put("w", "4");                            // evicts y
        assertThat(cache.keys()).containsExactly("z", "x", "w");
        assertThat(cache.get("x")).isEqualTo("one");
        assertThat(cache.get("missing")).isNull();
        assertThat(cache.keys()).containsExactly("z", "w", "x");
    }

    @Test
    void r6_keysReturnsASnapshot() {
        LruCache<Integer, Integer> cache = new LruCache<>(5);
        cache.put(1, 1);
        List<Integer> keys = cache.keys();
        keys.add(99);
        assertThat(cache.keys()).containsExactly(1);
        assertThat(cache.size()).isEqualTo(1);
    }

    @Test
    void r6_invalidCapacity() {
        assertThatThrownBy(() -> new LruCache<String, String>(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new LruCache<String, String>(-4)).isInstanceOf(IllegalArgumentException.class);
        LruCache<String, String> one = new LruCache<>(1);
        one.put("a", "1");
        one.put("b", "2");
        assertThat(one.keys()).containsExactly("b");
    }
}
