package com.javaprep.day16.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Map;
import java.util.function.Supplier;
import org.junit.jupiter.api.Test;

class MethodRefMapTest {

    @Test
    void r1_parser() {
        assertThat(MethodRefMap.parser().apply("42")).isEqualTo(42);
        assertThat(MethodRefMap.parser().apply("-7")).isEqualTo(-7);
        assertThatThrownBy(() -> MethodRefMap.parser().apply("x")).isInstanceOf(NumberFormatException.class);
    }

    @Test
    void r2_upper() {
        assertThat(MethodRefMap.upper().apply("abc")).isEqualTo("ABC");
        assertThat(MethodRefMap.upper().apply("")).isEmpty();
    }

    @Test
    void r3_prefixerIsBound() {
        assertThat(MethodRefMap.prefixer("id-").apply("9")).isEqualTo("id-9");
        assertThat(MethodRefMap.prefixer("").apply("z")).isEqualTo("z");
    }

    @Test
    void r3_nullPrefixFailsImmediately() {
        assertThatThrownBy(() -> MethodRefMap.prefixer(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r4_listFactoryReturnsFreshMutableLists() {
        Supplier<List<String>> factory = MethodRefMap.listFactory();
        List<String> first = factory.get();
        List<String> second = factory.get();
        first.add("x");
        assertThat(first).containsExactly("x");
        assertThat(second).isEmpty();
        assertThat(first).isNotSameAs(second);
    }

    @Test
    void r5_personFactory() {
        Person p = MethodRefMap.personFactory().apply("Ada");
        assertThat(p).isEqualTo(new Person("Ada"));
        assertThat(p.name()).isEqualTo("Ada");
    }

    @Test
    void r6_indexByKeepsOrder() {
        List<Person> people = List.of(new Person("ann"), new Person("bob"), new Person("cy"));
        Map<Integer, String> byLength = MethodRefMap.indexBy(List.of("a", "bb", "ccc"), String::length)
                .entrySet().stream().collect(java.util.stream.Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
        assertThat(byLength).containsEntry(2, "bb");
        Map<String, Person> byName = MethodRefMap.indexBy(people, Person::name);
        assertThat(byName.keySet()).containsExactly("ann", "bob", "cy");
        assertThat(byName.get("bob")).isEqualTo(new Person("bob"));
        assertThat(MethodRefMap.indexBy(List.<Person>of(), Person::name)).isEmpty();
    }

    @Test
    void r6_indexByRejectsDuplicates() {
        assertThatThrownBy(() -> MethodRefMap.indexBy(List.of("aa", "bb"), String::length))
                .isInstanceOf(IllegalArgumentException.class);
    }
}
