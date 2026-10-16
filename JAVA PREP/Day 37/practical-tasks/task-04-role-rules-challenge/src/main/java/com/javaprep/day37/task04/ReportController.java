package com.javaprep.day37.task04;

import java.util.List;
import java.util.Map;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED endpoints. */
@RestController
public class ReportController {

    @GetMapping("/api/reports")
    public List<String> reports() {
        return List.of("q1", "q2");
    }

    @GetMapping("/api/whoami")
    public Map<String, Object> whoami(Authentication authentication) {
        return Map.of("name", authentication.getName(),
                "authorities", authentication.getAuthorities().stream().map(Object::toString).sorted().toList());
    }

    @DeleteMapping("/api/reports/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable String id) {
    }

    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }
}
