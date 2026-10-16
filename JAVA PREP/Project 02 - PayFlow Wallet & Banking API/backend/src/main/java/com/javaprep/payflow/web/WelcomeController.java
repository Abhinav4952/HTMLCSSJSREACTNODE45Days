package com.javaprep.payflow.web;

import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Public welcome/health-style endpoint used to verify that the application and its wiring are alive. */
@RestController
public class WelcomeController {

    @GetMapping("/")
    public Map<String, Object> welcome() {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("application", "PayFlow Wallet and Banking API");
        body.put("status", "UP");
        body.put("hint", "See PROJECT_INSTRUCTIONS.md for the API contract; /actuator/health reports database status");
        return body;
    }
}
