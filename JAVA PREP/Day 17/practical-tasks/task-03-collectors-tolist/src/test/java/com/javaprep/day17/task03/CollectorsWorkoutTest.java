package com.javaprep.day17.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class CollectorsWorkoutTest {

    @Test
    void r1_upperNames() {
        assertThat(CollectorsWorkout.upperNames(List.of("ann", "Bob"))).containsExactly("ANN", "BOB");
        assertThat(CollectorsWorkout.upperNames(List.of())).isEmpty();
    }

    @Test
    void r2_uniqueLengths() {
        assertThat(CollectorsWorkout.uniqueLengths(List.of("a", "bb", "cc", "d"))).containsExactlyInAnyOrder(1, 2);
    }

    @Test
    void r3_lengthByWordKeepsFirstAndOrder() {
        Map<String, Integer> m = CollectorsWorkout.lengthByWord(List.of("kiwi", "fig", "kiwi", "apple"));
        assertThat(m).containsOnlyKeys("kiwi", "fig", "apple");
        assertThat(new ArrayList<>(m.keySet())).containsExactly("kiwi", "fig", "apple");
        assertThat(m).containsEntry("kiwi", 4).containsEntry("fig", 3).containsEntry("apple", 5);
    }

    @Test
    void r4_csv() {
        assertThat(CollectorsWorkout.csv(List.of("a", "b", "c"))).isEqualTo("[a, b, c]");
        assertThat(CollectorsWorkout.csv(List.of("solo"))).isEqualTo("[solo]");
        assertThat(CollectorsWorkout.csv(List.of())).isEqualTo("[]");
    }

    @Test
    void r5_immutableSorted() {
        List<String> sorted = CollectorsWorkout.immutableSorted(new ArrayList<>(List.of("pear", "apple", "fig")));
        assertThat(sorted).containsExactly("apple", "fig", "pear");
        assertThatThrownBy(() -> sorted.add("zzz")).isInstanceOf(UnsupportedOperationException.class);
        assertThatThrownBy(() -> sorted.set(0, "x")).isInstanceOf(UnsupportedOperationException.class);
    }

    @Test
    void r6_toIdsByType() {
        Map<String, List<String>> grouped = CollectorsWorkout.toIdsByType(List.of("b:2", "a:1", "b:9", "a:7", "c:5"));
        assertThat(new ArrayList<>(grouped.keySet())).containsExactly("a", "b", "c");
        assertThat(grouped.get("a")).containsExactly("1", "7");
        assertThat(grouped.get("b")).containsExactly("2", "9");
        assertThat(CollectorsWorkout.toIdsByType(List.of())).isEmpty();
    }
}
