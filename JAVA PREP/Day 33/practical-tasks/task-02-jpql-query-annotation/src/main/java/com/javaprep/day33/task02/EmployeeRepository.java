package com.javaprep.day33.task02;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // TODO(Day33-task02): add four @Query methods (JPQL, named parameters):
    //  search(@Param("q") String q)              employees whose name contains q ignoring case (lower(...) like lower(concat('%', :q, '%'))), ordered by name
    //  aboveAverage()                             employees earning more than the average salary of everyone (subquery), ordered by name
    //  raise(@Param("dept") String, @Param("factor") BigDecimal) -> int   bulk UPDATE of salary = salary * factor for a department (@Modifying(clearAutomatically = true, flushAutomatically = true))
    //  payroll()                                  List<DeptTotal>: department and sum(salary) AS total grouped by department ordered by department
}
