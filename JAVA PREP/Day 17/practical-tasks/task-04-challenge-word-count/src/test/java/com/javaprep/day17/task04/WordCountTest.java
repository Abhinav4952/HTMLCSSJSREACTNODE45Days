package com.javaprep.day17.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class WordCountTest {

    private static final String TEXT = "The cat and the hat.\nThe END! Cat's hat? the-end 42 42";

    @Test
    void r1_countWordsSplitsOnNonLettersAndLowercases() {
        var counts = WordCount.countWords(TEXT, Set.of());
        assertThat(counts).containsEntry("the", 4L)
                .containsEntry("cat", 2L)
                .containsEntry("hat", 2L)
                .containsEntry("end", 2L)
                .containsEntry("and", 1L)
                .containsEntry("s", 1L)
                .containsEntry("42", 2L);
    }

    @Test
    void r1_stopWordsAndEmptyText() {
        var counts = WordCount.countWords(TEXT, Set.of("the", "and"));
        assertThat(counts).doesNotContainKeys("the", "and").containsKey("cat");
        assertThat(WordCount.countWords(null, Set.of())).isEmpty();
        assertThat(WordCount.countWords("  \n ", Set.of())).isEmpty();
        assertThat(WordCount.countWords("...", Set.of())).isEmpty();
    }

    @Test
    void r2_topNOrdersByCountThenWord() {
        assertThat(WordCount.topN(TEXT, 3, Set.of())).containsExactly("the=4", "42=2", "cat=2");
        assertThat(WordCount.topN(TEXT, 2, Set.of("the"))).containsExactly("42=2", "cat=2");
    }

    @Test
    void r2_topNBoundaries() {
        assertThat(WordCount.topN(TEXT, 0, Set.of())).isEmpty();
        assertThat(WordCount.topN(TEXT, -4, Set.of())).isEmpty();
        assertThat(WordCount.topN("a b", 10, Set.of())).containsExactly("a=1", "b=1");
        assertThat(WordCount.topN(null, 3, Set.of())).isEmpty();
    }

    @Test
    void r3_lengthHistogramIsSortedAndCountsOccurrences() {
        var hist = WordCount.lengthHistogram("a bb cc ddd a");
        assertThat(List.copyOf(hist.keySet())).containsExactly(1, 2, 3);
        assertThat(hist.get(1)).isEqualTo(2L);
        assertThat(hist.get(2)).isEqualTo(2L);
        assertThat(hist.get(3)).isEqualTo(1L);
        assertThat(WordCount.lengthHistogram("")).isEmpty();
    }

    @Test
    void r4_hapax() {
        var once = WordCount.hapax("Red green red BLUE green yellow");
        assertThat(List.copyOf(once)).containsExactly("blue", "yellow");
        assertThat(WordCount.hapax("same same")).isEmpty();
        assertThat(WordCount.hapax(null)).isEmpty();
    }
}
