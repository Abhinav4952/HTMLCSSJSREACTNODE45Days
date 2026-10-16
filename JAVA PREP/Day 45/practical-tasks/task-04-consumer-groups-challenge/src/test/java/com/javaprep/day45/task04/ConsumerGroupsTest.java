package com.javaprep.day45.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.test.context.EmbeddedKafka;
import org.springframework.test.annotation.DirtiesContext;

@SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
@EmbeddedKafka(partitions = 1, topics = {BillingListener.TOPIC})
@DirtiesContext
class ConsumerGroupsTest {

    @Autowired
    private KafkaTemplate<String, String> template;
    @Autowired
    private BillingListener billing;
    @Autowired
    private ShippingListener shipping;

    @Test
    void everyGroupReceivesEveryMessage() throws Exception {
        template.send(BillingListener.TOPIC, "o1", "a").get();
        template.send(BillingListener.TOPIC, "o2", "b").get();
        template.send(BillingListener.TOPIC, "o3", "c").get();
        assertThat(billing.received().awaitCount(3, Duration.ofSeconds(15))).isTrue();
        assertThat(shipping.received().awaitCount(3, Duration.ofSeconds(15))).isTrue();
        assertThat(billing.received().snapshot()).containsExactly("a", "b", "c");
        assertThat(shipping.received().snapshot()).containsExactly("a", "b", "c");
    }
}
