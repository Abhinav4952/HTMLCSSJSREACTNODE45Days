package com.javaprep.day02.task02;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class ArrayAliasTest {

    @Test
    @DisplayName("sameArray is identity, not content equality")
    void sameArrayIdentity() {
        int[] a = {1, 2, 3};
        int[] alias = a;
        int[] copy = {1, 2, 3};
        assertThat(ArrayAlias.sameArray(a, alias)).isTrue();
        assertThat(ArrayAlias.sameArray(a, copy)).isFalse();
        assertThat(ArrayAlias.sameArray(null, null)).isTrue();
        assertThat(ArrayAlias.sameArray(a, null)).isFalse();
    }

    @Test
    @DisplayName("mutateShared is visible through aliases")
    void mutationVisibleThroughAlias() {
        int[] a = {1, 2, 3};
        int[] alias = a;
        ArrayAlias.mutateShared(a, 1, 99);
        assertThat(alias).containsExactly(1, 99, 3);
    }

    @Test
    @DisplayName("invalid index -> IndexOutOfBoundsException, null array -> NullPointerException")
    void errors() {
        int[] a = {1, 2, 3};
        assertThatThrownBy(() -> ArrayAlias.mutateShared(a, 3, 0)).isInstanceOf(IndexOutOfBoundsException.class);
        assertThatThrownBy(() -> ArrayAlias.mutateShared(a, -1, 0)).isInstanceOf(IndexOutOfBoundsException.class);
        assertThatThrownBy(() -> ArrayAlias.mutateShared(null, 0, 0)).isInstanceOf(NullPointerException.class);
    }
}
