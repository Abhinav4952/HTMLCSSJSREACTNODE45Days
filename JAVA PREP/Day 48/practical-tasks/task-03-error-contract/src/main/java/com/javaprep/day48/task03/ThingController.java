package com.javaprep.day48.task03;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED. Endpoints that deliberately fail in different ways. */
@RestController
@RequestMapping("/things")
public class ThingController {

    public record CreateThing(@NotBlank String name, @Min(1) int quantity) {
    }

    @GetMapping("/{id}")
    public Map<String, Object> get(@PathVariable long id) {
        if (id == 0) {
            throw new NotFoundException("thing 0 not found");
        }
        if (id == 403) {
            throw new ForbiddenException("not your thing");
        }
        if (id == 99) {
            throw new IllegalStateException("db password is hunter2");
        }
        return Map.of("id", id);
    }

    @PostMapping
    public Map<String, Object> create(@Valid @RequestBody CreateThing body) {
        return Map.of("name", body.name());
    }
}
