package com.javaprep.day30.task03;

import static org.assertj.core.api.Assertions.assertThat;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.math.BigDecimal;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.json.JsonTest;

@JsonTest
class EventJsonTest {

    @Autowired
    ObjectMapper mapper;

    @Test
    void serializesWithRenamedFormattedFields() throws Exception {
        Event e = new Event("Conf", LocalDate.of(2025, 3, 9), new BigDecimal("12.50"), "secret", "Hall A");
        JsonNode n = mapper.readTree(mapper.writeValueAsString(e));
        assertThat(n.get("event_name").asText()).isEqualTo("Conf");
        assertThat(n.get("date").asText()).isEqualTo("2025-03-09");
        assertThat(n.get("amount").decimalValue()).isEqualByComparingTo("12.50");
        assertThat(n.has("name")).isFalse();
    }

    @Test
    void internalNoteIsNeverSerialized() throws Exception {
        Event e = new Event("Conf", LocalDate.of(2025, 3, 9), BigDecimal.ONE, "secret", null);
        assertThat(mapper.writeValueAsString(e)).doesNotContain("secret").doesNotContain("internalNote");
    }

    @Test
    void nullsAreOmitted() throws Exception {
        Event e = new Event("Conf", LocalDate.of(2025, 3, 9), null, null, null);
        JsonNode n = mapper.readTree(mapper.writeValueAsString(e));
        assertThat(n.has("amount")).isFalse();
        assertThat(n.has("venue")).isFalse();
    }

    @Test
    void deserializesAndIgnoresInternalNote() throws Exception {
        String json = "{\"event_name\":\"Talk\",\"date\":\"2025-01-02\",\"amount\":3,\"internalNote\":\"hack\",\"venue\":\"B\"}";
        Event e = mapper.readerFor(Event.class).without(com.fasterxml.jackson.databind.DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES).readValue(json);
        assertThat(e.name()).isEqualTo("Talk");
        assertThat(e.date()).isEqualTo(LocalDate.of(2025, 1, 2));
        assertThat(e.internalNote()).isNull();
    }
}
