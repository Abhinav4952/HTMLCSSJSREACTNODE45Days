# Day 45 — Kafka I: Producers, Consumers, and EmbeddedKafka

**Phase:** Microservices (Kafka)  
**Primary theme:** Topics, partitions, keys, offsets, consumer groups, KafkaTemplate and @KafkaListener, tested with EmbeddedKafka  
**Estimated study time:** 2-3 h theory + 4-6 h tasks  
**Related tasks:** `task-01-producer-kafka-template`, `task-02-listener-kafka-listener`, `task-03-keyed-partition-ordering`, `task-04-consumer-groups-challenge`  
**Instruction alignment:** Maps to Day 45 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Topics, partitions, keys, offsets, consumer groups, KafkaTemplate and @KafkaListener, tested with EmbeddedKafka. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Kafka fundamentals: topics, partitions, offsets, and keys
2. Producers with Spring Kafka: KafkaTemplate, serializers, acks
3. Consumers, groups, and @KafkaListener
4. Testing Kafka code with EmbeddedKafka
5. Interview corner, common mistakes, glossary

## Subtopics

### Kafka fundamentals: topics, partitions, offsets, and keys

#### What it is

Kafka is a distributed, append-only commit log. A **topic** is split into **partitions**; each record in a partition gets a monotonically increasing **offset**. The producer picks the partition from the record **key** (hash) or round-robin when the key is null. Records are retained by time/size, not deleted when read.

#### Why it exists / why it matters

A log lets many independent consumers read the same data at their own pace, replay history, and scale reads by partition. Keys give per-entity ordering without global ordering costs.

#### Pros and cons

**Pros**

- High throughput, horizontal scaling by partitions
- Durable and replayable
- Per-key ordering
- Decouples producers from consumers

**Cons / trade-offs**

- Ordering only within a partition
- Partition count is hard to change
- Operational complexity
- At-least-once delivery means duplicates are possible

#### What happens without it / when misused

Choosing a bad key (e.g. constant) creates a hot partition; null keys lose per-entity ordering; too few partitions cap consumer parallelism.

#### Syntax and rules

Producer: `kafkaTemplate.send(topic, key, value)`. Partition = `murmur2(key) % numPartitions`. Replication factor gives durability (`acks=all` + `min.insync.replicas`).

#### Examples

**Example 1 — Key choice**

```text
orders for customer 42 -> key "customer-42" -> always partition 1 -> ordered
```

**Example 2 — CLI (manual lab)**

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic orders.v1 --partitions 3
```

#### Quick checks

1. What guarantees ordering in Kafka?
2. Can two consumers of one group read the same partition?

### Producers with Spring Kafka: KafkaTemplate, serializers, acks

#### What it is

Spring Boot auto-configures a `KafkaTemplate<K,V>` from `spring.kafka.producer.*`. `send()` is asynchronous and returns a `CompletableFuture<SendResult>`. Important settings: `acks` (0/1/all), `retries`, `enable.idempotence`, `linger.ms`, `batch.size`, key/value serializers.

#### Why it exists / why it matters

Understanding the asynchronous send and acknowledgement levels decides whether you can lose messages and whether you can block a web thread.

#### Pros and cons

**Pros**

- Simple API
- Configurable durability/latency trade-off
- Callbacks for success/failure

**Cons / trade-offs**

- Async errors are easy to ignore
- `acks=all` increases latency

#### What happens without it / when misused

Fire-and-forget without checking the future silently loses messages when the broker is down; `acks=0` loses data on leader failure.

#### Syntax and rules

```java
kafkaTemplate.send("orders.v1", key, value)
    .whenComplete((result, ex) -> { if (ex != null) log.error("send failed", ex); });
```
```yaml
spring.kafka.producer:
  acks: all
  properties:
    enable.idempotence: true
```

#### Examples

**Example 1 — Blocking send in tests**

```java
RecordMetadata md = template.send(TOPIC, key, value).get(10, TimeUnit.SECONDS).getRecordMetadata();
```

#### Quick checks

1. What does acks=all mean?
2. Why use a callback?

### Consumers, groups, and @KafkaListener

#### What it is

A **consumer group** shares the work of a topic: each partition is assigned to exactly one consumer of the group; different groups each receive all records. `@KafkaListener(topics, groupId)` registers a listener container. Offsets are committed after processing (default: after each batch via the container).

#### Why it exists / why it matters

Groups give you both scaling (more consumers in one group) and fan-out (more groups). Offsets give you resume-after-restart semantics.

#### Pros and cons

**Pros**

- Declarative consumers
- Automatic rebalancing
- Offset management by the container

**Cons / trade-offs**

- Rebalances pause consumption
- At-least-once: handlers must tolerate duplicates
- Max consumers per group = partition count

#### What happens without it / when misused

A listener that throws forever blocks its partition (poison message); a wrong `auto-offset-reset` loses or replays data on first start.

#### Syntax and rules

```java
@KafkaListener(topics = "orders.v1", groupId = "audit")
void on(ConsumerRecord<String,String> r) { ... }
```
`auto.offset.reset=earliest|latest` applies only when the group has no committed offset.

#### Examples

**Example 1 — Fan-out**

```text
topic orders -> group billing (all records) + group shipping (all records)
```

**Example 2 — Competing consumers**

```text
group workers with 3 members, 3 partitions -> one partition each
```

#### Quick checks

1. What triggers a rebalance?
2. What is auto.offset.reset?

### Testing Kafka code with EmbeddedKafka

#### What it is

`spring-kafka-test` provides `@EmbeddedKafka`, an in-JVM broker started for the test class. `${spring.embedded.kafka.brokers}` holds its address; point `spring.kafka.bootstrap-servers` at it. `KafkaTestUtils` builds consumer/producer properties.

#### Why it exists / why it matters

Integration tests with a real broker catch serialization, partitioning and group behavior that mocks cannot. No Docker is needed.

#### Pros and cons

**Pros**

- Fast, self-contained
- Real Kafka semantics
- Works in CI

**Cons / trade-offs**

- Slower than unit tests (seconds)
- Async: tests need polling/timeouts

#### What happens without it / when misused

Mocking `KafkaTemplate` verifies only that you called `send`, not that bytes arrive or that ordering holds. Using `Thread.sleep` instead of polling makes tests flaky.

#### Syntax and rules

```java
@SpringBootTest(properties = "spring.kafka.bootstrap-servers=${spring.embedded.kafka.brokers}")
@EmbeddedKafka(partitions = 1, topics = "orders.v1")
@DirtiesContext
class MyTest { }
```

#### Examples

**Example 1 — Await pattern**

```java
boolean ok = received.awaitCount(3, Duration.ofSeconds(15));
```

#### Quick checks

1. How does the app find the embedded broker?
2. Why @DirtiesContext?

## Interview corner

**Q1. Kafka vs RabbitMQ?**

Kafka is a replayable partitioned log built for throughput and streaming; RabbitMQ is a broker with queues and routing, messages are removed when consumed.

**Q2. How do you scale consumers?**

Add consumers to the group up to the partition count.

**Q3. What delivery semantics does Kafka give?**

At-least-once by default; exactly-once with idempotent producers + transactions within Kafka.

**Q4. Why use keys?**

To get per-entity ordering and co-locate related events.

**Q5. What is a rebalance?**

Reassignment of partitions among group members.

## Common mistakes & debugging

- Ignoring the send future.
- Expecting global ordering.
- Using a constant key.
- Forgetting `earliest` in tests so the first messages are skipped.
- Sleeping instead of polling in tests.

## Further reading

- Apache Kafka documentation: Design
- Spring for Apache Kafka Reference
- Confluent: Kafka 101

## Glossary

| Term | Meaning |
|------|---------|
| Topic | Named log of records |
| Partition | Ordered shard of a topic |
| Offset | Position in a partition |
| Consumer group | Set of consumers sharing a topic's partitions |
| Broker | Kafka server |
| acks | Producer durability level |

## Answers

### Kafka fundamentals: topics, partitions, offsets, and keys

1. Records with the same key go to the same partition, and a partition is ordered.
2. No; a partition is assigned to one member of a group at a time.

### Producers with Spring Kafka: KafkaTemplate, serializers, acks

1. The leader waits for all in-sync replicas before acknowledging.
2. Because send() is asynchronous; failures arrive later.

### Consumers, groups, and @KafkaListener

1. A consumer joining/leaving/crashing or partition changes.
2. Where to start when no committed offset exists.

### Testing Kafka code with EmbeddedKafka

1. Through the `spring.embedded.kafka.brokers` property.
2. So each class gets a fresh context/broker and listeners do not leak across tests.
