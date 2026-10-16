package com.javaprep.day45.task03;

import java.util.List;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class OrderedPublisher {

    public static final String TOPIC = "events.keyed";

    private final KafkaTemplate<String, String> kafkaTemplate;

    public OrderedPublisher(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    /**
     * Sends all values with the SAME key, in the given order, waiting for each acknowledgement (max 10 s each).
     * Returns the partition each record landed on (same size and order as {@code values}). Empty list -> empty result.
     */
    public List<Integer> publishAll(String key, List<String> values) throws Exception {
        // TODO(Day45-task03): loop over values, send with the key, block on each future, collect metadata.partition()
        throw new UnsupportedOperationException("TODO(Day45-task03): implement publishAll");
    }
}
