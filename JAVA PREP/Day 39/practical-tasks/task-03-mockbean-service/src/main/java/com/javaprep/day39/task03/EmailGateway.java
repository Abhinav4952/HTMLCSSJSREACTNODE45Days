package com.javaprep.day39.task03;

public interface EmailGateway {
    /** Returns true when the provider accepted the message. May throw GatewayException. */
    boolean send(String to, String body);
}
