package com.javaprep.day22.task04;

import java.lang.management.ManagementFactory;
import java.lang.management.ThreadInfo;
import java.lang.management.ThreadMXBean;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** jstack-style thread dump triage. */
public final class ThreadDumpAnalyzer {

    /** One parsed thread. */
    public record ThreadEntry(String name, String state, List<String> frames, String waitingForLock, List<String> heldLocks) {
    }

    private static final Pattern HEADER = Pattern.compile("^\"(.+?)\"\\s.*$");
    private static final Pattern STATE = Pattern.compile("^\\s*java\\.lang\\.Thread\\.State:\\s+(\\w+).*$");
    private static final Pattern FRAME = Pattern.compile("^\\s*at\\s+(.+?)\\s*$");
    private static final Pattern WAITING = Pattern.compile("^\\s*-\\s+waiting to lock\\s+<(0x[0-9a-fA-F]+)>.*$");
    private static final Pattern LOCKED = Pattern.compile("^\\s*-\\s+locked\\s+<(0x[0-9a-fA-F]+)>.*$");

    private ThreadDumpAnalyzer() {
    }

    public static List<ThreadEntry> parse(String dump) {
        // TODO(Day22-task04): iterate lines; a HEADER match starts a new thread (flush the previous one); STATE/FRAME/WAITING/LOCKED lines fill the current thread; lines before the first header are ignored; state defaults to UNKNOWN; null/blank dump -> empty list
        throw new UnsupportedOperationException("TODO(Day22-task04): parse");
    }

    public static Map<String, Long> countByState(List<ThreadEntry> threads) {
        // TODO(Day22-task04): sorted map (TreeMap) from state to the number of threads in that state
        throw new UnsupportedOperationException("TODO(Day22-task04): countByState");
    }

    public static Optional<String> hotspot(List<ThreadEntry> threads) {
        // TODO(Day22-task04): among RUNNABLE threads that have at least one frame count the first frame; return the most frequent (alphabetically first on ties) or Optional.empty()
        throw new UnsupportedOperationException("TODO(Day22-task04): hotspot");
    }

    public static Set<String> findDeadlock(List<ThreadEntry> threads) {
        // TODO(Day22-task04): map lock id -> holder thread; edge thread -> holder of its waitingForLock; follow edges from each thread, and when you revisit a thread on the current path return the names on the cycle (sorted); none -> empty set
        throw new UnsupportedOperationException("TODO(Day22-task04): findDeadlock");
    }

    public static List<String> liveDeadlockedThreads() {
        // TODO(Day22-task04): ThreadMXBean bean = ManagementFactory.getThreadMXBean(); long[] ids = bean.findDeadlockedThreads(); null -> empty list; otherwise the sorted thread names from bean.getThreadInfo(ids)
        throw new UnsupportedOperationException("TODO(Day22-task04): liveDeadlockedThreads");
    }
}
