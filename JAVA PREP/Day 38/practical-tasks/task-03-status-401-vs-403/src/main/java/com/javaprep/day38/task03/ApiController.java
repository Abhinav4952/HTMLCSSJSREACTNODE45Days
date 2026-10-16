package com.javaprep.day38.task03;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ApiController {

    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }

    @GetMapping("/api/hello")
    public String hello() {
        return "hello";
    }

    @GetMapping("/admin/stats")
    public String stats() {
        return "stats";
    }
}
