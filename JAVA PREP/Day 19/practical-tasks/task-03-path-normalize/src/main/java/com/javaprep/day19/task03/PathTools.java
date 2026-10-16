package com.javaprep.day19.task03;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

/** Pure Path logic; nothing here touches the file system. */
public final class PathTools {

    private PathTools() {
    }

    public static Path normalized(String text) {
        // TODO(Day19-task03): Path.of(text).normalize()
        throw new UnsupportedOperationException("TODO(Day19-task03): normalized");
    }

    public static List<String> segments(Path path) {
        // TODO(Day19-task03): the name elements of the path as strings, root excluded; empty path gives an empty list
        throw new UnsupportedOperationException("TODO(Day19-task03): segments");
    }

    public static String extension(Path file) {
        // TODO(Day19-task03): text after the last '.' of the file name; '' when no dot, when the dot is the first char (.bashrc), or when the name ends with '.'
        throw new UnsupportedOperationException("TODO(Day19-task03): extension");
    }

    public static Path changeExtension(Path file, String newExtension) {
        // TODO(Day19-task03): replace the extension of the file name (or append one if absent), keeping the parent; newExtension has no leading dot
        throw new UnsupportedOperationException("TODO(Day19-task03): changeExtension");
    }

    public static Path relativeTo(Path base, Path target) {
        // TODO(Day19-task03): base.relativize(target)
        throw new UnsupportedOperationException("TODO(Day19-task03): relativeTo");
    }

    public static Path resolveSafe(Path base, String userPath) {
        // TODO(Day19-task03): normalize the absolute base, resolve userPath, normalize; throw IllegalArgumentException when the result does not start with the base (absolute userPath or .. escape)
        throw new UnsupportedOperationException("TODO(Day19-task03): resolveSafe");
    }
}
