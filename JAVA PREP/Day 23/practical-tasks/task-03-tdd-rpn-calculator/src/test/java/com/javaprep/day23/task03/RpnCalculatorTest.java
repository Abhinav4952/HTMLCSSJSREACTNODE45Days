package com.javaprep.day23.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.NoSuchElementException;
import java.util.stream.Stream;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;

@DisplayName("RPN calculator, built test-first")
class RpnCalculatorTest {

    @Nested
    @DisplayName("BoundedStack")
    class StackBehaviour {
        private BoundedStack<String> stack;

        @BeforeEach
        void create() {
            stack = new BoundedStack<>(2);
        }

        @Test
        void r1_startsEmpty() {
            assertThat(stack.isEmpty()).isTrue();
            assertThat(stack.size()).isZero();
            assertThat(stack.capacity()).isEqualTo(2);
        }

        @Test
        void r1_isLastInFirstOut() {
            stack.push("a");
            stack.push("b");
            assertThat(stack.peek()).isEqualTo("b");
            assertThat(stack.size()).isEqualTo(2);
            assertThat(stack.pop()).isEqualTo("b");
            assertThat(stack.pop()).isEqualTo("a");
            assertThat(stack.isEmpty()).isTrue();
        }

        @Test
        void r1_rejectsPushWhenFull() {
            stack.push("a");
            stack.push("b");
            assertThatThrownBy(() -> stack.push("c")).isInstanceOf(IllegalStateException.class).hasMessageContaining("stack full");
            assertThat(stack.size()).isEqualTo(2);
        }

        @Test
        void r1_popAndPeekOnEmptyFail() {
            assertThatThrownBy(stack::pop).isInstanceOf(NoSuchElementException.class);
            assertThatThrownBy(stack::peek).isInstanceOf(NoSuchElementException.class);
        }

        @Test
        void r1_slotsAreReusableAfterPop() {
            stack.push("a");
            stack.push("b");
            stack.pop();
            stack.push("c");
            assertThat(stack.pop()).isEqualTo("c");
            assertThat(stack.pop()).isEqualTo("a");
        }

        @ParameterizedTest
        @ValueSource(ints = {0, -1})
        void r1_capacityMustBePositive(int capacity) {
            assertThatThrownBy(() -> new BoundedStack<String>(capacity)).isInstanceOf(IllegalArgumentException.class);
        }
    }

    @Nested
    @DisplayName("evaluate")
    class Arithmetic {
        private final RpnCalculator calculator = new RpnCalculator(16);

        @ParameterizedTest(name = "{0} = {1}")
        @CsvSource(delimiter = '|', value = {
                "42|42", "-7|-7", "2 3 +|5", "10 4 -|6", "6 7 *|42", "20 4 /|5", "7 2 /|3", "-7 2 /|-3",
                "3 4 + 2 *|14", "5 1 2 + 4 * + 3 -|14", "  2   3   +  |5", "2 3 4 * +|14", "100 10 / 5 /|2",
                "0 5 -|-5", "1 2 3 4 5 + + + +|15"
        })
        void r2_evaluates(String expression, long expected) {
            assertThat(calculator.evaluate(expression)).isEqualTo(expected);
        }

        @Test
        void r2_isReusableBetweenEvaluations() {
            assertThat(calculator.evaluate("1 1 +")).isEqualTo(2);
            assertThat(calculator.evaluate("2 2 *")).isEqualTo(4);
        }

        @Test
        void r2_detectsOverflow() {
            assertThatThrownBy(() -> calculator.evaluate("9223372036854775807 2 *")).isInstanceOf(ArithmeticException.class);
            assertThatThrownBy(() -> calculator.evaluate("9223372036854775807 1 +")).isInstanceOf(ArithmeticException.class);
        }
    }

    @Nested
    @DisplayName("errors")
    class Errors {
        private final RpnCalculator calculator = new RpnCalculator(3);

        @ParameterizedTest
        @ValueSource(strings = {"", "   ", "\t"})
        void r3_blankExpression(String expression) {
            assertThatThrownBy(() -> calculator.evaluate(expression)).isInstanceOf(IllegalArgumentException.class).hasMessage("empty expression");
        }

        @Test
        void r3_nullExpression() {
            assertThatThrownBy(() -> calculator.evaluate(null)).isInstanceOf(IllegalArgumentException.class).hasMessage("empty expression");
        }

        static Stream<Arguments> badInputs() {
            return Stream.of(
                    Arguments.of("1 +", IllegalArgumentException.class, "not enough operands"),
                    Arguments.of("+", IllegalArgumentException.class, "not enough operands"),
                    Arguments.of("1 2", IllegalArgumentException.class, "too many operands"),
                    Arguments.of("1 2 3 +", IllegalArgumentException.class, "too many operands"),
                    Arguments.of("1 x +", IllegalArgumentException.class, "unknown token: x"),
                    Arguments.of("2 3 ^", IllegalArgumentException.class, "unknown token: ^"),
                    Arguments.of("1 0 /", ArithmeticException.class, "division by zero"),
                    Arguments.of("1 2 3 4", IllegalStateException.class, "stack full"));
        }

        @ParameterizedTest
        @MethodSource("badInputs")
        void r3_reportsTheProblem(String expression, Class<? extends Throwable> type, String message) {
            assertThatThrownBy(() -> calculator.evaluate(expression)).isInstanceOf(type).hasMessageContaining(message);
        }
    }
}
