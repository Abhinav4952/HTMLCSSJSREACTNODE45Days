package com.javaprep.day33.task03;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Slice;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // TODO(Day33-task03): declare four methods:
    //  Page<Employee>  findByDepartment(String department, Pageable pageable)
    //  Slice<Employee> findByActiveTrue(Pageable pageable)
    //  native @Query: List<DeptCount> headcountNative()   select department as department, count(*) as headcount from employees group by department order by department
    //  native @Query with countQuery: Page<Employee> wellPaid(@Param("min") BigDecimal min, Pageable pageable)  rows of employees with salary >= :min
}
