package com.javaprep.day31.task03;

import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED web layer: depends ONLY on the service (never on the repository). */
@RestController
@RequestMapping("/api/todos")
public class TodoController {

    private final TodoService service;

    public TodoController(TodoService service) {
        this.service = service;
    }

    @PostMapping
    public TodoDto create(@RequestBody TodoDto body) {
        return service.create(body.title());
    }

    @PostMapping("/{id}/complete")
    public TodoDto complete(@PathVariable long id) {
        return service.complete(id);
    }

    @GetMapping
    public List<TodoDto> list(@RequestParam(defaultValue = "false") boolean onlyOpen) {
        return service.list(onlyOpen);
    }
}
