package com.javaprep.day40.task03.sample.web;

import com.javaprep.day40.task03.sample.Audited;

public class UserController {
    public String get(long id) {
        return "u" + id;
    }

    // not audited on purpose
    public void save(String name) {
    }
}
