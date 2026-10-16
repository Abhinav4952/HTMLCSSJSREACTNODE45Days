package com.javaprep.day46.task01;

import com.fasterxml.jackson.databind.ObjectMapper;

/** Serializes/deserializes versioned events (the "tolerant reader" pattern). */
public class EventCodec {

    public static final int MAX_SUPPORTED_VERSION = 2;

    private final ObjectMapper mapper;

    public EventCodec() {
        // TODO(Day46-task01): create the ObjectMapper and configure it to IGNORE unknown properties (forward compatibility)
        this.mapper = new ObjectMapper();
    }

    public String toJson(OrderPlacedEvent event) {
        // TODO(Day46-task01): mapper.writeValueAsString, wrap checked exceptions in EventFormatException
        throw new UnsupportedOperationException("TODO(Day46-task01): implement toJson");
    }

    /**
     * Rules: invalid JSON -> EventFormatException; blank orderId or customerId -> EventFormatException;
     * missing/0 version (events written before versioning) -> treated as version 1;
     * version greater than MAX_SUPPORTED_VERSION -> EventFormatException("unsupported version").
     */
    public OrderPlacedEvent fromJson(String json) {
        // TODO(Day46-task01): parse, then validate and normalise as described
        throw new UnsupportedOperationException("TODO(Day46-task01): implement fromJson");
    }
}
