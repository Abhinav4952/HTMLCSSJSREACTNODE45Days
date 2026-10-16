package com.javaprep.day31.task01;

/** Outgoing payload: never exposes the password. */
public record UserResponse(long id, String name, String email) {
}
