package com.javaprep.day14.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.TreeSet;
import org.junit.jupiter.api.Test;

class ProductTest {

    @Test
    void r1_constructorStoresValues() {
        Product p = new Product("A-1", "Widget", 250);
        assertThat(p.sku()).isEqualTo("A-1");
        assertThat(p.name()).isEqualTo("Widget");
        assertThat(p.priceCents()).isEqualTo(250);
        assertThat(new Product("Z", "Free", 0).priceCents()).isZero();
    }

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new Product(null, "n", 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("   ", "n", 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("s", null, 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("s", " ", 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new Product("s", "n", -1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_compareToOrdersBySku() {
        Product a = new Product("A-1", "x", 1);
        Product b = new Product("B-1", "y", 1);
        assertThat(a.compareTo(b)).isNegative();
        assertThat(b.compareTo(a)).isPositive();
        assertThat(a.compareTo(new Product("A-1", "other", 99))).isZero();
    }

    @Test
    void r3_equalsAndHashCodeUseSkuOnly() {
        Product a = new Product("A-1", "x", 1);
        Product same = new Product("A-1", "different", 500);
        assertThat(a).isEqualTo(same).hasSameHashCodeAs(same);
        assertThat(a).isNotEqualTo(new Product("A-2", "x", 1));
        assertThat(a).isNotEqualTo("A-1");
        assertThat(a.equals(null)).isFalse();
    }

    @Test
    void r3_consistentWithEqualsForAllPairs() {
        List<Product> ps = List.of(new Product("a", "1", 1), new Product("b", "2", 2), new Product("a", "3", 3));
        for (Product x : ps) {
            for (Product y : ps) {
                assertThat(x.compareTo(y) == 0).isEqualTo(x.equals(y));
                assertThat(Integer.signum(x.compareTo(y))).isEqualTo(-Integer.signum(y.compareTo(x)));
            }
        }
    }

    @Test
    void r5_sortingAndTreeSet() {
        List<Product> list = new ArrayList<>(List.of(
                new Product("C", "c", 3), new Product("A", "a", 1), new Product("B", "b", 2)));
        Collections.sort(list);
        assertThat(list).extracting(Product::sku).containsExactly("A", "B", "C");
        assertThat(Collections.max(list).sku()).isEqualTo("C");

        TreeSet<Product> set = new TreeSet<>(list);
        set.add(new Product("A", "duplicate sku", 100));
        assertThat(set).hasSize(3);
        assertThat(set.first().name()).isEqualTo("a");
    }
}
