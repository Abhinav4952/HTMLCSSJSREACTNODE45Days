package com.javaprep.day44.task01;

/** PROVIDED. id, path predicate prefix (e.g. /api/users) and the target service URI. */
public record Route(String id, String pathPrefix, String targetUri) {
}
