package com.javaprep.day45.task04;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Component;

@Component
public class BillingListener {

    public static final String TOPIC = "orders.groups";

    private final ReceivedEvents received = new ReceivedEvents();

    public ReceivedEvents received() {
        return received;
    }

    // TODO(Day45-task04): @KafkaListener(topics = TOPIC, groupId = "billing")
    public void onMessage(ConsumerRecord<String, String> record) {
        // TODO(Day45-task04): record the value
        throw new UnsupportedOperationException("TODO(Day45-task04): implement BillingListener.onMessage");
    }
}
