package com.javaprep.day17.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.Arrays;
import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class StreamFilterMapTest {

    @Test
    void r1_upperLongNames() {
        List<String> in = Arrays.asList(" ann ", null, "bo", "carl", "  ");
        assertThat(StreamFilterMap.upperLongNames(in, 3)).containsExactly("ANN", "CARL");
        assertThat(StreamFilterMap.upperLongNames(List.of(), 1)).isEmpty();
        assertThat(StreamFilterMap.upperLongNames(List.of("x"), 0)).containsExactly("X");
    }

    @Test
    void r2_squaresOfOdds() {
        assertThat(StreamFilterMap.squaresOfOdds(List.of(1, 2, 3, 4, 5))).containsExactly(1, 9, 25);
        assertThat(StreamFilterMap.squaresOfOdds(List.of(-3, -2, 0))).containsExactly(9);
        assertThat(StreamFilterMap.squaresOfOdds(List.of(2, 4))).isEmpty();
    }

    @Test
    void r3_distinctSortedLower() {
        List<String> in = Arrays.asList("Pear", " apple", "PEAR ", null, "  ", "Apple", "fig");
        assertThat(StreamFilterMap.distinctSortedLower(in)).containsExactly("apple", "fig", "pear");
        assertThat(StreamFilterMap.distinctSortedLower(List.of())).isEmpty();
    }

    @Test
    void r4_page() {
        List<Integer> nums = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        assertThat(StreamFilterMap.page(nums, 0, 4)).containsExactly(1, 2, 3, 4);
        assertThat(StreamFilterMap.page(nums, 1, 4)).containsExactly(5, 6, 7, 8);
        assertThat(StreamFilterMap.page(nums, 2, 4)).containsExactly(9, 10);
        assertThat(StreamFilterMap.page(nums, 3, 4)).isEmpty();
    }

    @Test
    void r4_pageValidatesArguments() {
        assertThatThrownBy(() -> StreamFilterMap.page(List.of(1), -1, 2)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> StreamFilterMap.page(List.of(1), 0, 0)).isInstanceOf(IllegalArgumentException.class);
        assertThat(StreamFilterMap.page(List.of(1, 2), Integer.MAX_VALUE, Integer.MAX_VALUE)).isEmpty();
    }

    @Test
    void r5_firstStartingWith() {
        List<String> names = Arrays.asList(null, "Bob", "Barbara", "Alice");
        assertThat(StreamFilterMap.firstStartingWith(names, "Ba")).contains("Barbara");
        assertThat(StreamFilterMap.firstStartingWith(names, "B")).contains("Bob");
        assertThat(StreamFilterMap.firstStartingWith(names, "Z")).isEmpty();
    }

    @Test
    @DisplayName("Laziness: each element flows through the whole pipeline; findFirst short-circuits")
    void r6_traceLaziness() {
        assertThat(StreamFilterMap.traceLaziness()).containsExactly("filter:a", "filter:bb", "map:bb");
    }
}
