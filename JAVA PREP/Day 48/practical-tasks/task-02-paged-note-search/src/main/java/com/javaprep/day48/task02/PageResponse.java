package com.javaprep.day48.task02;

import java.util.List;

/** PROVIDED. Stable JSON shape for paged results. */
public record PageResponse<T>(List<T> content, int page, int size, long totalElements, int totalPages) {
}
