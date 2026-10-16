package com.javaprep.day23.task02;

/** Provided collaborator: customer notifications. */
public interface NotificationSender {

    void send(String customerId, String message);
}
