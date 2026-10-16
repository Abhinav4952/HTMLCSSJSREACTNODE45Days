package com.javaprep.day39.task03;

import java.util.List;
import java.util.NoSuchElementException;
import org.springframework.stereotype.Service;

@Service
public class NotificationService {

    private final EmailGateway gateway;
    private final UserLookup users;

    public NotificationService(EmailGateway gateway, UserLookup users) {
        this.gateway = gateway;
        this.users = users;
    }

    /**
     * Blank/null message -> IllegalArgumentException BEFORE any collaborator is called.
     * Unknown user -> NoSuchElementException and the gateway is never called.
     * Otherwise send to the user's email; return the gateway's boolean. A GatewayException means false.
     */
    public boolean notifyUser(long userId, String message) {
        // TODO(Day39-task03): validate, look up the email, call the gateway, translate GatewayException to false
        throw new UnsupportedOperationException("TODO(Day39-task03): validate, look up the email, call the gateway, translate GatewayException to false");
    }

    /** Tries every id (unknown users and gateway failures are skipped, never abort the loop). Returns how many messages were accepted. */
    public int broadcast(List<Long> userIds, String message) {
        // TODO(Day39-task03): loop over ids, count successes, skip unknown users
        throw new UnsupportedOperationException("TODO(Day39-task03): loop over ids, count successes, skip unknown users");
                // skipped
    }
}
