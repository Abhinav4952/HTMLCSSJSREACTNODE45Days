package com.javaprep.day23.task04;

import java.time.LocalDate;

/** Provided immutable customer record with its loyalty tier. */
public record Customer(String id, int points, LocalDate lastActivity, Tier tier) {

    /** Loyalty tiers and their earning multipliers. */
    public enum Tier {
        BRONZE(1), SILVER(2), GOLD(3);

        private final int multiplier;

        Tier(int multiplier) {
            this.multiplier = multiplier;
        }

        public int multiplier() {
            return multiplier;
        }
    }
}
