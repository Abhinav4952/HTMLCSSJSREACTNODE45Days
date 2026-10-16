package com.javaprep.day19.task04;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.nio.file.StandardOpenOption;
import java.util.List;
import java.util.stream.Stream;

/** NIO.2 file helpers; IOExceptions are rethrown as UncheckedIOException. */
public final class FilesLab {

    private FilesLab() {
    }

    public static void writeLines(Path file, List<String> lines) {
        // TODO(Day19-task04): create parent directories if needed, then Files.write(file, lines, UTF_8) replacing existing content; wrap IOException in UncheckedIOException
        throw new UnsupportedOperationException("TODO(Day19-task04): writeLines");
    }

    public static List<String> readLines(Path file) {
        // TODO(Day19-task04): Files.readAllLines(file, UTF_8); wrap IOException (e.g. NoSuchFileException) in UncheckedIOException
        throw new UnsupportedOperationException("TODO(Day19-task04): readLines");
    }

    public static void appendLine(Path file, String line) {
        // TODO(Day19-task04): append line + System.lineSeparator() with CREATE and APPEND options in UTF-8; wrap IOException
        throw new UnsupportedOperationException("TODO(Day19-task04): appendLine");
    }

    public static long countLines(Path file) {
        // TODO(Day19-task04): count lines with Files.lines(file, UTF_8) in try-with-resources; wrap IOException
        throw new UnsupportedOperationException("TODO(Day19-task04): countLines");
    }

    public static List<Path> listTextFiles(Path dir) {
        // TODO(Day19-task04): regular files directly in dir whose name ends with .txt, sorted by file name; use try-with-resources around Files.list; wrap IOException
        throw new UnsupportedOperationException("TODO(Day19-task04): listTextFiles");
    }

    public static void copyReplacing(Path src, Path dst) {
        // TODO(Day19-task04): Files.copy(src, dst, REPLACE_EXISTING); wrap IOException
        throw new UnsupportedOperationException("TODO(Day19-task04): copyReplacing");
    }

    public static boolean deleteIfPresent(Path file) {
        // TODO(Day19-task04): Files.deleteIfExists(file) and return its result; wrap IOException
        throw new UnsupportedOperationException("TODO(Day19-task04): deleteIfPresent");
    }
}
