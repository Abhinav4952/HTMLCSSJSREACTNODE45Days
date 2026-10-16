package com.javaprep.day40.task02;

import org.springframework.stereotype.Service;

@Service
public class ReportService {

    @Timed
    public String build() throws InterruptedException {
        Thread.sleep(5);
        return "report";
    }

    @Timed
    public String explode() {
        throw new IllegalArgumentException("bad report");
    }

    public String untimed() {
        return "plain";
    }
}
