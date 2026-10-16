package com.javaprep.day47.task04;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED. Dummy endpoints used to verify the security rules. */
@RestController
public class ProbeController {

    @GetMapping("/public/ping")
    public String ping() {
        return "pong";
    }

    @PostMapping("/api/auth/login")
    public String login() {
        return "login";
    }

    @GetMapping("/api/projects")
    public String projects() {
        return "projects";
    }

    @PostMapping("/api/projects")
    public String createProject() {
        return "created";
    }

    @GetMapping("/api/admin/stats")
    public String stats() {
        return "stats";
    }
}
