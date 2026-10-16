package com.javaprep.day41.task02;

import org.slf4j.MDC;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED: echoes the request id visible in the MDC while the request is handled. */
@RestController
public class EchoController {

    @GetMapping("/echo")
    public String echo() {
        return String.valueOf(MDC.get(RequestIdFilter.MDC_KEY));
    }
}
