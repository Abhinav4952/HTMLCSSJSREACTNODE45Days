package com.javaprep.day23.task01;

import java.util.Locale;

/** Roman numeral conversion. */
public final class RomanNumerals {

    private static final int[] VALUES = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
    private static final String[] SYMBOLS = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};

    private RomanNumerals() {
    }

    public static String toRoman(int number) {
        // TODO(Day23-task01): IllegalArgumentException outside 1..3999; greedily subtract the largest VALUES entry and append its SYMBOLS entry
        throw new UnsupportedOperationException("TODO(Day23-task01): toRoman");
    }

    public static int fromRoman(String text) {
        // TODO(Day23-task01): null/blank -> IllegalArgumentException; upper-case (Locale.ROOT); parse greedily using SYMBOLS/VALUES; the leftover must be empty and toRoman(result) must equal the input (rejects IIII, VX, IC) otherwise IllegalArgumentException
        throw new UnsupportedOperationException("TODO(Day23-task01): fromRoman");
    }
}
