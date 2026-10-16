package com.javaprep.day31.task02;

import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// TODO(Day31-task02): make this a global REST exception translator
public class ApiExceptionHandler {

    /** 404 problem: title "Not Found", detail = exception message. */
    // TODO(Day31-task02): register for ResourceNotFoundException
    public ProblemDetail notFound(ResourceNotFoundException ex) {
        // TODO(Day31-task02): ProblemDetail.forStatusAndDetail(NOT_FOUND, message) with title "Not Found"
        throw new UnsupportedOperationException("TODO(Day31-task02): ProblemDetail.forStatusAndDetail(NOT_FOUND, message) with title 'Not Found'");
    }

    /** 409 problem: title "Conflict", detail = exception message. */
    // TODO(Day31-task02): register for IllegalStateException
    public ProblemDetail conflict(IllegalStateException ex) {
        // TODO(Day31-task02): build a 409 ProblemDetail
        throw new UnsupportedOperationException("TODO(Day31-task02): build a 409 ProblemDetail");
    }

    /** 400 problem: title "Validation failed"; custom property "errors" = map field -> message. */
    // TODO(Day31-task02): register for MethodArgumentNotValidException
    public ProblemDetail invalid(MethodArgumentNotValidException ex) {
        // TODO(Day31-task02): collect field errors into a map and set it as property errors
        throw new UnsupportedOperationException("TODO(Day31-task02): collect field errors into a map and set it as property errors");
    }
}
