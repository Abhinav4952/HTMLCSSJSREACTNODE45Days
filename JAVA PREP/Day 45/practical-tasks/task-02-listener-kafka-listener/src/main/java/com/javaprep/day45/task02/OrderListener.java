package com.javaprep.day45.task02;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Component;

@Component
public class OrderListener {

    public static final String TOPIC = "orders.v1";

    private final ReceivedEvents received;

    public OrderListener(ReceivedEvents received) {
        this.received = received;
    }

    // TODO(Day45-task02): make this method a Kafka listener: @KafkaListener(topics = TOPIC, groupId = "audit")
    /** Stores "key=value" for every record in the received collector. */
    public void onMessage(ConsumerRecord<String, String> record) {
        // TODO(Day45-task02): received.add(record.key() + "=" + record.value())
        throw new UnsupportedOperationException("TODO(Day45-task02): implement onMessage");
    }
}
