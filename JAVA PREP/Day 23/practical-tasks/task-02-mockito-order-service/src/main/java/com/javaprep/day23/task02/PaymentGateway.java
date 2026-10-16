package com.javaprep.day23.task02;

/** Provided collaborator: charges and refunds payments. */
public interface PaymentGateway {

    /** Result of a charge attempt. */
    record PaymentResult(boolean success, String paymentId) {
    }

    PaymentResult charge(String customerId, long amountCents);

    void refund(String paymentId);
}
