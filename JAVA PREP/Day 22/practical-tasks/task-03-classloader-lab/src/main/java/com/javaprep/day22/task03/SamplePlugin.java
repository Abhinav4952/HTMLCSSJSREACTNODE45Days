package com.javaprep.day22.task03;

/** Provided type: carries static state so class identity is observable. */
public class SamplePlugin {

    private static int counter;

    public String greet() {
        return "hello from plugin";
    }

    public int next() {
        return ++counter;
    }
}
