package com.javaprep.day46.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;

class EventCodecTest {

    private final EventCodec codec = new EventCodec();

    @Test
    void roundTrip() {
        OrderPlacedEvent e = new OrderPlacedEvent(1, "o-1", "c-9", 1250);
        String json = codec.toJson(e);
        assertThat(json).contains("\"orderId\":\"o-1\"").contains("\"amountCents\":1250");
        assertThat(codec.fromJson(json)).isEqualTo(e);
    }

    @Test
    void unknownFieldsAreIgnored() {
        String json = "{\"version\":1,\"orderId\":\"o-1\",\"customerId\":\"c\",\"amountCents\":10,\"coupon\":\"X\"}";
        assertThat(codec.fromJson(json).orderId()).isEqualTo("o-1");
    }

    @Test
    void missingVersionDefaultsToOne() {
        OrderPlacedEvent e = codec.fromJson("{\"orderId\":\"o-1\",\"customerId\":\"c\",\"amountCents\":10}");
        assertThat(e.version()).isEqualTo(1);
    }

    @Test
    void invalidJsonIsRejected() {
        assertThatThrownBy(() -> codec.fromJson("{not json")).isInstanceOf(EventFormatException.class);
    }

    @Test
    void blankIdsAreRejected() {
        assertThatThrownBy(() -> codec.fromJson("{\"version\":1,\"orderId\":\" \",\"customerId\":\"c\",\"amountCents\":1}"))
                .isInstanceOf(EventFormatException.class);
        assertThatThrownBy(() -> codec.fromJson("{\"version\":1,\"orderId\":\"o\",\"amountCents\":1}"))
                .isInstanceOf(EventFormatException.class);
    }

    @Test
    void futureVersionsAreRejected() {
        assertThatThrownBy(() -> codec.fromJson("{\"version\":3,\"orderId\":\"o\",\"customerId\":\"c\",\"amountCents\":1}"))
                .isInstanceOf(EventFormatException.class).hasMessageContaining("unsupported version");
        assertThat(codec.fromJson("{\"version\":2,\"orderId\":\"o\",\"customerId\":\"c\",\"amountCents\":1}").version()).isEqualTo(2);
    }
}
