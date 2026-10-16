package com.javaprep.day45.task01;

import org.apache.kafka.clients.producer.RecordMetadata;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class EventPublisher {

    public static final String TOPIC = "orders.v1";

    private final KafkaTemplate<String, String> kafkaTemplate;

    public EventPublisher(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    /**
     * Sends {@code value} with {@code key} to {@link #TOPIC}, WAITS (max 10 s) for the broker acknowledgement and
     * returns the record metadata (topic, partition, offset). value == null -> IllegalArgumentException (no tombstones).
     */
    public RecordMetadata publish(String key, String value) throws Exception {
        // TODO(Day45-task01): validate, kafkaTemplate.send(TOPIC, key, value), block on the future with a timeout
        throw new UnsupportedOperationException("TODO(Day45-task01): implement publish");
    }
}
