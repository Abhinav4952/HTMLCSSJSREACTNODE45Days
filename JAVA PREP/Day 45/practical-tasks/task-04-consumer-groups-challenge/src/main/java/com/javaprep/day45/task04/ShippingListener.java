package com.javaprep.day45.task04;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Component;

@Component
public class ShippingListener {

    public static final String TOPIC = BillingListener.TOPIC;

    private final ReceivedEvents received = new ReceivedEvents();

    public ReceivedEvents received() {
        return received;
    }

    // TODO(Day45-task04): @KafkaListener(topics = TOPIC, groupId = "shipping")
    public void onMessage(ConsumerRecord<String, String> record) {
        // TODO(Day45-task04): record the value
        throw new UnsupportedOperationException("TODO(Day45-task04): implement ShippingListener.onMessage");
    }
}
