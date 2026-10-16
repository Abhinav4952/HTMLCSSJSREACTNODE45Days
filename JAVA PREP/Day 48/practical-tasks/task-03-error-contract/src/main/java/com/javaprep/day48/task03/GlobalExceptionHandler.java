package com.javaprep.day48.task03;

import org.springframework.http.ProblemDetail;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * One consistent error contract (RFC 9457 ProblemDetail). Every response must set status, title (the HTTP reason
 * phrase, e.g. "Not Found") and detail.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /** 404, detail = exception message. */
    @ExceptionHandler(NotFoundException.class)
    public ProblemDetail handleNotFound(NotFoundException ex) {
        // TODO(Day48-task03): ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ...) + title
        throw new UnsupportedOperationException("TODO(Day48-task03): implement handleNotFound");
    }

    /** 403, detail = exception message. */
    @ExceptionHandler(ForbiddenException.class)
    public ProblemDetail handleForbidden(ForbiddenException ex) {
        // TODO(Day48-task03): 403 problem detail
        throw new UnsupportedOperationException("TODO(Day48-task03): implement handleForbidden");
    }

    /** 400, detail "Validation failed", property "errors" = map field name -> first message. */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        // TODO(Day48-task03): collect ex.getBindingResult().getFieldErrors() into a LinkedHashMap and setProperty("errors", map)
        throw new UnsupportedOperationException("TODO(Day48-task03): implement handleValidation");
    }

    /** 400, detail "Malformed request body" (never echo the parser message). */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ProblemDetail handleUnreadable(HttpMessageNotReadableException ex) {
        // TODO(Day48-task03): 400 problem detail
        throw new UnsupportedOperationException("TODO(Day48-task03): implement handleUnreadable");
    }

    /** 500, detail "Unexpected error" - NEVER include the exception message (it may contain secrets). Log it instead. */
    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnexpected(Exception ex) {
        // TODO(Day48-task03): log the exception, return a generic 500 problem detail
        throw new UnsupportedOperationException("TODO(Day48-task03): implement handleUnexpected");
    }
}
