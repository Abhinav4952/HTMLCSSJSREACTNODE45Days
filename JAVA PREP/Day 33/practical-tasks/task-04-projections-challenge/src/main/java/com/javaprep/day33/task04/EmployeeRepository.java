package com.javaprep.day33.task04;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    // TODO(Day33-task04): declare:
    //  List<EmployeeSummary> findByActiveTrueOrderByName()
    //  List<EmployeeLabel>   findByDepartmentOrderByName(String department)
    //  JPQL constructor expression -> List<EmployeeRow> rowsOf(@Param("dept") String dept): select new com.javaprep.day33.task04.EmployeeRow(e.name, e.salary) from Employee e where e.department = :dept order by e.salary desc
    //  dynamic projection: <T> List<T> findByDepartmentOrderByNameAsc(String department, Class<T> type)
}
