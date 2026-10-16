package com.javaprep.day13.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import org.junit.jupiter.api.Test;

class ArrayStackTest {

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new ArrayStack<String>(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new ArrayStack<String>(-3)).isInstanceOf(IllegalArgumentException.class);
        assertThat(new ArrayStack<String>().isEmpty()).isTrue();
    }

    @Test
    void r2_lifoOrder() {
        ArrayStack<String> stack = new ArrayStack<>();
        stack.push("a");
        stack.push("b");
        assertThat(stack.size()).isEqualTo(2);
        assertThat(stack.peek()).isEqualTo("b");
        assertThat(stack.pop()).isEqualTo("b");
        assertThat(stack.pop()).isEqualTo("a");
        assertThat(stack.isEmpty()).isTrue();
    }

    @Test
    void r2_emptyStackThrows() {
        ArrayStack<Integer> stack = new ArrayStack<>();
        assertThatThrownBy(stack::pop).isInstanceOf(java.util.NoSuchElementException.class);
        assertThatThrownBy(stack::peek).isInstanceOf(java.util.NoSuchElementException.class);
    }

    @Test
    void r3_growsBeyondInitialCapacity() {
        ArrayStack<Integer> stack = new ArrayStack<>(1);
        for (int i = 0; i < 1_000; i++) {
            stack.push(i);
        }
        assertThat(stack.size()).isEqualTo(1_000);
        for (int i = 999; i >= 0; i--) {
            assertThat(stack.pop()).isEqualTo(i);
        }
    }

    @Test
    void r4_pushAllAcceptsSubtypeSource() {
        ArrayStack<Number> stack = new ArrayStack<>();
        List<Integer> source = List.of(1, 2, 3);
        stack.pushAll(source);
        assertThat(stack.pop()).isEqualTo(3);
        assertThat(stack.size()).isEqualTo(2);
    }

    @Test
    void r5_popAllIntoSupertypeSink() {
        ArrayStack<Integer> stack = new ArrayStack<>();
        stack.pushAll(List.of(1, 2, 3));
        List<Object> sink = new ArrayList<>();
        int moved = stack.popAll(sink);
        assertThat(moved).isEqualTo(3);
        assertThat(sink).containsExactly(3, 2, 1);
        assertThat(stack.isEmpty()).isTrue();
        assertThat(stack.popAll(sink)).isZero();
    }

    @Test
    void r6_iteratorWalksTopToBottomWithoutMutating() {
        ArrayStack<String> stack = new ArrayStack<>();
        stack.push("x");
        stack.push("y");
        stack.push("z");
        List<String> seen = new ArrayList<>();
        for (String s : stack) {
            seen.add(s);
        }
        assertThat(seen).containsExactly("z", "y", "x");
        assertThat(stack.size()).isEqualTo(3);
    }

    @Test
    void r6_iteratorEdgeCases() {
        ArrayStack<String> stack = new ArrayStack<>();
        Iterator<String> empty = stack.iterator();
        assertThat(empty.hasNext()).isFalse();
        assertThatThrownBy(empty::next).isInstanceOf(java.util.NoSuchElementException.class);
        stack.push("only");
        Iterator<String> it = stack.iterator();
        assertThat(it.next()).isEqualTo("only");
        assertThatThrownBy(it::next).isInstanceOf(java.util.NoSuchElementException.class);
    }
}
