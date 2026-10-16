package com.javaprep.day09.task04;

public class Account {

    private final String id;
    private final long balanceCents;

    public Account(String id, long balanceCents) {
        this.id = id;
        this.balanceCents = balanceCents;
    }

    public String id() {
        return id;
    }

    public long balanceCents() {
        return balanceCents;
    }

    /** Format: {@code Account[id=<id>, balanceCents=<balanceCents>]}. */
    // TODO(Day09-task04): implement per Javadoc
    @Override
    public String toString() {
        throw new UnsupportedOperationException("TODO(Day09-task04): implement toString");
    }
}
