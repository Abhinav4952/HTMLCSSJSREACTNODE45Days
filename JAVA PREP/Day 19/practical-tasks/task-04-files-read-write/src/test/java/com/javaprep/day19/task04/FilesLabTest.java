package com.javaprep.day19.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

class FilesLabTest {

    @TempDir
    Path tmp;

    @Test
    void r1_writeCreatesParentsAndReplacesContent() throws Exception {
        Path file = tmp.resolve("nested").resolve("deeper").resolve("a.txt");
        FilesLab.writeLines(file, List.of("one", "two"));
        assertThat(Files.readAllLines(file)).containsExactly("one", "two");
        FilesLab.writeLines(file, List.of("only"));
        assertThat(Files.readAllLines(file)).containsExactly("only");
    }

    @Test
    void r2_readUsesUtf8() throws Exception {
        Path file = tmp.resolve("utf8.txt");
        Files.writeString(file, "héllo ✓\nwörld\n");
        assertThat(FilesLab.readLines(file)).containsExactly("héllo ✓", "wörld");
        Path empty = tmp.resolve("empty.txt");
        Files.createFile(empty);
        assertThat(FilesLab.readLines(empty)).isEmpty();
    }

    @Test
    void r2_missingFileBecomesUncheckedIoException() {
        Path missing = tmp.resolve("missing.txt");
        assertThatThrownBy(() -> FilesLab.readLines(missing))
                .isInstanceOf(UncheckedIOException.class)
                .hasCauseInstanceOf(NoSuchFileException.class);
    }

    @Test
    void r3_appendCreatesAndKeepsEarlierLines() {
        Path file = tmp.resolve("log.txt");
        FilesLab.appendLine(file, "first");
        FilesLab.appendLine(file, "second");
        assertThat(FilesLab.readLines(file)).containsExactly("first", "second");
    }

    @Test
    void r4_countLines() throws Exception {
        Path file = tmp.resolve("count.txt");
        Files.write(file, List.of("a", "b", "c"));
        assertThat(FilesLab.countLines(file)).isEqualTo(3);
        Path empty = tmp.resolve("e.txt");
        Files.createFile(empty);
        assertThat(FilesLab.countLines(empty)).isZero();
        assertThatThrownBy(() -> FilesLab.countLines(tmp.resolve("nope.txt"))).isInstanceOf(UncheckedIOException.class);
    }

    @Test
    void r5_listTextFilesIsSortedFlatAndFiltered() throws Exception {
        Files.writeString(tmp.resolve("b.txt"), "b");
        Files.writeString(tmp.resolve("a.txt"), "a");
        Files.writeString(tmp.resolve("c.md"), "c");
        Files.createDirectory(tmp.resolve("sub.txt"));
        Files.writeString(Files.createDirectory(tmp.resolve("inner")).resolve("z.txt"), "z");
        assertThat(FilesLab.listTextFiles(tmp)).extracting(p -> p.getFileName().toString()).containsExactly("a.txt", "b.txt");
        Path emptyDir = Files.createDirectory(tmp.resolve("empty-dir"));
        assertThat(FilesLab.listTextFiles(emptyDir)).isEmpty();
    }

    @Test
    void r6_copyReplacesExistingTarget() throws Exception {
        Path src = tmp.resolve("src.txt");
        Path dst = tmp.resolve("dst.txt");
        Files.writeString(src, "new");
        Files.writeString(dst, "old");
        FilesLab.copyReplacing(src, dst);
        assertThat(Files.readString(dst)).isEqualTo("new");
        assertThat(Files.exists(src)).isTrue();
        assertThatThrownBy(() -> FilesLab.copyReplacing(tmp.resolve("missing"), dst)).isInstanceOf(UncheckedIOException.class);
    }

    @Test
    void r7_deleteIfPresent() throws Exception {
        Path file = tmp.resolve("gone.txt");
        Files.writeString(file, "x");
        assertThat(FilesLab.deleteIfPresent(file)).isTrue();
        assertThat(Files.exists(file)).isFalse();
        assertThat(FilesLab.deleteIfPresent(file)).isFalse();
    }
}
