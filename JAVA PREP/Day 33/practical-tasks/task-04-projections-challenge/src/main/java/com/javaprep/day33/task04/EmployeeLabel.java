package com.javaprep.day33.task04;

import org.springframework.beans.factory.annotation.Value;

/** Open projection computed with SpEL. */
public interface EmployeeLabel {
    @Value("#{target.name + ' (' + target.department + ')'}")
    String getLabel();
}
