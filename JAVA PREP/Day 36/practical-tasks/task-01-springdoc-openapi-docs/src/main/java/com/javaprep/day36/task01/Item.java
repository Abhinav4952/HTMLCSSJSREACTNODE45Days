package com.javaprep.day36.task01;

import io.swagger.v3.oas.annotations.media.Schema;

public record Item(
        @Schema(description = "Unique identifier", example = "1")
        long id,
        // TODO(Day36-task01): document this field: @Schema(description = "Display name", example = "Laptop")
        String name,
        // TODO(Day36-task01): document this field: @Schema(description = "Price in euro", example = "999.00")
        double price) {
}
