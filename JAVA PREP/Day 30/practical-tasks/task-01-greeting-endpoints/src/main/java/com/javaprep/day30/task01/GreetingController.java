package com.javaprep.day30.task01;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// TODO(Day30-task01): annotate the class as a REST controller mapped under /api/greetings
public class GreetingController {

    /** GET /api/greetings/{name} -> "Hello, {name}!" (plain text). */
    // TODO(Day30-task01): add the GET mapping for /{name}
    public String greet(@PathVariable String name) {
        // TODO(Day30-task01): return "Hello, <name>!"
        throw new UnsupportedOperationException("TODO(Day30-task01): return 'Hello, <name>!'");
    }

    /** GET /api/greetings?name=Ann&times=3 -> "Hello, Ann! Hello, Ann! Hello, Ann!" (defaults: name=World, times=1). */
    // TODO(Day30-task01): add the GET mapping for the collection path (no path suffix)
    public String repeat(@RequestParam(defaultValue = "World") String name,
                         @RequestParam(defaultValue = "1") int times) {
        // TODO(Day30-task01): join `times` copies of the greeting with single spaces; times < 1 must produce an empty string
        throw new UnsupportedOperationException("TODO(Day30-task01): join `times` copies of the greeting with single spaces; times < 1 must produce an empty string");
    }
}
