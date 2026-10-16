package com.javaprep.day45.task01;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.test.EmbeddedKafkaBroker;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;

@SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
@EmbeddedKafka(partitions = 1, topics = {EventPublisher.TOPIC})
@DirtiesContext
class EventPublisherTest {

    @Autowired
    private EventPublisher publisher;
    @Autowired
    private EmbeddedKafkaBroker broker;

    @Test
    void publishReturnsMetadataForTheTopic() throws Exception {
        RecordMetadata md = publisher.publish("order-1", "created");
        assertThat(md.topic()).isEqualTo(EventPublisher.TOPIC);
        assertThat(md.offset()).isGreaterThanOrEqualTo(0);
    }

    @Test
    void recordArrivesWithKeyAndValue() throws Exception {
        publisher.publish("order-77", "paid");
        List<ConsumerRecord<String, String>> records = KafkaReader.readAll(broker, EventPublisher.TOPIC, 1);
        assertThat(records).anySatisfy(r -> {
            assertThat(r.key()).isEqualTo("order-77");
            assertThat(r.value()).isEqualTo("paid");
        });
    }

    @Test
    void nullValueIsRejected() {
        assertThatThrownBy(() -> publisher.publish("k", null)).isInstanceOf(IllegalArgumentException.class);
    }
}
