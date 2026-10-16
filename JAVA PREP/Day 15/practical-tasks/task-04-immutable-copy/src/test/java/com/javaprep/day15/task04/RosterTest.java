package com.javaprep.day15.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class RosterTest {

    private static Roster sample() {
        return new Roster(new ArrayList<>(List.of("ann", "bob")), new HashMap<>(Map.of("ann", 10, "bob", 20)));
    }

    @Test
    void r1_constructorCopiesAndRejectsNulls() {
        Roster roster = sample();
        assertThat(roster.names()).containsExactly("ann", "bob");
        assertThat(roster.scores()).containsOnlyKeys("ann", "bob").containsEntry("bob", 20);
        assertThatThrownBy(() -> new Roster(null, Map.of())).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> new Roster(Arrays.asList("a", null), Map.of())).isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> new Roster(List.of(), null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r2_callerChangesDoNotLeakIn() {
        List<String> names = new ArrayList<>(List.of("ann"));
        Map<String, Integer> scores = new HashMap<>(Map.of("ann", 1));
        Roster roster = new Roster(names, scores);
        names.add("mallory");
        scores.put("mallory", 99);
        assertThat(roster.names()).containsExactly("ann");
        assertThat(roster.scores()).containsOnlyKeys("ann");
    }

    @Test
    void r3_exposedCollectionsAreImmutable() {
        Roster roster = sample();
        List<String> names = roster.names();
        Map<String, Integer> scores = roster.scores();
        assertThatThrownBy(() -> names.add("x")).isInstanceOf(UnsupportedOperationException.class);
        assertThatThrownBy(() -> names.remove(0)).isInstanceOf(UnsupportedOperationException.class);
        assertThatThrownBy(() -> scores.put("x", 1)).isInstanceOf(UnsupportedOperationException.class);
    }

    @Test
    void r4_withNameReturnsNewInstance() {
        Roster original = sample();
        Roster bigger = original.withName("cy");
        assertThat(bigger).isNotSameAs(original);
        assertThat(bigger.names()).containsExactly("ann", "bob", "cy");
        assertThat(bigger.scores()).isEqualTo(original.scores());
        assertThat(original.names()).containsExactly("ann", "bob");
    }

    @Test
    void r5_safeCopyIsAnImmutableSnapshot() {
        List<Integer> source = new ArrayList<>(List.of(1, 2));
        List<Number> copy = Roster.<Number>safeCopy(source);
        source.add(3);
        assertThat(copy).containsExactly(1, 2);
        assertThatThrownBy(() -> copy.add(4)).isInstanceOf(UnsupportedOperationException.class);
    }

    @Test
    void r6_viewVersusCopyExperiments() {
        List<String> base = new ArrayList<>(List.of("a", "b"));
        assertThat(Roster.viewReflectsChanges(base)).isTrue();
        assertThat(Roster.copyIgnoresChanges(base)).isTrue();
        assertThat(base).containsExactly("a", "b");
    }
}
