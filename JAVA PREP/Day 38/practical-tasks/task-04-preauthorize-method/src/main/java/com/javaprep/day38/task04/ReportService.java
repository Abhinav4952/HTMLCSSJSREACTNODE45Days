package com.javaprep.day38.task04;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;

@Service
public class ReportService {

    /** Only ADMIN. */
    // TODO(Day38-task04): restrict to ADMIN with @PreAuthorize("hasRole('ADMIN')")
    public String deleteAll() {
        return "deleted";
    }

    /** USER or ADMIN. */
    // TODO(Day38-task04): restrict with @PreAuthorize("hasAnyRole('USER','ADMIN')")
    public String view() {
        return "report";
    }

    /** The owner themself or an ADMIN (compare the `owner` argument with authentication.name). */
    // TODO(Day38-task04): restrict with @PreAuthorize("#owner == authentication.name or hasRole('ADMIN')")
    public String readFor(String owner) {
        return "report-of-" + owner;
    }
}
