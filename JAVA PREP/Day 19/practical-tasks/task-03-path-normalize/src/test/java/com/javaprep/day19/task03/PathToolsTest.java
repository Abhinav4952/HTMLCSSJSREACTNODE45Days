package com.javaprep.day19.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.nio.file.Path;
import org.junit.jupiter.api.Test;

class PathToolsTest {

    @Test
    void r1_normalized() {
        assertThat(PathTools.normalized("a/./b/../c/file.txt")).isEqualTo(Path.of("a", "c", "file.txt"));
        assertThat(PathTools.normalized("../x")).isEqualTo(Path.of("..", "x"));
    }

    @Test
    void r2_segments() {
        assertThat(PathTools.segments(Path.of("a", "b", "c.txt"))).containsExactly("a", "b", "c.txt");
        assertThat(PathTools.segments(Path.of(""))).isEmpty();
        assertThat(PathTools.segments(Path.of("single"))).containsExactly("single");
    }

    @Test
    void r3_extension() {
        assertThat(PathTools.extension(Path.of("dir", "report.final.pdf"))).isEqualTo("pdf");
        assertThat(PathTools.extension(Path.of("README"))).isEmpty();
        assertThat(PathTools.extension(Path.of(".bashrc"))).isEmpty();
        assertThat(PathTools.extension(Path.of("odd."))).isEmpty();
        assertThat(PathTools.extension(Path.of("a.tar.gz"))).isEqualTo("gz");
    }

    @Test
    void r4_changeExtension() {
        assertThat(PathTools.changeExtension(Path.of("a", "b", "report.txt"), "md")).isEqualTo(Path.of("a", "b", "report.md"));
        assertThat(PathTools.changeExtension(Path.of("notes"), "txt")).isEqualTo(Path.of("notes.txt"));
        assertThat(PathTools.changeExtension(Path.of("x", "archive.tar.gz"), "zip")).isEqualTo(Path.of("x", "archive.tar.zip"));
        assertThat(PathTools.changeExtension(Path.of("odd."), "txt")).isEqualTo(Path.of("odd.txt"));
    }

    @Test
    void r5_relativeTo() {
        Path base = Path.of("srv", "data");
        Path target = Path.of("srv", "data", "reports", "q1.txt");
        assertThat(PathTools.relativeTo(base, target)).isEqualTo(Path.of("reports", "q1.txt"));
        assertThat(PathTools.relativeTo(target, base)).isEqualTo(Path.of("..", ".."));
    }

    @Test
    void r6_resolveSafeAllowsInsidePaths() {
        Path base = Path.of("srv", "data");
        Path expectedRoot = base.toAbsolutePath().normalize();
        assertThat(PathTools.resolveSafe(base, "reports/q1.txt")).isEqualTo(expectedRoot.resolve("reports").resolve("q1.txt"));
        assertThat(PathTools.resolveSafe(base, "a/../b.txt")).isEqualTo(expectedRoot.resolve("b.txt"));
        assertThat(PathTools.resolveSafe(base, ".")).isEqualTo(expectedRoot);
    }

    @Test
    void r6_resolveSafeRejectsEscapes() {
        Path base = Path.of("srv", "data");
        assertThatThrownBy(() -> PathTools.resolveSafe(base, "../secret.txt")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> PathTools.resolveSafe(base, "a/../../secret.txt")).isInstanceOf(IllegalArgumentException.class);
        Path absolute = Path.of("srv").toAbsolutePath().getRoot().resolve("etc").resolve("passwd");
        assertThatThrownBy(() -> PathTools.resolveSafe(base, absolute.toString())).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r6_siblingDirectoryWithSharedPrefixIsRejected() {
        Path base = Path.of("srv", "data");
        assertThatThrownBy(() -> PathTools.resolveSafe(base, "../data-private/x.txt")).isInstanceOf(IllegalArgumentException.class);
    }
}
