package com.javaprep.day10.task04;

public sealed interface Result permits Result.Success, Result.Failure {

    record Success(String value) implements Result {}

    record Failure(String error) implements Result {}

    // TODO(Day10-task04): return new Success(value); null value throws IllegalArgumentException
    static Result ok(String value) {
        throw new UnsupportedOperationException("TODO(Day10-task04): implement ok");
    }

    // TODO(Day10-task04): return new Failure(error); null/blank error throws IllegalArgumentException
    static Result fail(String error) {
        throw new UnsupportedOperationException("TODO(Day10-task04): implement fail");
    }
}
