package com.javaprep.day23.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.stream.Stream;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

@DisplayName("Roman numerals")
class RomanNumeralsTest {

    @ParameterizedTest(name = "{0} -> {1}")
    @CsvSource({"1,I", "2,II", "3,III", "4,IV", "5,V", "9,IX", "10,X", "14,XIV", "40,XL", "49,XLIX", "90,XC",
            "400,CD", "444,CDXLIV", "900,CM", "1994,MCMXCIV", "2024,MMXXIV", "3888,MMMDCCCLXXXVIII", "3999,MMMCMXCIX"})
    void r1_toRoman(int number, String expected) {
        assertEquals(expected, RomanNumerals.toRoman(number));
    }

    @ParameterizedTest
    @ValueSource(ints = {0, -1, -2024, 4000, Integer.MAX_VALUE, Integer.MIN_VALUE})
    void r1_toRomanRejectsOutOfRange(int number) {
        assertThatThrownBy(() -> RomanNumerals.toRoman(number)).isInstanceOf(IllegalArgumentException.class);
    }

    @ParameterizedTest(name = "{0} -> {1}")
    @CsvSource({"I,1", "IV,4", "ix,9", "xiv,14", "MCMXCIV,1994", "MMMCMXCIX,3999", "  XL  ,40"})
    void r2_fromRoman(String text, int expected) {
        assertEquals(expected, RomanNumerals.fromRoman(text));
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "IIII", "VX", "IC", "IIX", "MMMM", "ABC", "XXXX", "VV", "I I", "IXI"})
    void r2_fromRomanRejectsInvalid(String text) {
        assertThatThrownBy(() -> RomanNumerals.fromRoman(text)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_fromRomanRejectsNull() {
        assertThatThrownBy(() -> RomanNumerals.fromRoman(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    @DisplayName("round trip for every supported number")
    void r2_roundTrip() {
        for (int n = 1; n <= 3999; n++) {
            int expected = n;
            String roman = RomanNumerals.toRoman(n);
            int back = RomanNumerals.fromRoman(roman);
            assertAll("n=" + n, () -> assertThat(back).isEqualTo(expected), () -> assertThat(roman).matches("[MDCLXVI]+"));
        }
    }

    static Stream<Arguments> uniqueness() {
        return Stream.of(Arguments.of(1, 2), Arguments.of(4, 6), Arguments.of(1999, 2000), Arguments.of(3998, 3999));
    }

    @ParameterizedTest
    @MethodSource("uniqueness")
    void r2_differentNumbersGiveDifferentNumerals(int a, int b) {
        assertThat(RomanNumerals.toRoman(a)).isNotEqualTo(RomanNumerals.toRoman(b));
    }
}
