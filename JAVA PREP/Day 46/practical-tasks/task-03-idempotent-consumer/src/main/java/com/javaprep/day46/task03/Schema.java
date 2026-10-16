package com.javaprep.day46.task03;

/** PROVIDED. Table that remembers which events were already handled. */
public final class Schema {

    public static final String PROCESSED_EVENTS =
            "create table processed_events (event_id varchar(100) primary key, processed_at timestamp default current_timestamp)";

    private Schema() {
    }
}
