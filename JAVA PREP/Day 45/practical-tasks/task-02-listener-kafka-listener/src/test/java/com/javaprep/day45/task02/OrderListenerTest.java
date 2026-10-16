package com.javaprep.day45.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;

@SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
@EmbeddedKafka(partitions = 1, topics = {OrderListener.TOPIC})
@DirtiesContext
class OrderListenerTest {

    @Autowired
    private KafkaTemplate<String, String> template;
    @Autowired
    private ReceivedEvents received;

    @Test
    void listenerReceivesRecordsInOrder() throws Exception {
        template.send(OrderListener.TOPIC, "k1", "created").get();
        template.send(OrderListener.TOPIC, "k1", "paid").get();
        template.send(OrderListener.TOPIC, "k1", "shipped").get();
        assertThat(received.awaitCount(3, Duration.ofSeconds(15))).isTrue();
        assertThat(received.snapshot()).containsExactly("k1=created", "k1=paid", "k1=shipped");
    }
}
