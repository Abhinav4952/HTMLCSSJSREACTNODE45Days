package com.javaprep.day45.task03;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.test.EmbeddedKafkaBroker;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;

@SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
@EmbeddedKafka(partitions = 3, topics = {OrderedPublisher.TOPIC})
@DirtiesContext
class OrderedPublisherTest {

    @Autowired
    private OrderedPublisher publisher;
    @Autowired
    private EmbeddedKafkaBroker broker;

    @Test
    void sameKeyAlwaysLandsOnOnePartition() throws Exception {
        List<Integer> partitions = publisher.publishAll("customer-A", List.of("1", "2", "3", "4", "5"));
        assertThat(partitions).hasSize(5);
        assertThat(partitions).containsOnly(partitions.get(0));
    }

    @Test
    void perKeyOrderIsPreserved() throws Exception {
        publisher.publishAll("customer-B", List.of("b1", "b2", "b3", "b4"));
        publisher.publishAll("customer-C", List.of("c1", "c2", "c3"));
        List<ConsumerRecord<String, String>> all = KafkaReader.readAll(broker, OrderedPublisher.TOPIC, 7);
        List<String> forB = all.stream().filter(r -> "customer-B".equals(r.key())).map(ConsumerRecord::value).toList();
        List<String> forC = all.stream().filter(r -> "customer-C".equals(r.key())).map(ConsumerRecord::value).toList();
        assertThat(forB).containsExactly("b1", "b2", "b3", "b4");
        assertThat(forC).containsExactly("c1", "c2", "c3");
    }

    @Test
    void emptyInputSendsNothing() throws Exception {
        assertThat(publisher.publishAll("x", List.of())).isEmpty();
    }
}
