package com.javaprep.day24.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.ValueSource;

class MavenVersionTest {

    private static int cmp(String a, String b) {
        return Integer.signum(MavenVersion.parse(a).compareTo(MavenVersion.parse(b)));
    }

    // ------------------------------------------------------------------ r1 parsing
    @ParameterizedTest
    @ValueSource(strings = {"1", "1.0", "1.0.0", "2.10.3", "1.0-SNAPSHOT", "1.0-alpha", "1.0-alpha2", "1.0-beta-3", "2.0-RC1", "2.0-rc.2", "1.0-GA", "3.1.4-final", "1.0-milestone1", "1.0-cr1"})
    void r1_parsesValidVersions(String text) {
        assertThat(MavenVersion.parse(text)).hasToString(text);
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "abc", "1.", ".1", "1..2", "1.0-", "1.0-foo", "v1.0", "1.0-SNAPSHOT-2x", "1,0"})
    void r1_rejectsInvalidVersions(String text) {
        assertThatThrownBy(() -> MavenVersion.parse(text)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r1_nullIsRejected() {
        assertThatThrownBy(() -> MavenVersion.parse(null)).isInstanceOf(IllegalArgumentException.class);
    }

    // ------------------------------------------------------------------ r2 ordering
    @ParameterizedTest(name = "{0} < {1}")
    @CsvSource({
            "1.9,1.10", "1.2.3,1.2.4", "1.0,1.0.1", "1.99,2.0", "0.9,1",
            "1.0-alpha,1.0-beta", "1.0-beta,1.0-milestone1", "1.0-milestone1,1.0-rc1", "1.0-rc1,1.0-SNAPSHOT",
            "1.0-SNAPSHOT,1.0", "1.0-alpha,1.0", "1.0-rc1,1.0-rc2", "1.0-rc,1.0-rc1", "1.0-beta2,1.0-beta10",
            "1.0-rc1,1.0.1-alpha", "1.0-SNAPSHOT,1.0.1-SNAPSHOT"
    })
    void r2_isOrdered(String lower, String higher) {
        assertThat(cmp(lower, higher)).isEqualTo(-1);
        assertThat(cmp(higher, lower)).isEqualTo(1);
    }

    @ParameterizedTest(name = "{0} == {1}")
    @CsvSource({"1,1.0", "1.0,1.0.0", "1.0.0,1", "2.0-GA,2.0", "2.0-final,2.0", "1.0-rc1,1.0-cr1", "1.0-SNAPSHOT,1.0-snapshot"})
    void r2_equalVersionsCompareEqualAndShareHashCodes(String a, String b) {
        MavenVersion va = MavenVersion.parse(a);
        MavenVersion vb = MavenVersion.parse(b);
        assertThat(va.compareTo(vb)).isZero();
        assertThat(va).isEqualTo(vb);
        assertThat(va.hashCode()).isEqualTo(vb.hashCode());
    }

    @Test
    void r2_sortingARealisticList() {
        List<String> versions = new ArrayList<>(List.of("1.10", "1.9", "1.0-SNAPSHOT", "1.0", "1.0-rc1", "1.0-beta1", "1.0-alpha", "1.2", "1.10-SNAPSHOT", "1.1"));
        Collections.sort(versions, (a, b) -> MavenVersion.parse(a).compareTo(MavenVersion.parse(b)));
        assertThat(versions).containsExactly("1.0-alpha", "1.0-beta1", "1.0-rc1", "1.0-SNAPSHOT", "1.0", "1.1", "1.2", "1.9", "1.10-SNAPSHOT", "1.10");
    }

    // ------------------------------------------------------------------ r3 ranges
    private static boolean in(String range, String version) {
        return VersionRange.parse(range).contains(MavenVersion.parse(version));
    }

    @ParameterizedTest(name = "{0} contains {1} = {2}")
    @CsvSource({
            "'[1.0,2.0)',1.0,true", "'[1.0,2.0)',1.5,true", "'[1.0,2.0)',2.0,false", "'[1.0,2.0)',0.9,false", "'[1.0,2.0)',1.99,true",
            "'(1.0,2.0]',1.0,false", "'(1.0,2.0]',2.0,true", "'(1.0,2.0]',2.1,false",
            "'[1.0,2.0]',1.0,true", "'[1.0,2.0]',2.0,true", "'(1.0,2.0)',1.0,false", "'(1.0,2.0)',2.0,false",
            "'[1.5,)',1.5,true", "'[1.5,)',99.0,true", "'[1.5,)',1.4,false", "'(,1.5]',0.1,true", "'(,1.5]',1.5,true", "'(,1.5]',1.6,false",
            "'(,1.5)',1.5,false", "'[1.5]',1.5,true", "'[1.5]',1.5.0,true", "'[1.5]',1.6,false", "'[1.10,2.0)',1.9,false", "'[1.9,2.0)',1.10,true"
    })
    void r3_contains(String range, String version, boolean expected) {
        assertThat(in(range, version)).isEqualTo(expected);
    }

    @ParameterizedTest
    @ValueSource(strings = {"1.0", "", "[]", "[,]", "(1.0)", "[2.0,1.0]", "[1.0,2.0", "1.0,2.0]", "[1.0,2.0,3.0]", "[x,y]"})
    void r3_rejectsMalformedRanges(String spec) {
        assertThatThrownBy(() -> VersionRange.parse(spec)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_nullRangeIsRejected() {
        assertThatThrownBy(() -> VersionRange.parse(null)).isInstanceOf(IllegalArgumentException.class);
    }

    // ------------------------------------------------------------------ r4 mediation
    @Test
    void r4_nearestWins() {
        var result = DependencyMediation.resolve(List.of(
                new DependencyMediation.Declaration("commons-codec:commons-codec", "1.16", 3),
                new DependencyMediation.Declaration("commons-codec:commons-codec", "1.10", 2),
                new DependencyMediation.Declaration("org.slf4j:slf4j-api", "2.0.16", 1)));
        assertThat(result).containsExactly(
                Map.entry("commons-codec:commons-codec", "1.10"),
                Map.entry("org.slf4j:slf4j-api", "2.0.16"));
    }

    @Test
    void r4_firstDeclaredWinsOnTies() {
        var result = DependencyMediation.resolve(List.of(
                new DependencyMediation.Declaration("g:a", "1.0", 2),
                new DependencyMediation.Declaration("g:b", "5.0", 1),
                new DependencyMediation.Declaration("g:a", "2.0", 2),
                new DependencyMediation.Declaration("g:a", "3.0", 4)));
        assertThat(result).containsExactly(Map.entry("g:a", "1.0"), Map.entry("g:b", "5.0"));
    }

    @Test
    void r4_directDeclarationBeatsEverything() {
        var result = DependencyMediation.resolve(List.of(
                new DependencyMediation.Declaration("g:a", "9.9", 2),
                new DependencyMediation.Declaration("g:a", "1.0", 0)));
        assertThat(result.get("g:a")).isEqualTo("1.0");
        assertThat(DependencyMediation.resolve(List.of())).isEmpty();
    }

    // ------------------------------------------------------------------ r5 helpers
    @Test
    void r5_highestUsesVersionOrderingNotTextOrdering() {
        assertThat(DependencyMediation.highest(List.of("1.9", "1.10", "1.2"))).isEqualTo("1.10");
        assertThat(DependencyMediation.highest(List.of("2.0-SNAPSHOT", "2.0-rc1", "1.9"))).isEqualTo("2.0-SNAPSHOT");
        assertThat(DependencyMediation.highest(List.of("2.0", "2.0-SNAPSHOT"))).isEqualTo("2.0");
        assertThat(DependencyMediation.highest(List.of("7"))).isEqualTo("7");
        assertThatThrownBy(() -> DependencyMediation.highest(List.of())).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r5_satisfyingFiltersAndSorts() {
        List<String> available = List.of("2.0", "1.10", "1.2", "1.9", "1.0-SNAPSHOT", "0.9", "1.0", "3.0");
        assertThat(DependencyMediation.satisfying(VersionRange.parse("[1.0,2.0)"), available))
                .containsExactly("1.0", "1.2", "1.9", "1.10");
        assertThat(DependencyMediation.satisfying(VersionRange.parse("(,1.0)"), available))
                .containsExactly("0.9", "1.0-SNAPSHOT");
        assertThat(DependencyMediation.satisfying(VersionRange.parse("[5.0,)"), available)).isEmpty();
        assertThat(Set.copyOf(DependencyMediation.satisfying(VersionRange.parse("[1.0]"), available))).containsExactly("1.0");
    }
}
