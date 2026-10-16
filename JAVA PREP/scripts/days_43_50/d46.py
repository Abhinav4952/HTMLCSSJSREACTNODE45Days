from common import *
from d45 import KAFKA, KAFKA_TEST, YML, RECEIVED, READER

S = ["spring-boot-starter"]

# ---- task 1: JSON codec
EVT = "package %PKG%;\n\n/** PROVIDED. v1 contract of the OrderPlaced event. */\npublic record OrderPlacedEvent(int version, String orderId, String customerId, long amountCents) {\n}\n"
EEX = "package %PKG%;\n\n/** PROVIDED. Thrown for malformed or invalid events. */\npublic class EventFormatException extends RuntimeException {\n\n    public EventFormatException(String message, Throwable cause) {\n        super(message, cause);\n    }\n\n    public EventFormatException(String message) {\n        super(message);\n    }\n}\n"
CODEC = r'''package %PKG%;

import com.fasterxml.jackson.databind.ObjectMapper;

/** Serializes/deserializes versioned events (the "tolerant reader" pattern). */
public class EventCodec {

    public static final int MAX_SUPPORTED_VERSION = 2;

    private final ObjectMapper mapper;

    public EventCodec() {
        // TODO(%TAG%): create the ObjectMapper and configure it to IGNORE unknown properties (forward compatibility)
        this.mapper = new ObjectMapper();
    }

    public String toJson(OrderPlacedEvent event) {
        // TODO(%TAG%): mapper.writeValueAsString, wrap checked exceptions in EventFormatException
        throw new UnsupportedOperationException("TODO(%TAG%): implement toJson");
    }

    /**
     * Rules: invalid JSON -> EventFormatException; blank orderId or customerId -> EventFormatException;
     * missing/0 version (events written before versioning) -> treated as version 1;
     * version greater than MAX_SUPPORTED_VERSION -> EventFormatException("unsupported version").
     */
    public OrderPlacedEvent fromJson(String json) {
        // TODO(%TAG%): parse, then validate and normalise as described
        throw new UnsupportedOperationException("TODO(%TAG%): implement fromJson");
    }
}
'''
CODEC_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;

class EventCodecTest {

    private final EventCodec codec = new EventCodec();

    @Test
    void roundTrip() {
        OrderPlacedEvent e = new OrderPlacedEvent(1, "o-1", "c-9", 1250);
        String json = codec.toJson(e);
        assertThat(json).contains("\"orderId\":\"o-1\"").contains("\"amountCents\":1250");
        assertThat(codec.fromJson(json)).isEqualTo(e);
    }

    @Test
    void unknownFieldsAreIgnored() {
        String json = "{\"version\":1,\"orderId\":\"o-1\",\"customerId\":\"c\",\"amountCents\":10,\"coupon\":\"X\"}";
        assertThat(codec.fromJson(json).orderId()).isEqualTo("o-1");
    }

    @Test
    void missingVersionDefaultsToOne() {
        OrderPlacedEvent e = codec.fromJson("{\"orderId\":\"o-1\",\"customerId\":\"c\",\"amountCents\":10}");
        assertThat(e.version()).isEqualTo(1);
    }

    @Test
    void invalidJsonIsRejected() {
        assertThatThrownBy(() -> codec.fromJson("{not json")).isInstanceOf(EventFormatException.class);
    }

    @Test
    void blankIdsAreRejected() {
        assertThatThrownBy(() -> codec.fromJson("{\"version\":1,\"orderId\":\" \",\"customerId\":\"c\",\"amountCents\":1}"))
                .isInstanceOf(EventFormatException.class);
        assertThatThrownBy(() -> codec.fromJson("{\"version\":1,\"orderId\":\"o\",\"amountCents\":1}"))
                .isInstanceOf(EventFormatException.class);
    }

    @Test
    void futureVersionsAreRejected() {
        assertThatThrownBy(() -> codec.fromJson("{\"version\":3,\"orderId\":\"o\",\"customerId\":\"c\",\"amountCents\":1}"))
                .isInstanceOf(EventFormatException.class).hasMessageContaining("unsupported version");
        assertThat(codec.fromJson("{\"version\":2,\"orderId\":\"o\",\"customerId\":\"c\",\"amountCents\":1}").version()).isEqualTo(2);
    }
}
'''
j1 = task("json-event-contract", "Versioned JSON Event Contract", "Warm-up", "Spring Boot (Jackson)",
    "Define a tolerant JSON event codec: ignore unknown fields, default the version, validate required fields and reject unsupported versions.",
    "boot", {"main/Application.java": APP, "main/OrderPlacedEvent.java": EVT, "main/EventFormatException.java": EEX, "main/EventCodec.java": CODEC, "test/EventCodecTest.java": CODEC_TEST},
    ["Configure the mapper with `FAIL_ON_UNKNOWN_PROPERTIES = false`.", "Implement `toJson` / `fromJson` wrapping Jackson exceptions in `EventFormatException`.", "Normalize version 0 (absent) to 1.", "Reject blank/missing ids and versions above `MAX_SUPPORTED_VERSION`."],
    ["Missing primitive fields deserialize as 0 in records.", "Null `customerId`."],
    ["Records are supported by Jackson 2.12+.", "Because the record is immutable, build a new one to change the version."],
    starters=["spring-boot-starter-json"])

# ---- task 2: DLT
PL = r'''package %PKG%;

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
'''
EH = r'''package %PKG%;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.kafka.listener.DefaultErrorHandler;

@Configuration
public class ErrorHandlingConfig {

    /**
     * Retry a failing record 2 more times (3 deliveries in total) with a 10 ms pause, then publish it to the
     * dead-letter topic "<original>.DLT" and move on. Boot wires a CommonErrorHandler bean into the listener factory.
     */
    @Bean
    public DefaultErrorHandler errorHandler(KafkaTemplate<Object, Object> template) {
        // TODO(%TAG%): DeadLetterPublishingRecoverer(template) + FixedBackOff(10L, 2L) -> new DefaultErrorHandler(recoverer, backOff)
        throw new UnsupportedOperationException("TODO(%TAG%): implement errorHandler");
    }
}
'''
DLT_TEST = r'''package %PKG%;

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
'''
j2 = task("poison-message-dlt", "Poison Message and Dead-Letter Topic", "Core", "Spring Boot + Kafka",
    "Configure a `DefaultErrorHandler` with bounded retries and a `DeadLetterPublishingRecoverer` so one bad record cannot block a partition.",
    "boot", {"main/Application.java": APP, "res/application.yml": YML, "main/ReceivedEvents.java": RECEIVED,
             "main/ReceivedConfig.java": "package %PKG%;\n\nimport org.springframework.context.annotation.Bean;\nimport org.springframework.context.annotation.Configuration;\n\n/** PROVIDED. */\n@Configuration\npublic class ReceivedConfig {\n\n    @Bean\n    public ReceivedEvents receivedEvents() {\n        return new ReceivedEvents();\n    }\n}\n",
             "main/PaymentListener.java": PL, "main/ErrorHandlingConfig.java": EH, "test/KafkaReader.java": READER, "test/DeadLetterTest.java": DLT_TEST},
    ["Create a `DeadLetterPublishingRecoverer` from the template (default destination `<topic>.DLT`, same partition).", "Use `FixedBackOff(10L, 2L)`: two retries after the first failure.", "Return a `DefaultErrorHandler(recoverer, backOff)`."],
    ["The DLT must have at least as many partitions as the source topic.", "Healthy records after the poison one must still be processed."],
    ["`org.springframework.util.backoff.FixedBackOff`.", "Spring Boot applies a `CommonErrorHandler` bean to the auto-configured listener container factory."],
    starters=S, deps=[KAFKA, KAFKA_TEST])

# ---- task 3: idempotent consumer
SCHEMA = "package %PKG%;\n\n/** PROVIDED. Table that remembers which events were already handled. */\npublic final class Schema {\n\n    public static final String PROCESSED_EVENTS =\n            \"create table processed_events (event_id varchar(100) primary key, processed_at timestamp default current_timestamp)\";\n\n    private Schema() {\n    }\n}\n"
IC = r'''package %PKG%;

import java.sql.Connection;

/** Makes at-least-once delivery behave like exactly-once for side effects, using a processed-events table. */
public class IdempotentConsumer {

    private final Connection connection;

    public IdempotentConsumer(Connection connection) {
        this.connection = connection;
    }

    /**
     * In ONE transaction: insert eventId into processed_events, then run {@code sideEffect}, then commit.
     * <ul>
     *   <li>eventId already stored (primary-key violation) -> return false, sideEffect NOT run</li>
     *   <li>sideEffect throws -> roll back (event is NOT marked processed), rethrow the exception</li>
     *   <li>otherwise return true</li>
     *   <li>auto-commit must be restored to its previous value afterwards; SQLExceptions -> IllegalStateException</li>
     * </ul>
     */
    public boolean processOnce(String eventId, Runnable sideEffect) {
        // TODO(%TAG%): setAutoCommit(false), insert, detect SQLIntegrityConstraintViolationException, run, commit / rollback
        throw new UnsupportedOperationException("TODO(%TAG%): implement processOnce");
    }
}
'''
IC_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicInteger;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class IdempotentConsumerTest {

    private Connection conn;
    private IdempotentConsumer consumer;
    private final AtomicInteger effects = new AtomicInteger();

    @BeforeEach
    void setUp() throws Exception {
        conn = DriverManager.getConnection("jdbc:h2:mem:day46t3_" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1", "sa", "");
        try (Statement st = conn.createStatement()) {
            st.execute(Schema.PROCESSED_EVENTS);
        }
        consumer = new IdempotentConsumer(conn);
    }

    @AfterEach
    void tearDown() throws Exception {
        conn.close();
    }

    private int storedEvents() throws Exception {
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery("select count(*) from processed_events")) {
            rs.next();
            return rs.getInt(1);
        }
    }

    @Test
    void firstDeliveryRunsTheSideEffect() throws Exception {
        assertThat(consumer.processOnce("e-1", effects::incrementAndGet)).isTrue();
        assertThat(effects.get()).isEqualTo(1);
        assertThat(storedEvents()).isEqualTo(1);
    }

    @Test
    void duplicateDeliveryIsSkipped() {
        consumer.processOnce("e-1", effects::incrementAndGet);
        assertThat(consumer.processOnce("e-1", effects::incrementAndGet)).isFalse();
        assertThat(effects.get()).isEqualTo(1);
    }

    @Test
    void differentEventsAreBothProcessed() {
        consumer.processOnce("e-1", effects::incrementAndGet);
        consumer.processOnce("e-2", effects::incrementAndGet);
        assertThat(effects.get()).isEqualTo(2);
    }

    @Test
    void failedSideEffectRollsBackSoRetryWorks() throws Exception {
        assertThatThrownBy(() -> consumer.processOnce("e-1", () -> {
            throw new IllegalStateException("boom");
        })).isInstanceOf(IllegalStateException.class).hasMessage("boom");
        assertThat(storedEvents()).isZero();
        assertThat(consumer.processOnce("e-1", effects::incrementAndGet)).isTrue();
        assertThat(effects.get()).isEqualTo(1);
    }

    @Test
    void autoCommitIsRestored() throws Exception {
        consumer.processOnce("e-1", effects::incrementAndGet);
        assertThat(conn.getAutoCommit()).isTrue();
        consumer.processOnce("e-1", effects::incrementAndGet);
        assertThat(conn.getAutoCommit()).isTrue();
    }
}
'''
j3 = task("idempotent-consumer", "Idempotent Consumer with a Processed-Events Table", "Core", "Java + JDBC (H2)",
    "Guarantee a side effect runs once even when the same event is delivered twice, using a primary-key insert in the same transaction.",
    "h2", {"main/Schema.java": SCHEMA, "main/IdempotentConsumer.java": IC, "test/IdempotentConsumerTest.java": IC_TEST},
    ["Insert the event id inside a transaction before running the side effect.", "Detect duplicates via `SQLIntegrityConstraintViolationException` and return false.", "Roll back and rethrow when the side effect fails so the event can be retried.", "Always restore auto-commit."],
    ["Failure of the side effect after the insert.", "Duplicate id.", "Connection state after errors."],
    ["Use try/finally to restore auto-commit.", "On duplicate, roll back before returning."])

# ---- task 4: outbox
OSCHEMA = r'''package %PKG%;

/** PROVIDED. Orders table plus the transactional outbox table. */
public final class OutboxSchema {

    public static final String[] DDL = {
            "create table orders (id varchar(50) primary key, payload varchar(1000))",
            "create table outbox (id bigint auto_increment primary key, aggregate_id varchar(50) not null, "
                    + "event_type varchar(50) not null, payload varchar(1000) not null, published boolean not null default false)"
    };

    private OutboxSchema() {
    }
}
'''
OPUB = "package %PKG%;\n\n/** PROVIDED. Abstraction of the message broker (Kafka in production). */\n@FunctionalInterface\npublic interface OutboxPublisher {\n\n    void publish(String eventType, String payload);\n}\n"
OSVC = r'''package %PKG%;

import java.sql.Connection;

public class OrderService {

    private final Connection connection;

    public OrderService(Connection connection) {
        this.connection = connection;
    }

    /**
     * Atomically (ONE transaction) inserts the order row AND an outbox row (event_type "OrderPlaced", aggregate_id =
     * orderId, same payload). Any failure rolls BOTH back and is rethrown as IllegalStateException.
     * Auto-commit is restored afterwards.
     */
    public void placeOrder(String orderId, String payload) {
        // TODO(%TAG%): setAutoCommit(false); insert into orders; insert into outbox; commit; rollback on any exception
        throw new UnsupportedOperationException("TODO(%TAG%): implement placeOrder");
    }
}
'''
OPOLL = r'''package %PKG%;

import java.sql.Connection;

/** Relays unpublished outbox rows to the broker in id order (at-least-once). */
public class OutboxPoller {

    private final Connection connection;

    public OutboxPoller(Connection connection) {
        this.connection = connection;
    }

    /**
     * Selects unpublished rows ordered by id, publishes each, and marks it published AFTER a successful publish.
     * If the publisher throws, STOP (later rows must not overtake the failed one), leave it unpublished and return
     * the number of rows published in this call.
     */
    public int pollOnce(OutboxPublisher publisher) {
        // TODO(%TAG%): select unpublished rows order by id; publish; update published = true; stop on first failure
        throw new UnsupportedOperationException("TODO(%TAG%): implement pollOnce");
    }
}
'''
OTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class OutboxTest {

    private Connection conn;
    private OrderService orders;
    private OutboxPoller poller;

    @BeforeEach
    void setUp() throws Exception {
        conn = DriverManager.getConnection("jdbc:h2:mem:day46t4_" + UUID.randomUUID() + ";DB_CLOSE_DELAY=-1", "sa", "");
        try (Statement st = conn.createStatement()) {
            for (String ddl : OutboxSchema.DDL) {
                st.execute(ddl);
            }
        }
        orders = new OrderService(conn);
        poller = new OutboxPoller(conn);
    }

    @AfterEach
    void tearDown() throws Exception {
        conn.close();
    }

    private int count(String table) throws Exception {
        try (Statement st = conn.createStatement(); ResultSet rs = st.executeQuery("select count(*) from " + table)) {
            rs.next();
            return rs.getInt(1);
        }
    }

    @Test
    void placeOrderWritesOrderAndOutboxRow() throws Exception {
        orders.placeOrder("o-1", "{\"id\":\"o-1\"}");
        assertThat(count("orders")).isEqualTo(1);
        assertThat(count("outbox")).isEqualTo(1);
        assertThat(conn.getAutoCommit()).isTrue();
    }

    @Test
    void failureRollsBackTheOrderToo() throws Exception {
        // outbox.payload is NOT NULL: the outbox insert fails after the order insert succeeded
        assertThatThrownBy(() -> orders.placeOrder("o-2", null)).isInstanceOf(IllegalStateException.class);
        assertThat(count("orders")).isZero();
        assertThat(count("outbox")).isZero();
        assertThat(conn.getAutoCommit()).isTrue();
    }

    @Test
    void pollerPublishesInOrderAndMarksRows() throws Exception {
        orders.placeOrder("o-1", "p1");
        orders.placeOrder("o-2", "p2");
        List<String> sent = new ArrayList<>();
        assertThat(poller.pollOnce((type, payload) -> sent.add(type + ":" + payload))).isEqualTo(2);
        assertThat(sent).containsExactly("OrderPlaced:p1", "OrderPlaced:p2");
        assertThat(poller.pollOnce((type, payload) -> sent.add("again"))).isZero();
    }

    @Test
    void failedPublishStopsAndRetriesLater() throws Exception {
        orders.placeOrder("o-1", "p1");
        orders.placeOrder("o-2", "p2");
        orders.placeOrder("o-3", "p3");
        List<String> sent = new ArrayList<>();
        int first = poller.pollOnce((type, payload) -> {
            if (payload.equals("p2")) {
                throw new IllegalStateException("broker down");
            }
            sent.add(payload);
        });
        assertThat(first).isEqualTo(1);
        assertThat(sent).containsExactly("p1");

        int second = poller.pollOnce((type, payload) -> sent.add(payload));
        assertThat(second).isEqualTo(2);
        assertThat(sent).containsExactly("p1", "p2", "p3");
    }
}
'''
j4 = task("transactional-outbox-challenge", "Transactional Outbox Simulation (Challenge)", "Challenge", "Java + JDBC (H2)",
    "Solve the dual-write problem: write the order and its event in one transaction, then relay events to the broker with a poller that preserves order and tolerates failures.",
    "h2", {"main/OutboxSchema.java": OSCHEMA, "main/OutboxPublisher.java": OPUB, "main/OrderService.java": OSVC, "main/OutboxPoller.java": OPOLL, "test/OutboxTest.java": OTEST},
    ["`placeOrder` inserts order + outbox row atomically.", "Any failure rolls back both rows; restore auto-commit.", "`pollOnce` publishes unpublished rows in id order and marks each after success.", "Stop at the first publisher failure and return the count so far."],
    ["Null payload (outbox constraint).", "Publisher fails mid-batch.", "Second poll republishes only what remains."],
    ["Read the result set fully into a list before updating rows.", "Use `PreparedStatement` with parameters."])

TOPICS = [
    T("JSON events and schema evolution",
      "Events are facts published to a topic. JSON is the common serialization. A good event has an **id**, **type**, **version** and business payload; consumers follow the **tolerant reader** rule (ignore unknown fields, apply defaults for missing optional ones). Spring Kafka offers `JsonSerializer/JsonDeserializer`; many teams serialize explicitly with Jackson and keep Kafka values as Strings/bytes.",
      "Producers and consumers deploy independently, so the contract must evolve without breaking old consumers. Additive changes are safe; renames/removals need a new version.",
      ["Human-readable and tool-friendly", "Easy evolution with additive fields", "Language-neutral"],
      ["Larger than binary formats (Avro/Protobuf)", "No enforced schema without extra tooling (Schema Registry)"],
      "Strict deserialization (`FAIL_ON_UNKNOWN_PROPERTIES=true`) makes every new producer field an outage for old consumers; using Java class names as type headers couples services.",
      "```java\nObjectMapper m = new ObjectMapper().configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);\nrecord OrderPlaced(int version, String orderId, String customerId, long amountCents) {}\n```\nRules: add fields, never reuse names with new meaning, bump `version` for breaking changes, support N and N-1.",
      [("Event envelope", "json", "{\"eventId\":\"6c1f...\",\"type\":\"OrderPlaced\",\"version\":1,\"occurredAt\":\"2025-01-01T10:00:00Z\",\"data\":{\"orderId\":\"o-1\"}}")],
      [("Which changes are backward compatible?", "Adding optional fields; removing or renaming is not."),
       ("Why keep an event id?", "For idempotent consumers and tracing.")]),
    T("Error handling, retries, and dead-letter topics",
      "Spring Kafka's `DefaultErrorHandler` retries a failed record according to a `BackOff`, then calls a recoverer. `DeadLetterPublishingRecoverer` publishes the failed record (with exception headers) to `<topic>.DLT`. Non-retryable exceptions (deserialization, validation) can be classified to skip retries.",
      "One poison message that always throws would otherwise block a partition forever (the container re-delivers it). A DLT isolates it for inspection and replay while healthy traffic continues.",
      ["Pipeline keeps flowing", "Failed data is preserved for analysis", "Retry policy is centralized"],
      ["Order across the failed record is relaxed", "DLT needs monitoring/alerting and a replay process", "Blocking retries delay the partition"],
      "No handler: default behavior retries a few times then logs and SKIPS (data loss). Infinite retry: partition blocked. DLT never monitored: silent data loss.",
      "```java\n@Bean DefaultErrorHandler errorHandler(KafkaTemplate<Object,Object> t) {\n  var recoverer = new DeadLetterPublishingRecoverer(t);\n  return new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3L));\n}\n```\nUse `ExponentialBackOff` for real systems; `addNotRetryableExceptions(...)` for permanent errors; `ErrorHandlingDeserializer` to survive bad bytes.",
      [("Non-retryable", "java", "handler.addNotRetryableExceptions(IllegalArgumentException.class);"),
       ("DLT naming", "text", "payments.v1 -> payments.v1.DLT (same partition number)")],
      [("What is a poison message?", "A record that fails every time it is processed."),
       ("Why must the DLT have enough partitions?", "The recoverer publishes to the same partition number by default.")]),
    T("Idempotent consumers and the transactional outbox",
      "Kafka gives **at-least-once** delivery to consumers, so duplicates happen (rebalance, retry, producer retry). An **idempotent consumer** records processed event ids (primary key) in the same transaction as the side effect. The **transactional outbox** solves the dual-write problem: write business data and an outbox row in one local transaction; a poller/CDC relays the outbox to Kafka.",
      "You cannot atomically update a database and publish to Kafka. Without the outbox you either lose events (DB commit, then crash before publish) or publish phantom events (publish, then DB rollback).",
      ["Correctness under retries/crashes", "No distributed transaction (2PC)", "Order per aggregate can be preserved"],
      ["Extra table and relay process", "Added latency", "Cleanup/retention of processed ids"],
      "Without idempotency, a re-delivered `PaymentCaptured` charges twice. Without an outbox, a crash between commit and send silently drops the event.",
      "Consumer: `INSERT INTO processed_events(event_id)`; duplicate-key => skip. Producer side: `orders` + `outbox(published=false)` in one transaction; poller `SELECT ... WHERE published=false ORDER BY id`, publish, then mark published.",
      [("Idempotency check", "sql", "insert into processed_events(event_id) values (?)  -- PK violation = duplicate"),
       ("Outbox row", "sql", "insert into outbox(aggregate_id, event_type, payload) values (?, 'OrderPlaced', ?)")],
      [("Why does the poller mark rows published AFTER sending?", "Crash between send and mark causes a duplicate (acceptable) rather than a lost event."),
       ("Why is the id check in the same transaction as the side effect?", "So a failed side effect does not leave the event marked as processed.")]),
]

day(46, "Kafka II: JSON Events, Dead Letters, Idempotency, and Outbox", "Microservices (Kafka)",
    "Versioned JSON event contracts, retry/DLT error handling, idempotent consumers and the transactional outbox pattern",
    ["Design versioned JSON events with a tolerant reader", "Configure retries and a dead-letter topic", "Make consumers idempotent with a processed-events table", "Explain and simulate the transactional outbox", "Reason about delivery guarantees"],
    ["Day 45 Kafka I", "Day 25-27 JDBC and transactions"],
    TOPICS, [j1, j2, j3, j4],
    [("At-least-once vs exactly-once?", "At-least-once may duplicate; exactly-once needs idempotent producers + transactions or idempotent consumers."),
     ("What is the dual-write problem?", "Updating a DB and a broker cannot be atomic; the outbox pattern fixes it."),
     ("How do you replay a DLT?", "Fix the cause, then re-publish the records to the original topic with a tool or replay job."),
     ("How do you evolve an event schema?", "Additive changes, tolerant readers, version field, support old and new versions during migration."),
     ("Why not 2PC across DB and Kafka?", "Poor availability and unsupported by Kafka; prefer eventual consistency patterns.")],
    ["Strict JSON deserialization.", "Infinite retries without DLT.", "Marking events processed before the side effect succeeded.", "Publishing to Kafka inside the DB transaction.", "Ignoring DLT monitoring."],
    ["Spring Kafka Reference: Handling Exceptions, Dead Letter", "Chris Richardson: Transactional Outbox pattern", "Confluent: schema evolution"],
    [("DLT", "Dead-letter topic"), ("Poison message", "Record that always fails"), ("Idempotent", "Safe to apply more than once"), ("Outbox", "Table of events to relay to the broker"),
     ("Tolerant reader", "Ignore unknown fields, default missing ones"), ("CDC", "Change data capture")],
    "2-3 h theory + 4-6 h tasks", spring=True)
