package com.javaprep.day22.task04;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import java.util.concurrent.CyclicBarrier;
import java.util.concurrent.locks.ReentrantLock;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Timeout;

@Timeout(60)
class ThreadDumpAnalyzerTest {

    private static final String DUMP = """
            2026-10-16 18:00:00
            Full thread dump OpenJDK 64-Bit Server VM (21.0.5+11 mixed mode):

            "main" #1 [1234] prio=5 os_prio=31 cpu=45.2ms elapsed=10.3s tid=0x00007f1 nid=0x1c03 waiting on condition  [0x000070000]
               java.lang.Thread.State: TIMED_WAITING (sleeping)
            \tat java.lang.Thread.sleep(java.base@21.0.5/Native Method)
            \tat com.acme.Main.main(Main.java:10)

            "pool-1-thread-1" #21 [2001] prio=5 os_prio=31 tid=0x00007f2 nid=0x2003 runnable  [0x000070100]
               java.lang.Thread.State: RUNNABLE
            \tat com.acme.Hash.compute(Hash.java:77)
            \tat com.acme.Worker.run(Worker.java:12)

            "pool-1-thread-2" #22 [2002] prio=5 os_prio=31 tid=0x00007f3 nid=0x2004 runnable  [0x000070200]
               java.lang.Thread.State: RUNNABLE
            \tat com.acme.Hash.compute(Hash.java:77)
            \tat com.acme.Worker.run(Worker.java:12)

            "pool-1-thread-3" #23 [2003] prio=5 os_prio=31 tid=0x00007f4 nid=0x2005 runnable  [0x000070300]
               java.lang.Thread.State: RUNNABLE
            \tat com.acme.Parser.next(Parser.java:5)

            "transfer-A" #31 [3001] prio=5 os_prio=31 tid=0x00007f5 nid=0x3001 waiting for monitor entry  [0x000070400]
               java.lang.Thread.State: BLOCKED (on object monitor)
            \tat com.acme.Accounts.transfer(Accounts.java:42)
            \t- waiting to lock <0x000000076ab62208> (a java.lang.Object)
            \t- locked <0x000000076ab62218> (a java.lang.Object)

            "transfer-B" #32 [3002] prio=5 os_prio=31 tid=0x00007f6 nid=0x3002 waiting for monitor entry  [0x000070500]
               java.lang.Thread.State: BLOCKED (on object monitor)
            \tat com.acme.Accounts.transfer(Accounts.java:42)
            \t- waiting to lock <0x000000076ab62218> (a java.lang.Object)
            \t- locked <0x000000076ab62208> (a java.lang.Object)

            "innocent-waiter" #33 [3003] prio=5 os_prio=31 tid=0x00007f7 nid=0x3003 waiting for monitor entry  [0x000070600]
               java.lang.Thread.State: BLOCKED (on object monitor)
            \tat com.acme.Accounts.audit(Accounts.java:90)
            \t- waiting to lock <0x000000076ab62208> (a java.lang.Object)
            """;

    private static String dumpOf(String... blocks) {
        return String.join("\n\n", blocks);
    }

    private static String thread(String name, String waiting, String... held) {
        StringBuilder sb = new StringBuilder("\"" + name + "\" #1 prio=5 nid=0x1 blocked\n   java.lang.Thread.State: BLOCKED (on object monitor)\n\tat com.acme.X.y(X.java:1)\n");
        if (waiting != null) {
            sb.append("\t- waiting to lock <").append(waiting).append("> (a java.lang.Object)\n");
        }
        for (String h : held) {
            sb.append("\t- locked <").append(h).append("> (a java.lang.Object)\n");
        }
        return sb.toString();
    }

    @Test
    void r1_parseExtractsThreadsInOrder() {
        List<ThreadDumpAnalyzer.ThreadEntry> threads = ThreadDumpAnalyzer.parse(DUMP);
        assertThat(threads).extracting(ThreadDumpAnalyzer.ThreadEntry::name)
                .containsExactly("main", "pool-1-thread-1", "pool-1-thread-2", "pool-1-thread-3", "transfer-A", "transfer-B", "innocent-waiter");
        ThreadDumpAnalyzer.ThreadEntry main = threads.get(0);
        assertThat(main.state()).isEqualTo("TIMED_WAITING");
        assertThat(main.frames()).containsExactly("java.lang.Thread.sleep(java.base@21.0.5/Native Method)", "com.acme.Main.main(Main.java:10)");
        assertThat(main.waitingForLock()).isNull();
        assertThat(main.heldLocks()).isEmpty();
    }

    @Test
    void r1_parseReadsLocks() {
        List<ThreadDumpAnalyzer.ThreadEntry> threads = ThreadDumpAnalyzer.parse(DUMP);
        ThreadDumpAnalyzer.ThreadEntry a = threads.get(4);
        assertThat(a.state()).isEqualTo("BLOCKED");
        assertThat(a.waitingForLock()).isEqualTo("0x000000076ab62208");
        assertThat(a.heldLocks()).containsExactly("0x000000076ab62218");
        assertThat(threads.get(6).heldLocks()).isEmpty();
    }

    @Test
    void r1_parseHandlesEmptyAndNoise() {
        assertThat(ThreadDumpAnalyzer.parse("")).isEmpty();
        assertThat(ThreadDumpAnalyzer.parse(null)).isEmpty();
        assertThat(ThreadDumpAnalyzer.parse("Full thread dump\nnothing quoted here")).isEmpty();
        List<ThreadDumpAnalyzer.ThreadEntry> bare = ThreadDumpAnalyzer.parse("\"lonely\" #5 prio=5\n");
        assertThat(bare).hasSize(1);
        assertThat(bare.get(0).state()).isEqualTo("UNKNOWN");
        assertThat(bare.get(0).frames()).isEmpty();
    }

    @Test
    void r2_countByStateIsSorted() {
        var counts = ThreadDumpAnalyzer.countByState(ThreadDumpAnalyzer.parse(DUMP));
        assertThat(counts).containsExactly(
                java.util.Map.entry("BLOCKED", 3L),
                java.util.Map.entry("RUNNABLE", 3L),
                java.util.Map.entry("TIMED_WAITING", 1L));
        assertThat(ThreadDumpAnalyzer.countByState(List.of())).isEmpty();
    }

    @Test
    void r3_hotspotIsTheMostCommonRunnableTopFrame() {
        assertThat(ThreadDumpAnalyzer.hotspot(ThreadDumpAnalyzer.parse(DUMP))).contains("com.acme.Hash.compute(Hash.java:77)");
        assertThat(ThreadDumpAnalyzer.hotspot(ThreadDumpAnalyzer.parse(thread("t", null)))).as("only BLOCKED threads").isEmpty();
        assertThat(ThreadDumpAnalyzer.hotspot(List.of())).isEmpty();
    }

    @Test
    void r3_hotspotTieBreaksAlphabetically() {
        String dump = "\"a\" #1 x\n   java.lang.Thread.State: RUNNABLE\n\tat zeta.Z.run(Z.java:1)\n\n"
                + "\"b\" #2 x\n   java.lang.Thread.State: RUNNABLE\n\tat alpha.A.run(A.java:1)\n";
        assertThat(ThreadDumpAnalyzer.hotspot(ThreadDumpAnalyzer.parse(dump))).contains("alpha.A.run(A.java:1)");
    }

    @Test
    void r4_findsTheTwoThreadDeadlockButNotTheInnocentWaiter() {
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(DUMP))).containsExactly("transfer-A", "transfer-B");
    }

    @Test
    void r4_findsAThreeThreadCycle() {
        String dump = dumpOf(thread("t1", "0xB", "0xA"), thread("t2", "0xC", "0xB"), thread("t3", "0xA", "0xC"), thread("bystander", "0xA"));
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(dump))).containsExactly("t1", "t2", "t3");
    }

    @Test
    void r4_aBlockedChainIsNotADeadlock() {
        String dump = dumpOf(thread("t1", "0xB", "0xA"), thread("t2", null, "0xB"));
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(dump))).isEmpty();
        assertThat(ThreadDumpAnalyzer.findDeadlock(ThreadDumpAnalyzer.parse(thread("t", "0xZ")))).as("lock held by nobody").isEmpty();
        assertThat(ThreadDumpAnalyzer.findDeadlock(List.of())).isEmpty();
    }

    @Test
    void r5_liveDeadlockIsDetectedFromInsideTheJvm() throws Exception {
        assertThat(ThreadDumpAnalyzer.liveDeadlockedThreads()).isEmpty();
        ReentrantLock a = new ReentrantLock();
        ReentrantLock b = new ReentrantLock();
        CyclicBarrier bothHoldFirstLock = new CyclicBarrier(2);
        Thread t1 = deadlocker("dl-1", a, b, bothHoldFirstLock);
        Thread t2 = deadlocker("dl-2", b, a, bothHoldFirstLock);
        try {
            t1.start();
            t2.start();
            List<String> found = List.of();
            long deadline = System.nanoTime() + 20_000_000_000L;
            while (System.nanoTime() < deadline) {
                found = ThreadDumpAnalyzer.liveDeadlockedThreads();
                if (!found.isEmpty()) {
                    break;
                }
                Thread.sleep(50);
            }
            assertThat(found).containsExactly("dl-1", "dl-2");
        } finally {
            t1.interrupt();
            t2.interrupt();
            t1.join(5_000);
            t2.join(5_000);
        }
        assertThat(ThreadDumpAnalyzer.liveDeadlockedThreads()).as("cleaned up").isEmpty();
    }

    private static Thread deadlocker(String name, ReentrantLock first, ReentrantLock second, CyclicBarrier barrier) {
        Thread t = new Thread(() -> {
            first.lock();
            try {
                barrier.await();
                second.lockInterruptibly();
                second.unlock();
            } catch (Exception interruptedOrBroken) {
                // the test interrupts us to clean up
            } finally {
                first.unlock();
            }
        }, name);
        t.setDaemon(true);
        return t;
    }
}
