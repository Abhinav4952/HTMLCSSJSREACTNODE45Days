package com.javaprep.peoplehub.leave.events;

import java.time.LocalDate;

/**
 * Contract of the Kafka event "LeaveApproved" (topic leave.approved.v1, key = employeeId). See docs/LEAVE_APPROVED_EVENT.md.
 * Fields may be ADDED in later versions; consumers must ignore unknown fields (tolerant reader).
 */
public record LeaveApprovedEvent(
        int version,
        String eventId,
        long leaveRequestId,
        long employeeId,
        long approverId,
        String leaveType,
        LocalDate startDate,
        LocalDate endDate,
        int days,
        String approvedAt) {
}
