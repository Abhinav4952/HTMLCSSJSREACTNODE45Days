package com.javaprep.day20.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicReference;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(30)
class BoundedBufferTest {

    private static void awaitState(Thread t, Thread.State expected) throws InterruptedException {
        long deadline = System.nanoTime() + 5_000_000_000L;
        while (t.getState() != expected) {
            if (System.nanoTime() > deadline) {
                throw new AssertionError("thread never reached " + expected + " (was " + t.getState() + ")");
            }
            Thread.onSpinWait();
        }
    }

    @Test
    void r1_constructorValidation() {
        assertThatThrownBy(() -> new BoundedBuffer<String>(0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new BoundedBuffer<String>(-1)).isInstanceOf(IllegalArgumentException.class);
        BoundedBuffer<String> b = new BoundedBuffer<>(3);
        assertThat(b.capacity()).isEqualTo(3);
        assertThat(b.size()).isZero();
    }

    @Test
    void r2_fifoSingleThread() throws Exception {
        BoundedBuffer<Integer> b = new BoundedBuffer<>(3);
        b.put(1);
        b.put(2);
        b.put(3);
        assertThat(b.size()).isEqualTo(3);
        assertThat(b.take()).isEqualTo(1);
        b.put(4);
        assertThat(b.take()).isEqualTo(2);
        assertThat(b.take()).isEqualTo(3);
        assertThat(b.take()).isEqualTo(4);
        assertThat(b.size()).isZero();
    }

    @Test
    void r2_nullRejected() {
        BoundedBuffer<String> b = new BoundedBuffer<>(1);
        assertThatThrownBy(() -> b.put(null)).isInstanceOf(NullPointerException.class);
    }

    @Test
    void r3_takeBlocksUntilAnItemArrives() throws Exception {
        BoundedBuffer<String> b = new BoundedBuffer<>(2);
        AtomicReference<String> got = new AtomicReference<>();
        Thread consumer = new Thread(() -> {
            try {
                got.set(b.take());
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        consumer.start();
        awaitState(consumer, Thread.State.WAITING);
        assertThat(got.get()).isNull();
        b.put("hello");
        consumer.join(5_000);
        assertThat(consumer.isAlive()).isFalse();
        assertThat(got.get()).isEqualTo("hello");
    }

    @Test
    void r4_putBlocksWhileFull() throws Exception {
        BoundedBuffer<String> b = new BoundedBuffer<>(1);
        b.put("a");
        Thread producer = new Thread(() -> {
            try {
                b.put("b");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        producer.start();
        awaitState(producer, Thread.State.WAITING);
        assertThat(b.size()).isEqualTo(1);
        assertThat(b.take()).isEqualTo("a");
        producer.join(5_000);
        assertThat(producer.isAlive()).isFalse();
        assertThat(b.take()).isEqualTo("b");
    }

    @Test
    void r5_interruptWhileWaitingPropagates() throws Exception {
        BoundedBuffer<String> b = new BoundedBuffer<>(1);
        AtomicReference<Throwable> thrown = new AtomicReference<>();
        Thread consumer = new Thread(() -> {
            try {
                b.take();
            } catch (Throwable t) {
                thrown.set(t);
            }
        });
        consumer.start();
        awaitState(consumer, Thread.State.WAITING);
        consumer.interrupt();
        consumer.join(5_000);
        assertThat(consumer.isAlive()).isFalse();
        assertThat(thrown.get()).isInstanceOf(InterruptedException.class);
    }

    @Test
    void r6_producerConsumerTransfersEverythingInOrder() throws Exception {
        BoundedBuffer<Integer> b = new BoundedBuffer<>(3);
        int total = 10_000;
        List<Integer> received = new ArrayList<>();
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < total; i++) {
                    b.put(i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < total; i++) {
                    received.add(b.take());
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        producer.start();
        consumer.start();
        producer.join(20_000);
        consumer.join(20_000);
        assertThat(received).hasSize(total);
        for (int i = 0; i < total; i++) {
            assertThat(received.get(i)).isEqualTo(i);
        }
        assertThat(b.size()).isZero();
    }
}
