package com.javaprep.day23.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import org.junit.jupiter.params.provider.ValueSource;

@DisplayName("Slugs")
class SlugsTest {

    @ParameterizedTest(name = "\"{0}\" -> \"{1}\"")
    @CsvSource(delimiter = '|', value = {
            "Hello World|hello-world",
            "  Hello   World  |hello-world",
            "Java 21: Virtual Threads!|java-21-virtual-threads",
            "Crème Brûlée à la façon|creme-brulee-a-la-facon",
            "Ünïcödé Tëst|unicode-test",
            "---already--dashed---|already-dashed",
            "snake_case_and.dots|snake-case-and-dots",
            "ALL CAPS|all-caps",
            "a|a",
            "!!!|",
            "x   |x"
    })
    void r3_slugify(String input, String expected) {
        assertThat(Slugs.slugify(input)).isEqualTo(expected == null ? "" : expected);
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"   ", "\t\n"})
    void r3_blankOrEmptyBecomesEmptyExceptNull(String input) {
        if (input == null) {
            assertThatThrownBy(() -> Slugs.slugify(null)).isInstanceOf(IllegalArgumentException.class);
        } else {
            assertThat(Slugs.slugify(input)).isEmpty();
        }
    }

    @Test
    void r3_slugifyIsIdempotent() {
        String once = Slugs.slugify("  Déjà Vu -- Part 2!  ");
        assertThat(once).isEqualTo("deja-vu-part-2");
        assertThat(Slugs.slugify(once)).isEqualTo(once);
    }

    @ParameterizedTest
    @ValueSource(strings = {"a", "abc", "a-b", "hello-world-2", "123", "a1-b2-c3"})
    void r4_validSlugs(String slug) {
        assertThat(Slugs.isValidSlug(slug)).isTrue();
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "-a", "a-", "a--b", "A", "a b", "a_b", "é"})
    void r4_invalidSlugs(String slug) {
        assertThat(Slugs.isValidSlug(slug)).isFalse();
    }

    @Test
    void r4_nullIsNotAValidSlug() {
        assertThat(Slugs.isValidSlug(null)).isFalse();
    }

    @Test
    void r4_everySlugifiedValueIsValidOrEmpty() {
        for (String s : new String[] {"Hello, World!", "Ça va?", "2026-10-16", "Zażółć gęślą jaźń", "   "}) {
            String slug = Slugs.slugify(s);
            assertThat(slug.isEmpty() || Slugs.isValidSlug(slug)).as(s).isTrue();
        }
    }
}
