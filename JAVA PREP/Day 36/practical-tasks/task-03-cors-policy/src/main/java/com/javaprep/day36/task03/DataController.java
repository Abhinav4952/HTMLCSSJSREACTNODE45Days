package com.javaprep.day36.task03;

import java.util.Map;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DataController {

    @GetMapping("/api/data")
    public Map<String, String> data() {
        return Map.of("status", "ok");
    }

    @PostMapping("/api/data")
    public Map<String, String> create() {
        return Map.of("status", "created");
    }

    @DeleteMapping("/api/data/{id}")
    public void delete(@PathVariable long id) {
    }

    @GetMapping("/other")
    public String other() {
        return "other";
    }

    // TODO(Day36-task03): allow ANY origin for this single endpoint with @CrossOrigin(origins = "*")
    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }
}
