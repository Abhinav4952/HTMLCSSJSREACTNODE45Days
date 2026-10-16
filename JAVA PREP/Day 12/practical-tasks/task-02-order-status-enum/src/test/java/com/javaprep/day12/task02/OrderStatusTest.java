package com.javaprep.day12.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.EnumMap;
import java.util.EnumSet;
import java.util.Map;
import java.util.Set;

import static com.javaprep.day12.task02.OrderStatus.*;

class OrderStatusTest {

    private static final Map<OrderStatus, Set<OrderStatus>> ALLOWED = new EnumMap<>(OrderStatus.class);

    static {
        ALLOWED.put(NEW, EnumSet.of(PAID, CANCELLED));
        ALLOWED.put(PAID, EnumSet.of(SHIPPED, CANCELLED));
        ALLOWED.put(SHIPPED, EnumSet.of(DELIVERED));
        ALLOWED.put(DELIVERED, EnumSet.noneOf(OrderStatus.class));
        ALLOWED.put(CANCELLED, EnumSet.noneOf(OrderStatus.class));
    }

    @Test
    @DisplayName("happy-path transitions")
    void happyPath() {
        assertThat(NEW.canTransitionTo(PAID)).isTrue();
        assertThat(PAID.canTransitionTo(SHIPPED)).isTrue();
        assertThat(SHIPPED.canTransitionTo(DELIVERED)).isTrue();
        assertThat(NEW.canTransitionTo(CANCELLED)).isTrue();
        assertThat(PAID.canTransitionTo(CANCELLED)).isTrue();
    }

    @Test
    @DisplayName("every one of the 25 (from,to) pairs matches the transition table")
    void fullMatrix() {
        for (OrderStatus from : OrderStatus.values()) {
            for (OrderStatus to : OrderStatus.values()) {
                assertThat(from.canTransitionTo(to))
                        .as("%s -> %s", from, to)
                        .isEqualTo(ALLOWED.get(from).contains(to));
            }
        }
    }

    @Test
    @DisplayName("terminal states and shipped->cancelled are blocked")
    void blocked() {
        assertThat(SHIPPED.canTransitionTo(CANCELLED)).isFalse();
        assertThat(DELIVERED.canTransitionTo(NEW)).isFalse();
        assertThat(CANCELLED.canTransitionTo(PAID)).isFalse();
    }

    @Test
    @DisplayName("null target -> NullPointerException")
    void nullTarget() {
        assertThatThrownBy(() -> NEW.canTransitionTo(null)).isInstanceOf(NullPointerException.class);
    }
}
