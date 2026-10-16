package com.javaprep.day50.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;

class TextStatsTest {

    @Test
    void topWordsCountsCaseInsensitivelyAndBreaksTiesAlphabetically() {
        String text = "The cat and the hat. The CAT sat; and sat!";
        assertThat(TextStats.topWords(text, 3)).containsExactly("the", "and", "cat");
    }

    @Test
    void topWordsEdgeCases() {
        assertThat(TextStats.topWords("", 5)).isEmpty();
        assertThat(TextStats.topWords("b a", 10)).containsExactly("a", "b");
        assertThatThrownBy(() -> TextStats.topWords("x", 0)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void groupsAnagramsInStableOrder() {
        assertThat(TextStats.groupAnagrams(List.of("listen", "google", "silent", "gogole", "cat")))
                .containsExactly(List.of("listen", "silent"), List.of("google", "gogole"), List.of("cat"));
    }

    @Test
    void firstNonRepeatedCharacter() {
        assertThat(TextStats.firstNonRepeated("swiss")).contains('w');
        assertThat(TextStats.firstNonRepeated("aabb")).isEmpty();
        assertThat(TextStats.firstNonRepeated("")).isEmpty();
        assertThat(TextStats.firstNonRepeated("aAb")).contains('a');
    }

    @Test
    void balancedBrackets() {
        assertThat(TextStats.isBalanced("{[()]}")).isTrue();
        assertThat(TextStats.isBalanced("a(b)c[d]{e}")).isTrue();
        assertThat(TextStats.isBalanced("")).isTrue();
        assertThat(TextStats.isBalanced(null)).isTrue();
        assertThat(TextStats.isBalanced("(]")).isFalse();
        assertThat(TextStats.isBalanced("((")).isFalse();
        assertThat(TextStats.isBalanced("())")).isFalse();
    }
}
