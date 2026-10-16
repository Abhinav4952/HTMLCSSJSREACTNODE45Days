# Day 46 — Kafka II: JSON Events, Dead Letters, Idempotency, and Outbox

**Phase:** Microservices (Kafka)  
**Primary theme:** Versioned JSON event contracts, retry/DLT error handling, idempotent consumers and the transactional outbox pattern  
**Estimated study time:** 2-3 h theory + 4-6 h tasks  
**Related tasks:** `task-01-json-event-contract`, `task-02-poison-message-dlt`, `task-03-idempotent-consumer`, `task-04-transactional-outbox-challenge`  
**Instruction alignment:** Maps to Day 46 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

Versioned JSON event contracts, retry/DLT error handling, idempotent consumers and the transactional outbox pattern. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. JSON events and schema evolution
2. Error handling, retries, and dead-letter topics
3. Idempotent consumers and the transactional outbox
4. Interview corner, common mistakes, glossary

## Subtopics

### JSON events and schema evolution

#### What it is

Events are facts published to a topic. JSON is the common serialization. A good event has an **id**, **type**, **version** and business payload; consumers follow the **tolerant reader** rule (ignore unknown fields, apply defaults for missing optional ones). Spring Kafka offers `JsonSerializer/JsonDeserializer`; many teams serialize explicitly with Jackson and keep Kafka values as Strings/bytes.

#### Why it exists / why it matters

Producers and consumers deploy independently, so the contract must evolve without breaking old consumers. Additive changes are safe; renames/removals need a new version.

#### Pros and cons

**Pros**

- Human-readable and tool-friendly
- Easy evolution with additive fields
- Language-neutral

**Cons / trade-offs**

- Larger than binary formats (Avro/Protobuf)
- No enforced schema without extra tooling (Schema Registry)

#### What happens without it / when misused

Strict deserialization (`FAIL_ON_UNKNOWN_PROPERTIES=true`) makes every new producer field an outage for old consumers; using Java class names as type headers couples services.

#### Syntax and rules

```java
ObjectMapper m = new ObjectMapper().configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
record OrderPlaced(int version, String orderId, String customerId, long amountCents) {}
```
Rules: add fields, never reuse names with new meaning, bump `version` for breaking changes, support N and N-1.

#### Examples

**Example 1 — Event envelope**

```json
{"eventId":"6c1f...","type":"OrderPlaced","version":1,"occurredAt":"2025-01-01T10:00:00Z","data":{"orderId":"o-1"}}
```

#### Quick checks

1. Which changes are backward compatible?
2. Why keep an event id?

### Error handling, retries, and dead-letter topics

#### What it is

Spring Kafka's `DefaultErrorHandler` retries a failed record according to a `BackOff`, then calls a recoverer. `DeadLetterPublishingRecoverer` publishes the failed record (with exception headers) to `<topic>.DLT`. Non-retryable exceptions (deserialization, validation) can be classified to skip retries.

#### Why it exists / why it matters

One poison message that always throws would otherwise block a partition forever (the container re-delivers it). A DLT isolates it for inspection and replay while healthy traffic continues.

#### Pros and cons

**Pros**

- Pipeline keeps flowing
- Failed data is preserved for analysis
- Retry policy is centralized

**Cons / trade-offs**

- Order across the failed record is relaxed
- DLT needs monitoring/alerting and a replay process
- Blocking retries delay the partition

#### What happens without it / when misused

No handler: default behavior retries a few times then logs and SKIPS (data loss). Infinite retry: partition blocked. DLT never monitored: silent data loss.

#### Syntax and rules

```java
@Bean DefaultErrorHandler errorHandler(KafkaTemplate<Object,Object> t) {
  var recoverer = new DeadLetterPublishingRecoverer(t);
  return new DefaultErrorHandler(recoverer, new FixedBackOff(1000L, 3L));
}
```
Use `ExponentialBackOff` for real systems; `addNotRetryableExceptions(...)` for permanent errors; `ErrorHandlingDeserializer` to survive bad bytes.

#### Examples

**Example 1 — Non-retryable**

```java
handler.addNotRetryableExceptions(IllegalArgumentException.class);
```

**Example 2 — DLT naming**

```text
payments.v1 -> payments.v1.DLT (same partition number)
```

#### Quick checks

1. What is a poison message?
2. Why must the DLT have enough partitions?

### Idempotent consumers and the transactional outbox

#### What it is

Kafka gives **at-least-once** delivery to consumers, so duplicates happen (rebalance, retry, producer retry). An **idempotent consumer** records processed event ids (primary key) in the same transaction as the side effect. The **transactional outbox** solves the dual-write problem: write business data and an outbox row in one local transaction; a poller/CDC relays the outbox to Kafka.

#### Why it exists / why it matters

You cannot atomically update a database and publish to Kafka. Without the outbox you either lose events (DB commit, then crash before publish) or publish phantom events (publish, then DB rollback).

#### Pros and cons

**Pros**

- Correctness under retries/crashes
- No distributed transaction (2PC)
- Order per aggregate can be preserved

**Cons / trade-offs**

- Extra table and relay process
- Added latency
- Cleanup/retention of processed ids

#### What happens without it / when misused

Without idempotency, a re-delivered `PaymentCaptured` charges twice. Without an outbox, a crash between commit and send silently drops the event.

#### Syntax and rules

Consumer: `INSERT INTO processed_events(event_id)`; duplicate-key => skip. Producer side: `orders` + `outbox(published=false)` in one transaction; poller `SELECT ... WHERE published=false ORDER BY id`, publish, then mark published.

#### Examples

**Example 1 — Idempotency check**

```sql
insert into processed_events(event_id) values (?)  -- PK violation = duplicate
```

**Example 2 — Outbox row**

```sql
insert into outbox(aggregate_id, event_type, payload) values (?, 'OrderPlaced', ?)
```

#### Quick checks

1. Why does the poller mark rows published AFTER sending?
2. Why is the id check in the same transaction as the side effect?

## Interview corner

**Q1. At-least-once vs exactly-once?**

At-least-once may duplicate; exactly-once needs idempotent producers + transactions or idempotent consumers.

**Q2. What is the dual-write problem?**

Updating a DB and a broker cannot be atomic; the outbox pattern fixes it.

**Q3. How do you replay a DLT?**

Fix the cause, then re-publish the records to the original topic with a tool or replay job.

**Q4. How do you evolve an event schema?**

Additive changes, tolerant readers, version field, support old and new versions during migration.

**Q5. Why not 2PC across DB and Kafka?**

Poor availability and unsupported by Kafka; prefer eventual consistency patterns.

## Common mistakes & debugging

- Strict JSON deserialization.
- Infinite retries without DLT.
- Marking events processed before the side effect succeeded.
- Publishing to Kafka inside the DB transaction.
- Ignoring DLT monitoring.

## Further reading

- Spring Kafka Reference: Handling Exceptions, Dead Letter
- Chris Richardson: Transactional Outbox pattern
- Confluent: schema evolution

## Glossary

| Term | Meaning |
|------|---------|
| DLT | Dead-letter topic |
| Poison message | Record that always fails |
| Idempotent | Safe to apply more than once |
| Outbox | Table of events to relay to the broker |
| Tolerant reader | Ignore unknown fields, default missing ones |
| CDC | Change data capture |

## Answers

### JSON events and schema evolution

1. Adding optional fields; removing or renaming is not.
2. For idempotent consumers and tracing.

### Error handling, retries, and dead-letter topics

1. A record that fails every time it is processed.
2. The recoverer publishes to the same partition number by default.

### Idempotent consumers and the transactional outbox

1. Crash between send and mark causes a duplicate (acceptable) rather than a lost event.
2. So a failed side effect does not leave the event marked as processed.
