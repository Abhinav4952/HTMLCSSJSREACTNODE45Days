package com.javaprep.day18.task03;

import java.util.List;

/** Provided value type; items may be null. */
public record Order(String id, List<LineItem> items) {
}
