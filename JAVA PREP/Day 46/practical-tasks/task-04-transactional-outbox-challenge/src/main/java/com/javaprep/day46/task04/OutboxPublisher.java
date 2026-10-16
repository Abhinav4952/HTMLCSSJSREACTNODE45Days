package com.javaprep.day46.task04;

/** PROVIDED. Abstraction of the message broker (Kafka in production). */
@FunctionalInterface
public interface OutboxPublisher {

    void publish(String eventType, String payload);
}
