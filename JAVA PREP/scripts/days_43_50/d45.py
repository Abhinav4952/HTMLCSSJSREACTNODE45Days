from common import *

KAFKA = dep("org.springframework.kafka", "spring-kafka")
KAFKA_TEST = dep("org.springframework.kafka", "spring-kafka-test", scope="test")
S = ["spring-boot-starter"]

YML = "# Provided. Tests override spring.kafka.bootstrap-servers with the embedded broker address.\nspring:\n  kafka:\n    bootstrap-servers: localhost:9092\n    consumer:\n      auto-offset-reset: earliest\n      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer\n      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer\n    producer:\n      key-serializer: org.apache.kafka.common.serialization.StringSerializer\n      value-serializer: org.apache.kafka.common.serialization.StringSerializer\n      acks: all\n"

RECEIVED = r'''package %PKG%;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/** PROVIDED (do not edit). Thread-safe collector the listeners write to and the tests wait on. */
public class ReceivedEvents {

    private final List<String> items = new CopyOnWriteArrayList<>();

    public void add(String item) {
        items.add(item);
    }

    public List<String> snapshot() {
        return List.copyOf(items);
    }

    /** Polls until at least {@code count} items arrived or the timeout elapsed. */
    public boolean awaitCount(int count, Duration timeout) {
        long deadline = System.nanoTime() + timeout.toNanos();
        while (System.nanoTime() < deadline) {
            if (items.size() >= count) {
                return true;
            }
            try {
                Thread.sleep(25);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
        return items.size() >= count;
    }
}
'''
READER = r'''package %PKG%;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import org.apache.kafka.clients.consumer.Consumer;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.springframework.kafka.core.DefaultKafkaConsumerFactory;
import org.springframework.kafka.test.EmbeddedKafkaBroker;
import org.springframework.kafka.test.utils.KafkaTestUtils;

/** PROVIDED test helper: reads records from a topic with a throw-away consumer group. */
final class KafkaReader {

    private KafkaReader() {
    }

    static List<ConsumerRecord<String, String>> readAll(EmbeddedKafkaBroker broker, String topic, int expected) {
        Map<String, Object> props = KafkaTestUtils.consumerProps("verify-" + UUID.randomUUID(), "true", broker);
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        List<ConsumerRecord<String, String>> out = new ArrayList<>();
        try (Consumer<String, String> consumer = new DefaultKafkaConsumerFactory<>(props, new StringDeserializer(),
                new StringDeserializer()).createConsumer()) {
            consumer.subscribe(List.of(topic));
            long deadline = System.nanoTime() + Duration.ofSeconds(15).toNanos();
            while (out.size() < expected && System.nanoTime() < deadline) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(200));
                records.forEach(out::add);
            }
        }
        return out;
    }
}
'''

# ---- task 1: producer
PUB = r'''package %PKG%;

import org.apache.kafka.clients.producer.RecordMetadata;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class EventPublisher {

    public static final String TOPIC = "orders.v1";

    private final KafkaTemplate<String, String> kafkaTemplate;

    public EventPublisher(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    /**
     * Sends {@code value} with {@code key} to {@link #TOPIC}, WAITS (max 10 s) for the broker acknowledgement and
     * returns the record metadata (topic, partition, offset). value == null -> IllegalArgumentException (no tombstones).
     */
    public RecordMetadata publish(String key, String value) throws Exception {
        // TODO(%TAG%): validate, kafkaTemplate.send(TOPIC, key, value), block on the future with a timeout
        throw new UnsupportedOperationException("TODO(%TAG%): implement publish");
    }
}
'''
PUB_TEST = r'''package %PKG%;

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
'''
k1 = task("producer-kafka-template", "Producer with KafkaTemplate", "Warm-up", "Spring Boot + Kafka",
    "Publish keyed String events with `KafkaTemplate`, wait for the broker acknowledgement and verify with an `EmbeddedKafka` broker (no Docker, no local Kafka).",
    "boot", {"main/Application.java": APP, "res/application.yml": YML, "main/EventPublisher.java": PUB, "test/KafkaReader.java": READER, "test/EventPublisherTest.java": PUB_TEST},
    ["Reject `null` values with `IllegalArgumentException`.", "Send to `TOPIC` with the given key.", "Block on the returned future (<= 10 s) and return the `RecordMetadata`."],
    ["Broker slow to answer -> timeout exception.", "Null key is allowed (round-robin partitioning)."],
    ["`kafkaTemplate.send(...)` returns a `CompletableFuture<SendResult>` in Spring Kafka 3.x.", "`future.get(10, TimeUnit.SECONDS).getRecordMetadata()`."],
    starters=S, deps=[KAFKA, KAFKA_TEST])

# ---- task 2: consumer
LST = r'''package %PKG%;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Component;

@Component
public class OrderListener {

    public static final String TOPIC = "orders.v1";

    private final ReceivedEvents received;

    public OrderListener(ReceivedEvents received) {
        this.received = received;
    }

    // TODO(%TAG%): make this method a Kafka listener: @KafkaListener(topics = TOPIC, groupId = "audit")
    /** Stores "key=value" for every record in the received collector. */
    public void onMessage(ConsumerRecord<String, String> record) {
        // TODO(%TAG%): received.add(record.key() + "=" + record.value())
        throw new UnsupportedOperationException("TODO(%TAG%): implement onMessage");
    }
}
'''
CFG_RECEIVED = r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** PROVIDED. Exposes the shared collector bean. */
@Configuration
public class ReceivedConfig {

    @Bean
    public ReceivedEvents receivedEvents() {
        return new ReceivedEvents();
    }
}
'''
LST_TEST = r'''package %PKG%;

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
'''
k2 = task("listener-kafka-listener", "Consumer with @KafkaListener", "Core", "Spring Boot + Kafka",
    "Turn a plain method into a Kafka consumer with `@KafkaListener`, using a consumer group, and assert the records arrive in order.",
    "boot", {"main/Application.java": APP, "res/application.yml": YML, "main/ReceivedEvents.java": RECEIVED, "main/ReceivedConfig.java": CFG_RECEIVED,
             "main/OrderListener.java": LST, "test/OrderListenerTest.java": LST_TEST},
    ["Annotate `onMessage` with `@KafkaListener(topics = TOPIC, groupId = \"audit\")`.", "Store `key=value` for every record."],
    ["Listener starts after the first message was sent: `auto-offset-reset: earliest` (provided) handles this.", "Order is preserved inside one partition."],
    ["Import `org.springframework.kafka.annotation.KafkaListener`.", "Boot enables listener annotations automatically when spring-kafka is on the classpath."],
    starters=S, deps=[KAFKA, KAFKA_TEST])

# ---- task 3: keyed ordering
OP = r'''package %PKG%;

import java.util.List;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;

@Component
public class OrderedPublisher {

    public static final String TOPIC = "events.keyed";

    private final KafkaTemplate<String, String> kafkaTemplate;

    public OrderedPublisher(KafkaTemplate<String, String> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    /**
     * Sends all values with the SAME key, in the given order, waiting for each acknowledgement (max 10 s each).
     * Returns the partition each record landed on (same size and order as {@code values}). Empty list -> empty result.
     */
    public List<Integer> publishAll(String key, List<String> values) throws Exception {
        // TODO(%TAG%): loop over values, send with the key, block on each future, collect metadata.partition()
        throw new UnsupportedOperationException("TODO(%TAG%): implement publishAll");
    }
}
'''
OP_TEST = r'''package %PKG%;

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
'''
k3 = task("keyed-partition-ordering", "Keyed Partition Ordering", "Core", "Spring Boot + Kafka",
    "Prove Kafka's ordering guarantee: records with the same key go to the same partition and are read back in order, even on a 3-partition topic.",
    "boot", {"main/Application.java": APP, "res/application.yml": YML, "main/OrderedPublisher.java": OP, "test/KafkaReader.java": READER, "test/OrderedPublisherTest.java": OP_TEST},
    ["Send each value with the given key, in order.", "Block on every send and collect `RecordMetadata.partition()`.", "Return an empty list for empty input."],
    ["Without waiting you cannot know the partition.", "Ordering is only guaranteed per partition, not across partitions."],
    ["`Integer` list via `new ArrayList<>()`.", "Default partitioner hashes the key (murmur2) modulo partition count."],
    starters=S, deps=[KAFKA, KAFKA_TEST])

# ---- task 4: consumer groups
BILL = r'''package %PKG%;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.stereotype.Component;

@Component
public class BillingListener {

    public static final String TOPIC = "orders.groups";

    private final ReceivedEvents received = new ReceivedEvents();

    public ReceivedEvents received() {
        return received;
    }

    // TODO(%TAG%): @KafkaListener(topics = TOPIC, groupId = "billing")
    public void onMessage(ConsumerRecord<String, String> record) {
        // TODO(%TAG%): record the value
        throw new UnsupportedOperationException("TODO(%TAG%): implement BillingListener.onMessage");
    }
}
'''
SHIP = BILL.replace("BillingListener", "ShippingListener").replace('"billing"', '"shipping"').replace("    public static final String TOPIC = \"orders.groups\";\n\n", "    public static final String TOPIC = BillingListener.TOPIC;\n\n")
GRP_TEST = r'''package %PKG%;

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
'''
k4 = task("consumer-groups-challenge", "Independent Consumer Groups (Challenge)", "Challenge", "Spring Boot + Kafka",
    "Two services (billing and shipping) must each see every order event: give them different consumer groups, then reason about what would change if they shared a group.",
    "boot", {"main/Application.java": APP, "res/application.yml": YML, "main/ReceivedEvents.java": RECEIVED, "main/BillingListener.java": BILL,
             "main/ShippingListener.java": SHIP, "test/ConsumerGroupsTest.java": GRP_TEST},
    ["Make `BillingListener.onMessage` a listener in group `billing` that records the record value.", "Make `ShippingListener.onMessage` a listener in group `shipping` doing the same.",
     "Explain in your commit message (or a short comment) what would happen if both used the same group id."],
    ["Same group = messages are split between members (competing consumers); different groups = each group gets all messages."],
    ["The listener classes already own their collectors.", "Both listeners subscribe to the same topic."],
    starters=S, deps=[KAFKA, KAFKA_TEST])

TOPICS = [
    T("Kafka fundamentals: topics, partitions, offsets, and keys",
      "Kafka is a distributed, append-only commit log. A **topic** is split into **partitions**; each record in a partition gets a monotonically increasing **offset**. The producer picks the partition from the record **key** (hash) or round-robin when the key is null. Records are retained by time/size, not deleted when read.",
      "A log lets many independent consumers read the same data at their own pace, replay history, and scale reads by partition. Keys give per-entity ordering without global ordering costs.",
      ["High throughput, horizontal scaling by partitions", "Durable and replayable", "Per-key ordering", "Decouples producers from consumers"],
      ["Ordering only within a partition", "Partition count is hard to change", "Operational complexity", "At-least-once delivery means duplicates are possible"],
      "Choosing a bad key (e.g. constant) creates a hot partition; null keys lose per-entity ordering; too few partitions cap consumer parallelism.",
      "Producer: `kafkaTemplate.send(topic, key, value)`. Partition = `murmur2(key) % numPartitions`. Replication factor gives durability (`acks=all` + `min.insync.replicas`).",
      [("Key choice", "text", "orders for customer 42 -> key \"customer-42\" -> always partition 1 -> ordered"),
       ("CLI (manual lab)", "bash", "kafka-topics --bootstrap-server localhost:9092 --create --topic orders.v1 --partitions 3")],
      [("What guarantees ordering in Kafka?", "Records with the same key go to the same partition, and a partition is ordered."),
       ("Can two consumers of one group read the same partition?", "No; a partition is assigned to one member of a group at a time.")]),
    T("Producers with Spring Kafka: KafkaTemplate, serializers, acks",
      "Spring Boot auto-configures a `KafkaTemplate<K,V>` from `spring.kafka.producer.*`. `send()` is asynchronous and returns a `CompletableFuture<SendResult>`. Important settings: `acks` (0/1/all), `retries`, `enable.idempotence`, `linger.ms`, `batch.size`, key/value serializers.",
      "Understanding the asynchronous send and acknowledgement levels decides whether you can lose messages and whether you can block a web thread.",
      ["Simple API", "Configurable durability/latency trade-off", "Callbacks for success/failure"],
      ["Async errors are easy to ignore", "`acks=all` increases latency"],
      "Fire-and-forget without checking the future silently loses messages when the broker is down; `acks=0` loses data on leader failure.",
      "```java\nkafkaTemplate.send(\"orders.v1\", key, value)\n    .whenComplete((result, ex) -> { if (ex != null) log.error(\"send failed\", ex); });\n```\n```yaml\nspring.kafka.producer:\n  acks: all\n  properties:\n    enable.idempotence: true\n```",
      [("Blocking send in tests", "java", "RecordMetadata md = template.send(TOPIC, key, value).get(10, TimeUnit.SECONDS).getRecordMetadata();")],
      [("What does acks=all mean?", "The leader waits for all in-sync replicas before acknowledging."),
       ("Why use a callback?", "Because send() is asynchronous; failures arrive later.")]),
    T("Consumers, groups, and @KafkaListener",
      "A **consumer group** shares the work of a topic: each partition is assigned to exactly one consumer of the group; different groups each receive all records. `@KafkaListener(topics, groupId)` registers a listener container. Offsets are committed after processing (default: after each batch via the container).",
      "Groups give you both scaling (more consumers in one group) and fan-out (more groups). Offsets give you resume-after-restart semantics.",
      ["Declarative consumers", "Automatic rebalancing", "Offset management by the container"],
      ["Rebalances pause consumption", "At-least-once: handlers must tolerate duplicates", "Max consumers per group = partition count"],
      "A listener that throws forever blocks its partition (poison message); a wrong `auto-offset-reset` loses or replays data on first start.",
      "```java\n@KafkaListener(topics = \"orders.v1\", groupId = \"audit\")\nvoid on(ConsumerRecord<String,String> r) { ... }\n```\n`auto.offset.reset=earliest|latest` applies only when the group has no committed offset.",
      [("Fan-out", "text", "topic orders -> group billing (all records) + group shipping (all records)"),
       ("Competing consumers", "text", "group workers with 3 members, 3 partitions -> one partition each")],
      [("What triggers a rebalance?", "A consumer joining/leaving/crashing or partition changes."),
       ("What is auto.offset.reset?", "Where to start when no committed offset exists.")]),
    T("Testing Kafka code with EmbeddedKafka",
      "`spring-kafka-test` provides `@EmbeddedKafka`, an in-JVM broker started for the test class. `${spring.embedded.kafka.brokers}` holds its address; point `spring.kafka.bootstrap-servers` at it. `KafkaTestUtils` builds consumer/producer properties.",
      "Integration tests with a real broker catch serialization, partitioning and group behavior that mocks cannot. No Docker is needed.",
      ["Fast, self-contained", "Real Kafka semantics", "Works in CI"],
      ["Slower than unit tests (seconds)", "Async: tests need polling/timeouts"],
      "Mocking `KafkaTemplate` verifies only that you called `send`, not that bytes arrive or that ordering holds. Using `Thread.sleep` instead of polling makes tests flaky.",
      "```java\n@SpringBootTest(properties = \"spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}\")\n@EmbeddedKafka(partitions = 1, topics = \"orders.v1\")\n@DirtiesContext\nclass MyTest { }\n```",
      [("Await pattern", "java", "boolean ok = received.awaitCount(3, Duration.ofSeconds(15));")],
      [("How does the app find the embedded broker?", "Through the `spring.embedded.kafka.brokers` property."),
       ("Why @DirtiesContext?", "So each class gets a fresh context/broker and listeners do not leak across tests.")]),
]

day(45, "Kafka I: Producers, Consumers, and EmbeddedKafka", "Microservices (Kafka)",
    "Topics, partitions, keys, offsets, consumer groups, KafkaTemplate and @KafkaListener, tested with EmbeddedKafka",
    ["Explain topics, partitions, offsets and keys", "Publish keyed events with `KafkaTemplate` and handle acknowledgements", "Consume with `@KafkaListener` and consumer groups", "Prove per-key ordering", "Test with `@EmbeddedKafka` without Docker"],
    ["Day 43-44 microservices", "Optional: `setup/KAFKA_SETUP.md` for manual labs (tests do not need it)"],
    TOPICS, [k1, k2, k3, k4],
    [("Kafka vs RabbitMQ?", "Kafka is a replayable partitioned log built for throughput and streaming; RabbitMQ is a broker with queues and routing, messages are removed when consumed."),
     ("How do you scale consumers?", "Add consumers to the group up to the partition count."),
     ("What delivery semantics does Kafka give?", "At-least-once by default; exactly-once with idempotent producers + transactions within Kafka."),
     ("Why use keys?", "To get per-entity ordering and co-locate related events."),
     ("What is a rebalance?", "Reassignment of partitions among group members.")],
    ["Ignoring the send future.", "Expecting global ordering.", "Using a constant key.", "Forgetting `earliest` in tests so the first messages are skipped.", "Sleeping instead of polling in tests."],
    ["Apache Kafka documentation: Design", "Spring for Apache Kafka Reference", "Confluent: Kafka 101"],
    [("Topic", "Named log of records"), ("Partition", "Ordered shard of a topic"), ("Offset", "Position in a partition"), ("Consumer group", "Set of consumers sharing a topic's partitions"),
     ("Broker", "Kafka server"), ("acks", "Producer durability level")],
    "2-3 h theory + 4-6 h tasks", spring=True)
