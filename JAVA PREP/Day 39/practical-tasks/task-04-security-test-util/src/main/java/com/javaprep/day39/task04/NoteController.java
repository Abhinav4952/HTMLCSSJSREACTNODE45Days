package com.javaprep.day39.task04;

import java.security.Principal;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class NoteController {

    @GetMapping("/me")
    public String me(Principal principal) {
        return principal.getName();
    }

    @PostMapping("/notes")
    @ResponseStatus(HttpStatus.CREATED)
    public String create() {
        return "created";
    }

    @GetMapping("/admin")
    public String admin() {
        return "admin";
    }
}
