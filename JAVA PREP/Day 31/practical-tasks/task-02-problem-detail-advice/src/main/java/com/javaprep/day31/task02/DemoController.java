package com.javaprep.day31.task02;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED controller whose failures your advice must translate (do not edit). */
@RestController
@RequestMapping("/api/demo")
public class DemoController {

    public record Payload(@NotBlank String title) {
    }

    @GetMapping("/missing/{id}")
    public String missing(@PathVariable long id) {
        throw new ResourceNotFoundException("Item " + id + " not found");
    }

    @GetMapping("/conflict")
    public String conflict() {
        throw new IllegalStateException("Already processed");
    }

    @PostMapping("/validate")
    public String validate(@Valid @RequestBody Payload payload) {
        return payload.title();
    }
}
