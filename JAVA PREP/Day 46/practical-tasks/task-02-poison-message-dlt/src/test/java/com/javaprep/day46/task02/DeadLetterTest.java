package com.javaprep.day46.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.test.EmbeddedKafkaBroker;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;

@SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
@EmbeddedKafka(partitions = 1, topics = {PaymentListener.TOPIC, PaymentListener.TOPIC + ".DLT"})
@DirtiesContext
class DeadLetterTest {

    @Autowired
    private KafkaTemplate<String, String> template;
    @Autowired
    private ReceivedEvents received;
    @Autowired
    private PaymentListener listener;
    @Autowired
    private EmbeddedKafkaBroker broker;

    @Test
    void poisonMessageGoesToDltAndHealthyMessagesStillFlow() throws Exception {
        template.send(PaymentListener.TOPIC, "p1", "ok-1").get();
        template.send(PaymentListener.TOPIC, "p2", "poison").get();
        template.send(PaymentListener.TOPIC, "p3", "ok-2").get();

        assertThat(received.awaitCount(2, Duration.ofSeconds(20))).isTrue();
        assertThat(received.snapshot()).containsExactly("ok-1", "ok-2");

        List<ConsumerRecord<String, String>> dead = KafkaReader.readAll(broker, PaymentListener.TOPIC + ".DLT", 1);
        assertThat(dead).hasSize(1);
        assertThat(dead.get(0).value()).isEqualTo("poison");
        assertThat(dead.get(0).key()).isEqualTo("p2");
        assertThat(listener.poisonAttempts()).isEqualTo(3);
    }
}
