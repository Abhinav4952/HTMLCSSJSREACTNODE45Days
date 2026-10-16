package com.javaprep.day33.task01;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // TODO(Day33-task01): declare DERIVED query methods (names matter!), the facade EmployeeQueries documents the contract:
    //   findByDepartment(String)                                 -> List<Employee>
    //   findByDepartmentAndActiveTrue(String)                    -> List<Employee>
    //   findBySalaryGreaterThanEqualOrderBySalaryDesc(BigDecimal) -> List<Employee>
    //   findByNameContainingIgnoreCase(String)                   -> List<Employee>
    //   countByDepartment(String)                                -> long
    //   existsByNameIgnoreCase(String)                           -> boolean
    //   findTop2ByOrderBySalaryDesc()                            -> List<Employee>
    //   findByHiredOnBetween(LocalDate, LocalDate)               -> List<Employee>
    //   deleteByActiveFalse()                                    -> long
}
