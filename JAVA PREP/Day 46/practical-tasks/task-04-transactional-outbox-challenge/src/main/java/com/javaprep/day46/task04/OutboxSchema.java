package com.javaprep.day46.task04;

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
