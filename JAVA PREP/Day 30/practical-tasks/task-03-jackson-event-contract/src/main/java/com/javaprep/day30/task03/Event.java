package com.javaprep.day30.task03;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * JSON contract:
 *  - "name" is serialized as "event_name"
 *  - "date" is a string like 2025-03-09
 *  - "internalNote" never appears in JSON (in or out)
 *  - null fields are omitted from output
 */
// TODO(Day30-task03): add @JsonInclude(JsonInclude.Include.NON_NULL) on the record
public record Event(
        // TODO(Day30-task03): rename to event_name with @JsonProperty
        String name,
        // TODO(Day30-task03): format as yyyy-MM-dd text with @JsonFormat(shape = STRING, pattern = "yyyy-MM-dd")
        LocalDate date,
        BigDecimal amount,
        // TODO(Day30-task03): exclude from JSON with @JsonIgnore
        String internalNote,
        String venue) {
}
