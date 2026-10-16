from sx import *

S = ["spring-boot-starter-data-jpa"]
DEPS = [H2]

EMP = r'''package %PKG%;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;
import java.time.LocalDate;

@Entity
@Table(name = "employees")
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String department;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal salary;

    @Column(nullable = false)
    private boolean active;

    @Column(name = "hired_on", nullable = false)
    private LocalDate hiredOn;

    protected Employee() {
    }

    public Employee(String name, String department, String salary, boolean active, String hiredOn) {
        this.name = name;
        this.department = department;
        this.salary = new BigDecimal(salary);
        this.active = active;
        this.hiredOn = LocalDate.parse(hiredOn);
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDepartment() {
        return department;
    }

    public BigDecimal getSalary() {
        return salary;
    }

    public boolean isActive() {
        return active;
    }

    public LocalDate getHiredOn() {
        return hiredOn;
    }
}
'''

SEED = r'''    @BeforeEach
    void seed() {
        repository.saveAll(List.of(
                new Employee("Ann", "Eng", "100", true, "2020-01-10"),
                new Employee("Bob", "Eng", "80", true, "2021-05-01"),
                new Employee("Cid", "Eng", "60", false, "2019-03-03"),
                new Employee("Dee", "Ops", "70", true, "2022-07-07"),
                new Employee("Eve", "Ops", "50", true, "2018-02-02"),
                new Employee("Fay", "HR", "40", false, "2023-09-09")));
        repository.flush();
    }
'''

# ------------------------------------------------------------ task 1
REPO1 = r'''package %PKG%;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    //A! declare DERIVED query methods (names matter!), the facade EmployeeQueries documents the contract:
    //   findByDepartment(String)                                 -> List<Employee>
    //   findByDepartmentAndActiveTrue(String)                    -> List<Employee>
    //   findBySalaryGreaterThanEqualOrderBySalaryDesc(BigDecimal) -> List<Employee>
    //   findByNameContainingIgnoreCase(String)                   -> List<Employee>
    //   countByDepartment(String)                                -> long
    //   existsByNameIgnoreCase(String)                           -> boolean
    //   findTop2ByOrderBySalaryDesc()                            -> List<Employee>
    //   findByHiredOnBetween(LocalDate, LocalDate)               -> List<Employee>
    //   deleteByActiveFalse()                                    -> long
    List<Employee> findByDepartment(String department);

    List<Employee> findByDepartmentAndActiveTrue(String department);

    List<Employee> findBySalaryGreaterThanEqualOrderBySalaryDesc(BigDecimal min);

    List<Employee> findByNameContainingIgnoreCase(String fragment);

    long countByDepartment(String department);

    boolean existsByNameIgnoreCase(String name);

    List<Employee> findTop2ByOrderBySalaryDesc();

    List<Employee> findByHiredOnBetween(LocalDate from, LocalDate to);

    long deleteByActiveFalse();
    //E!
}
'''
FAC1 = r'''package %PKG%;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

/** Facade the tests call. Each method must delegate to ONE derived query on the repository. */
@Component
public class EmployeeQueries {

    private final EmployeeRepository repository;

    public EmployeeQueries(EmployeeRepository repository) {
        this.repository = repository;
    }

    public List<Employee> inDepartment(String department) {
        //B! delegate to findByDepartment
        return repository.findByDepartment(department);
        //E!
    }

    public List<Employee> activeIn(String department) {
        //B! delegate to findByDepartmentAndActiveTrue
        return repository.findByDepartmentAndActiveTrue(department);
        //E!
    }

    /** Highest salary first. */
    public List<Employee> earningAtLeast(BigDecimal min) {
        //B! delegate to findBySalaryGreaterThanEqualOrderBySalaryDesc
        return repository.findBySalaryGreaterThanEqualOrderBySalaryDesc(min);
        //E!
    }

    public List<Employee> nameContains(String fragment) {
        //B! delegate to findByNameContainingIgnoreCase
        return repository.findByNameContainingIgnoreCase(fragment);
        //E!
    }

    public long headcount(String department) {
        //B! delegate to countByDepartment
        return repository.countByDepartment(department);
        //E!
    }

    public boolean nameTaken(String name) {
        //B! delegate to existsByNameIgnoreCase
        return repository.existsByNameIgnoreCase(name);
        //E!
    }

    public List<Employee> topTwoPaid() {
        //B! delegate to findTop2ByOrderBySalaryDesc
        return repository.findTop2ByOrderBySalaryDesc();
        //E!
    }

    /** Inclusive on both ends. */
    public List<Employee> hiredBetween(LocalDate from, LocalDate to) {
        //B! delegate to findByHiredOnBetween
        return repository.findByHiredOnBetween(from, to);
        //E!
    }

    @Transactional
    public long purgeInactive() {
        //B! delegate to deleteByActiveFalse and return the number of deleted rows
        return repository.deleteByActiveFalse();
        //E!
    }
}
'''
T1 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(EmployeeQueries.class)
class DerivedQueriesTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeeQueries queries;

''' + SEED + r'''
    private static List<String> names(List<Employee> list) {
        return list.stream().map(Employee::getName).toList();
    }

    @Test
    void byDepartment() {
        assertThat(names(queries.inDepartment("Eng"))).containsExactlyInAnyOrder("Ann", "Bob", "Cid");
        assertThat(queries.inDepartment("Nope")).isEmpty();
    }

    @Test
    void byDepartmentAndActive() {
        assertThat(names(queries.activeIn("Eng"))).containsExactlyInAnyOrder("Ann", "Bob");
    }

    @Test
    void salaryThresholdOrderedDescending() {
        assertThat(names(queries.earningAtLeast(new BigDecimal("70")))).containsExactly("Ann", "Bob", "Dee");
    }

    @Test
    void nameContainsIgnoresCase() {
        assertThat(names(queries.nameContains("E"))).containsExactlyInAnyOrder("Dee", "Eve");
    }

    @Test
    void countAndExists() {
        assertThat(queries.headcount("Ops")).isEqualTo(2);
        assertThat(queries.nameTaken("aNN")).isTrue();
        assertThat(queries.nameTaken("Zed")).isFalse();
    }

    @Test
    void topTwo() {
        assertThat(names(queries.topTwoPaid())).containsExactly("Ann", "Bob");
    }

    @Test
    void hiredBetweenIsInclusive() {
        assertThat(names(queries.hiredBetween(LocalDate.parse("2019-03-03"), LocalDate.parse("2021-05-01"))))
                .containsExactlyInAnyOrder("Cid", "Ann", "Bob");
    }

    @Test
    void purgeInactiveReturnsCount() {
        assertThat(queries.purgeInactive()).isEqualTo(2);
        assertThat(repository.count()).isEqualTo(4);
    }
}
'''
PROPS = lambda n: {"tres/application.properties": h2props("33", str(n))}
a1 = tk("derived-query-methods", "Derived Query Methods", "Warm-up",
    "Express queries purely through repository method names: And, Containing, IgnoreCase, OrderBy, Top, Between, count/exists/delete.",
    {"main/Application.java": APP, "main/Employee.java": EMP, "main/EmployeeRepository.java": REPO1, "main/EmployeeQueries.java": FAC1},
    {"test/DerivedQueriesTest.java": T1, **PROPS(1)},
    ["Declare nine derived query methods on `EmployeeRepository` (names are listed in the TODO).", "Implement every `EmployeeQueries` method as a delegate."],
    ["`Between` is inclusive on both bounds.", "Derived delete methods need a transaction; the facade method is `@Transactional`.", "A misspelled property name makes the context fail at startup."],
    ["Property names come from the entity fields (`hiredOn`, not `hired_on`).", "`Top2` limits the result count; combine with `OrderBy...Desc`."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 2
DEPT_TOTAL = "package %PKG%;\n\nimport java.math.BigDecimal;\n\n/** Interface projection: aliases in the query must be 'department' and 'total'. */\npublic interface DeptTotal {\n    String getDepartment();\n\n    BigDecimal getTotal();\n}\n"
REPO2 = r'''package %PKG%;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    //A! add four @Query methods (JPQL, named parameters):
    //  search(@Param("q") String q)              employees whose name contains q ignoring case (lower(...) like lower(concat('%', :q, '%'))), ordered by name
    //  aboveAverage()                             employees earning more than the average salary of everyone (subquery), ordered by name
    //  raise(@Param("dept") String, @Param("factor") BigDecimal) -> int   bulk UPDATE of salary = salary * factor for a department (@Modifying(clearAutomatically = true, flushAutomatically = true))
    //  payroll()                                  List<DeptTotal>: department and sum(salary) AS total grouped by department ordered by department
    @Query("select e from Employee e where lower(e.name) like lower(concat('%', :q, '%')) order by e.name")
    List<Employee> search(@Param("q") String q);

    @Query("select e from Employee e where e.salary > (select avg(x.salary) from Employee x) order by e.name")
    List<Employee> aboveAverage();

    @Modifying(clearAutomatically = true, flushAutomatically = true)
    @Query("update Employee e set e.salary = e.salary * :factor where e.department = :dept")
    int raise(@Param("dept") String dept, @Param("factor") BigDecimal factor);

    @Query("select e.department as department, sum(e.salary) as total from Employee e group by e.department order by e.department")
    List<DeptTotal> payroll();
    //E!
}
'''
FAC2 = r'''package %PKG%;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
public class EmployeeReports {

    private final EmployeeRepository repository;

    public EmployeeReports(EmployeeRepository repository) {
        this.repository = repository;
    }

    public List<Employee> search(String q) {
        //B! delegate to repository.search
        return repository.search(q);
        //E!
    }

    public List<Employee> aboveAverage() {
        //B! delegate to repository.aboveAverage
        return repository.aboveAverage();
        //E!
    }

    /** @return number of employees updated */
    @Transactional
    public int giveRaise(String department, BigDecimal factor) {
        //B! delegate to repository.raise
        return repository.raise(department, factor);
        //E!
    }

    public List<DeptTotal> payroll() {
        //B! delegate to repository.payroll
        return repository.payroll();
        //E!
    }
}
'''
T2 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(EmployeeReports.class)
class JpqlQueriesTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeeReports reports;

''' + SEED + r'''
    @Test
    void searchIgnoresCaseAndOrdersByName() {
        assertThat(reports.search("E")).extracting(Employee::getName).containsExactly("Dee", "Eve");
        assertThat(reports.search("zzz")).isEmpty();
    }

    @Test
    void aboveAverageUsesSubquery() {
        // average is 66.666...
        assertThat(reports.aboveAverage()).extracting(Employee::getName).containsExactly("Ann", "Bob", "Dee");
    }

    @Test
    void bulkRaiseUpdatesRowsAndRefreshesContext() {
        int updated = reports.giveRaise("Ops", new BigDecimal("1.10"));
        assertThat(updated).isEqualTo(2);
        List<Employee> ops = repository.findAll().stream().filter(e -> e.getDepartment().equals("Ops")).toList();
        assertThat(ops).extracting(Employee::getSalary).usingComparatorForType(BigDecimal::compareTo, BigDecimal.class)
                .containsExactlyInAnyOrder(new BigDecimal("77.00"), new BigDecimal("55.00"));
    }

    @Test
    void raiseForUnknownDepartmentUpdatesNothing() {
        assertThat(reports.giveRaise("Nope", new BigDecimal("2"))).isZero();
    }

    @Test
    void payrollGroupsByDepartment() {
        List<DeptTotal> totals = reports.payroll();
        assertThat(totals).extracting(DeptTotal::getDepartment).containsExactly("Eng", "HR", "Ops");
        assertThat(totals.get(0).getTotal()).isEqualByComparingTo("240");
        assertThat(totals.get(2).getTotal()).isEqualByComparingTo("120");
    }
}
'''
a2 = tk("jpql-query-annotation", "JPQL with @Query", "Core",
    "Write JPQL by hand: LIKE search, a subquery, a bulk @Modifying update, and an aggregate returned through an interface projection.",
    {"main/Application.java": APP, "main/Employee.java": EMP, "main/DeptTotal.java": DEPT_TOTAL, "main/EmployeeRepository.java": REPO2, "main/EmployeeReports.java": FAC2},
    {"test/JpqlQueriesTest.java": T2, **PROPS(2)},
    ["Add four `@Query` methods to `EmployeeRepository` (see the TODO for contracts).", "Implement the four delegating methods in `EmployeeReports`."],
    ["JPQL uses entity/field names (`Employee`, `hiredOn`), not table/column names.", "Bulk updates bypass the persistence context: use `clearAutomatically`.", "Aliases in aggregate queries must match projection getter names."],
    ["`:name` parameters pair with `@Param(\"name\")`.", "`avg(x.salary)` in a subquery needs a different alias than the outer query."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 3
DEPT_COUNT = "package %PKG%;\n\n/** Projection for the native query (aliases: department, headcount). */\npublic interface DeptCount {\n    String getDepartment();\n\n    long getHeadcount();\n}\n"
REPO3 = r'''package %PKG%;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Slice;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    //A! declare four methods:
    //  Page<Employee>  findByDepartment(String department, Pageable pageable)
    //  Slice<Employee> findByActiveTrue(Pageable pageable)
    //  native @Query: List<DeptCount> headcountNative()   select department as department, count(*) as headcount from employees group by department order by department
    //  native @Query with countQuery: Page<Employee> wellPaid(@Param("min") BigDecimal min, Pageable pageable)  rows of employees with salary >= :min
    Page<Employee> findByDepartment(String department, Pageable pageable);

    Slice<Employee> findByActiveTrue(Pageable pageable);

    @Query(value = "select department as department, count(*) as headcount from employees group by department order by department", nativeQuery = true)
    List<DeptCount> headcountNative();

    @Query(value = "select * from employees where salary >= :min order by id",
            countQuery = "select count(*) from employees where salary >= :min", nativeQuery = true)
    Page<Employee> wellPaid(@Param("min") BigDecimal min, Pageable pageable);
    //E!
}
'''
FAC3 = r'''package %PKG%;

import java.math.BigDecimal;
import java.util.List;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Slice;
import org.springframework.stereotype.Component;

@Component
public class EmployeePaging {

    private final EmployeeRepository repository;

    public EmployeePaging(EmployeeRepository repository) {
        this.repository = repository;
    }

    public Page<Employee> department(String department, Pageable pageable) {
        //B! delegate to findByDepartment
        return repository.findByDepartment(department, pageable);
        //E!
    }

    public Slice<Employee> activeSlice(Pageable pageable) {
        //B! delegate to findByActiveTrue
        return repository.findByActiveTrue(pageable);
        //E!
    }

    public List<DeptCount> headcounts() {
        //B! delegate to headcountNative
        return repository.headcountNative();
        //E!
    }

    public Page<Employee> wellPaid(BigDecimal min, Pageable pageable) {
        //B! delegate to wellPaid
        return repository.wellPaid(min, pageable);
        //E!
    }

    /** Human readable summary for a page, e.g. "page 2/3 (5 items total)" for page index 1. */
    public static String describe(Page<?> page) {
        //B! return page <number+1>/<totalPages> (<totalElements> items total)
        return "page " + (page.getNumber() + 1) + "/" + page.getTotalPages() + " (" + page.getTotalElements() + " items total)";
        //E!
    }
}
'''
T3 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.math.BigDecimal;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Slice;
import org.springframework.data.domain.Sort;

@DataJpaTest
@Import(EmployeePaging.class)
class PagingAndNativeTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeePaging paging;

''' + SEED + r'''
    @Test
    void firstPageSortedBySalaryDescending() {
        Page<Employee> p = paging.department("Eng", PageRequest.of(0, 2, Sort.by("salary").descending()));
        assertThat(p.getContent()).extracting(Employee::getName).containsExactly("Ann", "Bob");
        assertThat(p.getTotalElements()).isEqualTo(3);
        assertThat(p.getTotalPages()).isEqualTo(2);
        assertThat(p.hasNext()).isTrue();
    }

    @Test
    void lastPage() {
        Page<Employee> p = paging.department("Eng", PageRequest.of(1, 2, Sort.by("salary").descending()));
        assertThat(p.getContent()).extracting(Employee::getName).containsExactly("Cid");
        assertThat(p.isLast()).isTrue();
    }

    @Test
    void sliceKnowsOnlyWhetherThereIsMore() {
        Slice<Employee> s = paging.activeSlice(PageRequest.of(0, 3, Sort.by("name")));
        assertThat(s.getContent()).extracting(Employee::getName).containsExactly("Ann", "Bob", "Dee");
        assertThat(s.hasNext()).isTrue();
        assertThat(paging.activeSlice(PageRequest.of(1, 3, Sort.by("name"))).hasNext()).isFalse();
    }

    @Test
    void nativeAggregateThroughProjection() {
        List<DeptCount> counts = paging.headcounts();
        assertThat(counts).extracting(DeptCount::getDepartment).containsExactly("Eng", "HR", "Ops");
        assertThat(counts).extracting(DeptCount::getHeadcount).containsExactly(3L, 1L, 2L);
    }

    @Test
    void nativePagedQueryUsesCountQuery() {
        Page<Employee> p = paging.wellPaid(new BigDecimal("60"), PageRequest.of(0, 3));
        assertThat(p.getTotalElements()).isEqualTo(4);
        assertThat(p.getContent()).hasSize(3);
        assertThat(paging.wellPaid(new BigDecimal("60"), PageRequest.of(1, 3)).getContent()).hasSize(1);
    }

    @Test
    void describeFormatsPageInfo() {
        Page<Employee> p = paging.department("Eng", PageRequest.of(1, 2));
        assertThat(EmployeePaging.describe(p)).isEqualTo("page 2/2 (3 items total)");
    }
}
'''
a3 = tk("native-and-pagination", "Pagination, Slices and Native Queries", "Core",
    "Return Page and Slice results with Pageable/Sort, and write native SQL queries (with countQuery) when JPQL is not enough.",
    {"main/Application.java": APP, "main/Employee.java": EMP, "main/DeptCount.java": DEPT_COUNT, "main/EmployeeRepository.java": REPO3, "main/EmployeePaging.java": FAC3},
    {"test/PagingAndNativeTest.java": T3, **PROPS(3)},
    ["Declare the four repository methods.", "Implement the delegating facade methods and `describe`."],
    ["Page numbers are zero-based; `describe` shows one-based.", "Native paged queries need a `countQuery`.", "`Slice` skips the count query: cheaper, but no totals."],
    ["`PageRequest.of(page, size, Sort)`.", "Native SQL uses table and column names (`employees`, `hired_on`)."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 4
SUMMARY = "package %PKG%;\n\n/** Closed interface projection: Spring Data selects only these two columns. */\npublic interface EmployeeSummary {\n    String getName();\n\n    String getDepartment();\n}\n"
LABEL = "package %PKG%;\n\nimport org.springframework.beans.factory.annotation.Value;\n\n/** Open projection computed with SpEL. */\npublic interface EmployeeLabel {\n    @Value(\"#{target.name + ' (' + target.department + ')'}\")\n    String getLabel();\n}\n"
ROW = "package %PKG%;\n\nimport java.math.BigDecimal;\n\n/** Class-based (DTO) projection. */\npublic record EmployeeRow(String name, BigDecimal salary) {\n}\n"
REPO4 = r'''package %PKG%;

import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    //A! declare:
    //  List<EmployeeSummary> findByActiveTrueOrderByName()
    //  List<EmployeeLabel>   findByDepartmentOrderByName(String department)
    //  JPQL constructor expression -> List<EmployeeRow> rowsOf(@Param("dept") String dept): select new %PKG%.EmployeeRow(e.name, e.salary) from Employee e where e.department = :dept order by e.salary desc
    //  dynamic projection: <T> List<T> findByDepartmentOrderByNameAsc(String department, Class<T> type)
    List<EmployeeSummary> findByActiveTrueOrderByName();

    List<EmployeeLabel> findByDepartmentOrderByName(String department);

    @Query("select new %PKG%.EmployeeRow(e.name, e.salary) from Employee e where e.department = :dept order by e.salary desc")
    List<EmployeeRow> rowsOf(@Param("dept") String dept);

    <T> List<T> findByDepartmentOrderByNameAsc(String department, Class<T> type);
    //E!
}
'''
FAC4 = r'''package %PKG%;

import java.util.List;
import org.springframework.stereotype.Component;

@Component
public class EmployeeProjections {

    private final EmployeeRepository repository;

    public EmployeeProjections(EmployeeRepository repository) {
        this.repository = repository;
    }

    public List<EmployeeSummary> activeSummaries() {
        //B! closed projection
        return repository.findByActiveTrueOrderByName();
        //E!
    }

    public List<String> labels(String department) {
        //B! open projection labels
        return repository.findByDepartmentOrderByName(department).stream().map(EmployeeLabel::getLabel).toList();
        //E!
    }

    public List<EmployeeRow> rows(String department) {
        //B! DTO projection via constructor expression
        return repository.rowsOf(department);
        //E!
    }

    public <T> List<T> byDepartment(String department, Class<T> type) {
        //B! dynamic projection
        return repository.findByDepartmentOrderByNameAsc(department, type);
        //E!
    }
}
'''
T4 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(EmployeeProjections.class)
class ProjectionsTest {

    @Autowired
    EmployeeRepository repository;
    @Autowired
    EmployeeProjections projections;

''' + SEED + r'''
    @Test
    void closedProjectionCarriesOnlyTwoValues() {
        List<EmployeeSummary> s = projections.activeSummaries();
        assertThat(s).extracting(EmployeeSummary::getName).containsExactly("Ann", "Bob", "Dee", "Eve");
        assertThat(s.get(0).getDepartment()).isEqualTo("Eng");
    }

    @Test
    void openProjectionComputesLabel() {
        assertThat(projections.labels("Ops")).containsExactly("Dee (Ops)", "Eve (Ops)");
    }

    @Test
    void constructorExpressionBuildsDtos() {
        List<EmployeeRow> rows = projections.rows("Eng");
        assertThat(rows).extracting(EmployeeRow::name).containsExactly("Ann", "Bob", "Cid");
        assertThat(rows.get(0).salary()).isEqualByComparingTo("100");
    }

    @Test
    void dynamicProjectionChoosesTypeAtCallSite() {
        assertThat(projections.byDepartment("HR", EmployeeSummary.class)).extracting(EmployeeSummary::getName).containsExactly("Fay");
        assertThat(projections.byDepartment("HR", Employee.class)).hasSize(1).first().isInstanceOf(Employee.class);
        assertThat(projections.byDepartment("Eng", EmployeeRow.class)).extracting(EmployeeRow::name).containsExactly("Ann", "Bob", "Cid");
    }
}
'''
a4 = tk("projections-challenge", "Projections: Interface, Open, DTO and Dynamic", "Challenge",
    "Fetch only the data you need: closed and open interface projections, a constructor-expression DTO and a dynamic projection chosen by the caller.",
    {"main/Application.java": APP, "main/Employee.java": EMP, "main/EmployeeSummary.java": SUMMARY, "main/EmployeeLabel.java": LABEL,
     "main/EmployeeRow.java": ROW, "main/EmployeeRepository.java": REPO4, "main/EmployeeProjections.java": FAC4},
    {"test/ProjectionsTest.java": T4, **PROPS(4)},
    ["Declare the four repository methods (closed, open, constructor-expression, dynamic).", "Implement the facade delegates; `labels` maps the open projection to strings."],
    ["Constructor expressions need the fully qualified class name.", "Dynamic projection works with entity, interface and record/class types.", "Open projections load the whole entity; closed projections select fewer columns."],
    ["Record `EmployeeRow` has a matching constructor `(String, BigDecimal)`.", "`Class<T>` as the last parameter enables dynamic projections."],
    S, deps=DEPS)

topics = [
    T("Derived query methods",
      "Spring Data parses repository method names (`findBy`, `countBy`, `existsBy`, `deleteBy`, `Top`/`First`) into queries at startup. Keywords: `And`, `Or`, `Between`, `LessThan`, `GreaterThanEqual`, `Like`, `Containing`, `StartingWith`, `In`, `IsNull`, `True`, `IgnoreCase`, `OrderBy...Asc/Desc`. Property paths traverse relations (`findByAddressCity`).",
      "Most lookups are simple predicates; encoding them in the method name removes the need for JPQL strings and gives startup-time validation.",
      ["Zero query code for simple cases", "Compile-time visible API, verified at startup", "Readable for short predicates", "Supports sorting, limiting and projections"],
      ["Long names become unreadable (use `@Query`)", "Name typos fail only at startup/test time", "Renaming entity fields requires renaming methods"],
      "Hand-writing JPQL for every lookup is verbose. Conversely, 6-clause method names (`findByAAndBOrCAndD...`) are a maintenance trap and hide precedence rules.",
      "```java\nList<Employee> findByDepartmentAndActiveTrue(String d);\nList<Employee> findBySalaryGreaterThanEqualOrderBySalaryDesc(BigDecimal min);\nlong countByDepartment(String d);\nboolean existsByNameIgnoreCase(String n);\nList<Employee> findTop2ByOrderBySalaryDesc();\nlong deleteByActiveFalse();   // needs a transaction\n```",
      [("Between", "java", "List<Employee> findByHiredOnBetween(LocalDate from, LocalDate to);   // inclusive"),
       ("Collection parameter", "java", "List<Employee> findByDepartmentIn(Collection<String> departments);"),
       ("Nested property", "java", "List<Order> findByCustomerAddressCity(String city);   // customer.address.city")],
      [("Is Between inclusive?", "Yes, both bounds are inclusive."),
       ("What happens with a wrong property name?", "The application context fails to start with a PropertyReferenceException."),
       ("How do you limit results?", "`Top`/`First` in the name or a `Pageable` parameter.")]),
    T("@Query: JPQL, native SQL, modifying queries",
      "`@Query` supplies explicit JPQL (entity-based, portable) or native SQL (`nativeQuery = true`). Use named (`:name` + `@Param`) or positional parameters. `@Modifying` marks UPDATE/DELETE queries; use `clearAutomatically = true` so stale managed entities do not survive a bulk update. Aliases in select lists map to interface projection getters.",
      "Complex joins, aggregates, subqueries and database-specific features are clearer (and faster) as explicit queries than as method names.",
      ["Full expressive power of JPQL/SQL", "Validated at startup (JPQL)", "Named parameters are refactor-safe", "Bulk operations avoid loading entities"],
      ["Native SQL ties code to a database dialect", "Bulk updates bypass the persistence context, lifecycle callbacks and optimistic locking", "String queries have no compile-time checking"],
      "Forgetting `clearAutomatically` after a bulk update returns stale entities from the first-level cache. Concatenating user input into native strings invites SQL injection - always bind parameters.",
      "```java\n@Query(\"select e from Employee e where lower(e.name) like lower(concat('%', :q, '%'))\")\nList<Employee> search(@Param(\"q\") String q);\n\n@Modifying(clearAutomatically = true, flushAutomatically = true)\n@Query(\"update Employee e set e.salary = e.salary * :f where e.department = :d\")\nint raise(@Param(\"d\") String d, @Param(\"f\") BigDecimal f);\n\n@Query(value = \"select department, count(*) as headcount from employees group by department\", nativeQuery = true)\nList<DeptCount> headcounts();\n```",
      [("Subquery", "java", "@Query(\"select e from Employee e where e.salary > (select avg(x.salary) from Employee x)\")"),
       ("Aggregate projection", "java", "@Query(\"select e.department as department, sum(e.salary) as total from Employee e group by e.department\")\nList<DeptTotal> payroll();"),
       ("Native with count", "java", "@Query(value = \"select * from employees where salary >= :min\",\n       countQuery = \"select count(*) from employees where salary >= :min\", nativeQuery = true)\nPage<Employee> wellPaid(@Param(\"min\") BigDecimal min, Pageable p);")],
      [("What does clearAutomatically do?", "Clears the persistence context after the bulk query so later reads hit the database."),
       ("JPQL vs SQL names?", "JPQL uses entity and field names; SQL uses table and column names."),
       ("How do you avoid SQL injection?", "Bind parameters; never concatenate user input.")]),
    T("Pagination, sorting and projections",
      "`Pageable` (`PageRequest.of(page, size, Sort)`) turns list methods into `Page<T>` (content + total count + page metadata) or `Slice<T>` (content + has-next, no count query) or `List<T>`. **Projections** limit what is fetched: closed interface projections (getter names), open projections (`@Value` SpEL), class/record DTOs, and dynamic projections (`Class<T>` parameter).",
      "Returning unbounded lists does not scale, and loading entire entities to show two columns wastes memory and I/O. Pagination and projections make APIs predictable and efficient.",
      ["Bounded memory and response size", "`Slice` avoids expensive counts", "Projections reduce selected columns", "Dynamic projection reuses one query for several views"],
      ["Offset pagination gets slow on deep pages (use keyset/Scroll for huge tables)", "Count queries can be expensive", "Open projections load the full entity"],
      "Without paging, one request can load millions of rows (OOM, slow responses). Sorting by a non-indexed or unstable column yields duplicate/missing rows across pages: always add a unique tiebreaker such as the id.",
      "```java\nPage<Employee> findByDepartment(String dept, Pageable pageable);\nPageRequest.of(0, 20, Sort.by(\"salary\").descending().and(Sort.by(\"id\")));\n\ninterface EmployeeSummary { String getName(); String getDepartment(); }\nrecord EmployeeRow(String name, BigDecimal salary) {}\n<T> List<T> findByDepartment(String d, Class<T> type);\n```\n`Page` getters: `getContent`, `getTotalElements`, `getTotalPages`, `getNumber`, `hasNext`.",
      [("Controller usage", "java", "@GetMapping Page<EmployeeSummary> list(@PageableDefault(size = 20) Pageable p) { return repo.findAllBy(p); }"),
       ("Slice", "java", "Slice<Employee> findByActiveTrue(Pageable p);   // no count query"),
       ("Constructor expression", "java", "@Query(\"select new com.acme.EmployeeRow(e.name, e.salary) from Employee e\")")],
      [("Page vs Slice?", "`Page` runs a count query and knows totals; `Slice` only knows whether another slice exists."),
       ("Why add a tiebreaker to sorting?", "Stable ordering across pages prevents duplicates and gaps."),
       ("What is a dynamic projection?", "A repository method taking `Class<T>` so the caller chooses the return type.")]),
]

day(33, "Spring Data JPA II: Derived Queries, JPQL, Native SQL, Paging and Projections", "Spring Boot",
    "Querying with Spring Data: method-name queries, @Query, pagination and projections",
    ["Write derived query methods", "Use @Query with JPQL, native SQL and @Modifying", "Paginate with Page/Slice/Pageable/Sort", "Choose among interface, open, DTO and dynamic projections"],
    ["Day 32 Spring Data JPA I"],
    topics, [a1, a2, a3, a4],
    [("Derived queries vs @Query?", "Derived for short predicates; @Query when joins, aggregates or readability need explicit control."),
     ("Page vs Slice?", "Page includes totals via a count query; Slice does not."),
     ("Why use projections?", "To select only the required columns and decouple API shapes from entities."),
     ("What is the danger of @Modifying queries?", "They bypass the persistence context; clear it to avoid stale reads."),
     ("Offset pagination drawbacks?", "Deep pages are slow; consider keyset pagination.")],
    ["Misspelled property in a derived method.", "Forgetting `countQuery` for native paged queries.", "Using entity names in native SQL.", "Missing alias for projections."],
    ["Spring Data JPA Reference: Query Methods, Projections", "Hibernate: HQL guide"],
    [("Derived query", "Query generated from a method name"), ("JPQL", "Object query language of JPA"), ("Pageable", "Page request abstraction"),
     ("Projection", "Reduced view of entity data"), ("Slice", "Page without total count")],
    "2–3 h theory + 3–5 h tasks", spring=True)
