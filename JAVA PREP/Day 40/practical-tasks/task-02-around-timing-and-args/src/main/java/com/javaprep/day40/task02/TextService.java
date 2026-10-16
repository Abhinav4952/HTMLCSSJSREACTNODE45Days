package com.javaprep.day40.task02;

import org.springframework.stereotype.Service;

@Service
public class TextService {

    public String shout(String s) {
        return s.toUpperCase() + "!";
    }

    public String echo(String s) {
        return s;
    }

    public int twice(int n) {
        return n * 2;
    }
}
