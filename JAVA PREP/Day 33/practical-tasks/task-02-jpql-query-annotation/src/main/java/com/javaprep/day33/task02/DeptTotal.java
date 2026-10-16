package com.javaprep.day33.task02;

import java.math.BigDecimal;

/** Interface projection: aliases in the query must be 'department' and 'total'. */
public interface DeptTotal {
    String getDepartment();

    BigDecimal getTotal();
}
