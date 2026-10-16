package com.javaprep.day40.task04;

import org.springframework.stereotype.Service;

@Service
public class PaymentService {

    private final CallRecorder recorder;

    public PaymentService(CallRecorder recorder) {
        this.recorder = recorder;
    }

    public String pay(String user) {
        recorder.add("pay:" + user);
        if ("bad".equals(user)) {
            throw new IllegalStateException("declined");
        }
        return "paid:" + user;
    }
}
