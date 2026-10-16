package com.javaprep.day37.task01;

import java.security.Principal;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED endpoints; your SecurityFilterChain decides who may call them. */
@RestController
public class DemoController {

    @GetMapping("/public/hello")
    public String hello() {
        return "hello";
    }

    @GetMapping("/api/me")
    public String me(Principal principal) {
        return principal.getName();
    }

    @GetMapping("/admin/stats")
    public Map<String, Integer> stats() {
        return Map.of("users", 42);
    }

    @PostMapping("/api/echo")
    public String echo(@RequestBody String body) {
        return body;
    }
}
