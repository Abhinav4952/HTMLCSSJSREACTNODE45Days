package com.javaprep.day40.task03.sample;

public class UserService {
    public String find(long id) {
        return "u" + id;
    }

    @Audited
    public void save(String name) {
    }

    public int count() {
        return 0;
    }
}
