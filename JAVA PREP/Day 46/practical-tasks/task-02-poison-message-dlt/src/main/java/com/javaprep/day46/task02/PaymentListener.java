package com.javaprep.day46.task02;

import java.util.concurrent.atomic.AtomicInteger;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

/** PROVIDED. Fails permanently for any value containing "poison". */
@Component
public class PaymentListener {

    public static final String TOPIC = "payments.v1";

    private final ReceivedEvents received;
    private final AtomicInteger poisonAttempts = new AtomicInteger();

    public PaymentListener(ReceivedEvents received) {
        this.received = received;
    }

    @KafkaListener(topics = TOPIC, groupId = "payments")
    public void onMessage(ConsumerRecord<String, String> record) {
        if (record.value().contains("poison")) {
            poisonAttempts.incrementAndGet();
            throw new IllegalStateException("cannot process: " + record.value());
        }
        received.add(record.value());
    }

    public int poisonAttempts() {
        return poisonAttempts.get();
    }
}
