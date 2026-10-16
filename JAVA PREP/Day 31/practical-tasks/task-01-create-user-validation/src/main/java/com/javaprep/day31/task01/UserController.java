package com.javaprep.day31.task01;

import jakarta.validation.Valid;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final AtomicLong ids = new AtomicLong();

    /** POST /api/users -> 201 and a UserResponse (id from the counter); invalid payload -> 400 (automatic). */
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse create(
            // TODO(Day31-task01): trigger validation of the body with @Valid
            @RequestBody CreateUserRequest request) {
        // TODO(Day31-task01): build a UserResponse from the request (no password) using ids.incrementAndGet()
        throw new UnsupportedOperationException("TODO(Day31-task01): build a UserResponse from the request (no password) using ids.incrementAndGet()");
    }
}
