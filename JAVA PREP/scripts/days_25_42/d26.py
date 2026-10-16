from common import *
from d25 import TEST_HEAD

LAB = sqllab(26)

FLAT = r'''
    private static List<String> flat(List<List<Object>> rows) {
        List<String> out = new ArrayList<>();
        for (List<Object> r : rows) {
            List<String> cols = new ArrayList<>();
            for (Object o : r) {
                cols.add(String.valueOf(o instanceof Number n && !(o instanceof Double) ? n.longValue() : o));
            }
            out.add(String.join(":", cols));
        }
        return out;
    }
'''

# ------------------------------------------------------------ task 1
T1_TEST = TEST_HEAD + r'''
class JoinsTest {

    private Connection c;
    private Map<String, String> q;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "%TAG%");
        SqlLab.runScript(c, "sql/seed.sql", "%TAG%");
        q = SqlLab.namedBlocks("sql/answers.sql", "%TAG%");
    }

    @AfterEach
    void tearDown() throws Exception {
        c.close();
    }
''' + FLAT + r'''
    @Test
    void innerJoinOnlyMatchedPairs() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("inner_join")))).containsExactly("Ana:Eng", "Bo:Eng", "Cy:Sales");
    }

    @Test
    void leftJoinFindsEmployeesWithoutDepartment() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("left_unassigned")))).containsExactly("Di");
    }

    @Test
    void departmentsWithoutEmployees() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("dept_without_employees")))).containsExactly("Legal");
    }

    @Test
    void selfJoinManagers() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("self_join_manager")))).containsExactly("Bo:Ana", "Cy:Ana", "Di:Ana");
    }

    @Test
    void fullOuterRowCount() throws Exception {
        assertThat(SqlLab.scalar(c, q.get("full_outer_row_count"))).isEqualTo(5);
    }
}
'''

j1 = task("inner-outer-joins", "Inner and Outer Joins", "Warm-up", "SQL script + JDBC test",
    "Query a small HR schema with INNER, LEFT, anti-join and self-join queries, plus a FULL OUTER row count.",
    "h2",
    {"main/SqlLab.java": LAB,
     "sql/schema.sql": """-- PROVIDED
CREATE TABLE departments (id INT PRIMARY KEY, name VARCHAR(30) NOT NULL);
CREATE TABLE employees (
    id INT PRIMARY KEY, name VARCHAR(30) NOT NULL,
    dept_id INT REFERENCES departments(id),
    manager_id INT REFERENCES employees(id)
);
""",
     "sql/seed.sql": """-- PROVIDED
INSERT INTO departments VALUES (1, 'Eng');
INSERT INTO departments VALUES (2, 'Sales');
INSERT INTO departments VALUES (3, 'Legal');
INSERT INTO employees VALUES (1, 'Ana', 1, NULL);
INSERT INTO employees VALUES (2, 'Bo', 1, 1);
INSERT INTO employees VALUES (3, 'Cy', 2, 1);
INSERT INTO employees VALUES (4, 'Di', NULL, 1);
""",
     "sql/answers.sql": """-- @inner_join
-- TODO(%TAG%): employee name, department name for employees that HAVE a department; ORDER BY employee name

-- @left_unassigned
-- TODO(%TAG%): names of employees with NO department (LEFT JOIN ... WHERE d.id IS NULL); ORDER BY name

-- @dept_without_employees
-- TODO(%TAG%): names of departments that have no employees (anti-join); ORDER BY name

-- @self_join_manager
-- TODO(%TAG%): employee name, manager name for employees that have a manager; ORDER BY employee name

-- @full_outer_row_count
-- TODO(%TAG%): COUNT of rows in the full outer join of employees and departments (UNION of LEFT and RIGHT joins is fine)
""",
     "test/JoinsTest.java": T1_TEST},
    ["Answer the five query blocks in `sql/answers.sql`.", "Use the correct join type for each question (inner, left, anti-join, self-join).",
     "Order results exactly as requested so the tests can compare lists."],
    ["Employees with a NULL `dept_id` must not appear in the inner join.", "The CEO (no manager) must not appear in the self-join result.",
     "`COUNT` over a UNION needs a subquery."],
    ["Anti-join: `LEFT JOIN ... WHERE right.id IS NULL`.", "Self join: alias the same table twice (`e` and `m`).",
     "Full outer count = matched + unmatched left + unmatched right = 3 + 1 + 1."],
    sol={"sql/answers.sql": """-- @inner_join
SELECT e.name, d.name FROM employees e JOIN departments d ON d.id = e.dept_id ORDER BY e.name;
-- @left_unassigned
SELECT e.name FROM employees e LEFT JOIN departments d ON d.id = e.dept_id WHERE d.id IS NULL ORDER BY e.name;
-- @dept_without_employees
SELECT d.name FROM departments d LEFT JOIN employees e ON e.dept_id = d.id WHERE e.id IS NULL ORDER BY d.name;
-- @self_join_manager
SELECT e.name, m.name FROM employees e JOIN employees m ON m.id = e.manager_id ORDER BY e.name;
-- @full_outer_row_count
SELECT COUNT(*) FROM (SELECT e.id eid, d.id did FROM employees e LEFT JOIN departments d ON d.id = e.dept_id
 UNION SELECT e.id, d.id FROM employees e RIGHT JOIN departments d ON d.id = e.dept_id) x;
"""})

# ------------------------------------------------------------ task 2
T2_TEST = TEST_HEAD + r'''
class GroupByTest {

    private Connection c;
    private Map<String, String> q;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "%TAG%");
        SqlLab.runScript(c, "sql/seed.sql", "%TAG%");
        q = SqlLab.namedBlocks("sql/answers.sql", "%TAG%");
    }

    @AfterEach
    void tearDown() throws Exception {
        c.close();
    }
''' + FLAT + r'''
    @Test
    void totalsByRegion() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("total_by_region")))).containsExactly("APAC:12000", "EU:13000", "US:5500");
    }

    @Test
    void saleCountByRegion() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("count_by_region")))).containsExactly("APAC:1", "EU:3", "US:2");
    }

    @Test
    void havingFiltersGroups() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("regions_over_10000")))).containsExactly("APAC", "EU");
    }

    @Test
    void topRep() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("top_rep")))).containsExactly("di:12000");
    }

    @Test
    void averageIsRoundedDown() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("avg_sale_eu")))).containsExactly("4333");
    }
}
'''

j2 = task("group-by-having", "GROUP BY and HAVING", "Core", "SQL script + JDBC test",
    "Aggregate a `sales` table with COUNT/SUM/AVG, GROUP BY, HAVING and ORDER BY ... LIMIT.",
    "h2",
    {"main/SqlLab.java": LAB,
     "sql/schema.sql": """-- PROVIDED
CREATE TABLE sales (
    id INT PRIMARY KEY, region VARCHAR(10) NOT NULL, rep VARCHAR(20) NOT NULL,
    amount_cents INT NOT NULL, sold_on DATE NOT NULL
);
""",
     "sql/seed.sql": """-- PROVIDED
INSERT INTO sales VALUES (1, 'EU', 'ana', 5000, DATE '2024-01-05');
INSERT INTO sales VALUES (2, 'EU', 'bo', 7000, DATE '2024-01-20');
INSERT INTO sales VALUES (3, 'US', 'cy', 3000, DATE '2024-02-01');
INSERT INTO sales VALUES (4, 'US', 'cy', 2500, DATE '2024-02-15');
INSERT INTO sales VALUES (5, 'APAC', 'di', 12000, DATE '2024-02-20');
INSERT INTO sales VALUES (6, 'EU', 'ana', 1000, DATE '2024-03-01');
""",
     "sql/answers.sql": """-- @total_by_region
-- TODO(%TAG%): region, SUM(amount_cents) per region ORDER BY region

-- @count_by_region
-- TODO(%TAG%): region, COUNT(*) per region ORDER BY region

-- @regions_over_10000
-- TODO(%TAG%): regions (one column) whose total exceeds 10000 — use HAVING; ORDER BY region

-- @top_rep
-- TODO(%TAG%): rep and total amount of the single best rep (GROUP BY rep, ORDER BY total DESC, LIMIT 1)

-- @avg_sale_eu
-- TODO(%TAG%): average sale of region 'EU' rounded DOWN to a whole number (FLOOR, then CAST AS INT)
""",
     "test/GroupByTest.java": T2_TEST},
    ["Fill the five blocks in `sql/answers.sql`.", "Use HAVING (not WHERE) for filters on aggregates.", "Use deterministic ORDER BY clauses."],
    ["Ties are not present in the data, but your ORDER BY must still be explicit.", "AVG of integers: the expected value is `4333` (13000 / 3 rounded down)."],
    ["WHERE filters rows before grouping; HAVING filters groups after.", "`SELECT rep, SUM(amount_cents) t ... ORDER BY t DESC LIMIT 1`."],
    sol={"sql/answers.sql": """-- @total_by_region
SELECT region, SUM(amount_cents) FROM sales GROUP BY region ORDER BY region;
-- @count_by_region
SELECT region, COUNT(*) FROM sales GROUP BY region ORDER BY region;
-- @regions_over_10000
SELECT region FROM sales GROUP BY region HAVING SUM(amount_cents) > 10000 ORDER BY region;
-- @top_rep
SELECT rep, SUM(amount_cents) t FROM sales GROUP BY rep ORDER BY t DESC LIMIT 1;
-- @avg_sale_eu
SELECT CAST(FLOOR(AVG(amount_cents)) AS INT) FROM sales WHERE region = 'EU';
"""})

# ------------------------------------------------------------ task 3
IDX_MAIN = r'''package %PKG%;

import java.util.List;

/** Produces index DDL and reads query plans. Pure string logic — no database needed. */
public final class IndexAdvisor {

    private IndexAdvisor() {
    }

    /**
     * Composite index recommendation: equality columns first (in the given order), then the optional range column.
     * Format: {@code CREATE INDEX idx_<table>_<col1>_<col2> ON <table> (<col1>, <col2>)}.
     * Example: ("orders", [customer_id, status], "created_at") ->
     * {@code CREATE INDEX idx_orders_customer_id_status_created_at ON orders (customer_id, status, created_at)}.
     * rangeColumn may be null. No columns at all -> IllegalArgumentException.
     */
    public static String recommendIndex(String table, List<String> equalityColumns, String rangeColumn) {
        // TODO(%TAG%): build the DDL string as documented above
        throw new UnsupportedOperationException("TODO(%TAG%): implement recommendIndex");
    }

    /** {@code CREATE UNIQUE INDEX uq_<table>_<column> ON <table> (<column>)} */
    public static String recommendUniqueIndex(String table, String column) {
        // TODO(%TAG%): build the unique-index DDL string
        throw new UnsupportedOperationException("TODO(%TAG%): implement recommendUniqueIndex");
    }

    /**
     * Can a B-tree index on the column serve this predicate? False for a leading-wildcard LIKE
     * ({@code email like '%gmail.com'}) and for a function wrapped around the column ({@code lower(email) = 'a'}).
     * True otherwise ({@code status = 'NEW'}, {@code email like 'ana%'}, {@code created_at > '2024-01-01'}).
     */
    public static boolean isIndexUsable(String predicate) {
        // TODO(%TAG%): lower-case + trim the predicate and apply the two rules
        throw new UnsupportedOperationException("TODO(%TAG%): implement isIndexUsable");
    }

    /**
     * Classifies an H2 EXPLAIN plan text: contains "tablescan" (any case) -> "FULL_SCAN";
     * contains "idx_" (any case) -> "INDEX_SCAN"; otherwise "UNKNOWN".
     */
    public static String classifyPlan(String planText) {
        // TODO(%TAG%): classify the plan
        throw new UnsupportedOperationException("TODO(%TAG%): implement classifyPlan");
    }
}
'''

IDX_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import org.junit.jupiter.api.Test;

class IndexAdvisorTest {

    @Test
    void compositeIndexPutsEqualityBeforeRange() {
        assertThat(IndexAdvisor.recommendIndex("orders", List.of("customer_id", "status"), "created_at"))
                .isEqualTo("CREATE INDEX idx_orders_customer_id_status_created_at ON orders (customer_id, status, created_at)");
    }

    @Test
    void rangeColumnIsOptional() {
        assertThat(IndexAdvisor.recommendIndex("users", List.of("email"), null))
                .isEqualTo("CREATE INDEX idx_users_email ON users (email)");
    }

    @Test
    void onlyRangeColumn() {
        assertThat(IndexAdvisor.recommendIndex("logs", List.of(), "created_at"))
                .isEqualTo("CREATE INDEX idx_logs_created_at ON logs (created_at)");
    }

    @Test
    void nothingToIndexIsRejected() {
        assertThatThrownBy(() -> IndexAdvisor.recommendIndex("t", List.of(), null))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void uniqueIndex() {
        assertThat(IndexAdvisor.recommendUniqueIndex("users", "email"))
                .isEqualTo("CREATE UNIQUE INDEX uq_users_email ON users (email)");
    }

    @Test
    void sargability() {
        assertThat(IndexAdvisor.isIndexUsable("status = 'NEW'")).isTrue();
        assertThat(IndexAdvisor.isIndexUsable("email LIKE 'ana%'")).isTrue();
        assertThat(IndexAdvisor.isIndexUsable("created_at > '2024-01-01'")).isTrue();
        assertThat(IndexAdvisor.isIndexUsable("email LIKE '%gmail.com'")).isFalse();
        assertThat(IndexAdvisor.isIndexUsable("  LOWER(email) = 'a@x.io'")).isFalse();
    }

    @Test
    void planClassification() {
        assertThat(IndexAdvisor.classifyPlan("SELECT * FROM PUBLIC.ORDERS /* PUBLIC.ORDERS.tableScan */"))
                .isEqualTo("FULL_SCAN");
        assertThat(IndexAdvisor.classifyPlan("SELECT * FROM PUBLIC.ORDERS /* PUBLIC.IDX_ORDERS_STATUS: STATUS = 'NEW' */"))
                .isEqualTo("INDEX_SCAN");
        assertThat(IndexAdvisor.classifyPlan("something else")).isEqualTo("UNKNOWN");
    }
}
'''

IDX_SOL = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;

public final class IndexAdvisor {
    public static String recommendIndex(String table, List<String> eq, String range) {
        List<String> cols = new ArrayList<>(eq);
        if (range != null) cols.add(range);
        if (cols.isEmpty()) throw new IllegalArgumentException("no columns");
        return "CREATE INDEX idx_" + table + "_" + String.join("_", cols) + " ON " + table + " (" + String.join(", ", cols) + ")";
    }
    public static String recommendUniqueIndex(String table, String column) {
        return "CREATE UNIQUE INDEX uq_" + table + "_" + column + " ON " + table + " (" + column + ")";
    }
    public static boolean isIndexUsable(String p) {
        String s = p.trim().toLowerCase();
        return !(s.matches(".*like\\s+'%.*") || s.matches("^[a-z_]+\\(.*"));
    }
    public static String classifyPlan(String plan) {
        String s = plan.toLowerCase();
        return s.contains("tablescan") ? "FULL_SCAN" : s.contains("idx_") ? "INDEX_SCAN" : "UNKNOWN";
    }
}
'''

j3 = task("index-explain-notes", "Index and EXPLAIN Notes", "Core", "Plain Java",
    "Turn query shapes into recommended index DDL strings, decide whether a predicate can use a B-tree index, and classify an EXPLAIN plan.",
    "plain",
    {"main/IndexAdvisor.java": IDX_MAIN, "test/IndexAdvisorTest.java": IDX_TEST},
    ["Implement `recommendIndex` (equality columns first, then range) and `recommendUniqueIndex` with the documented naming.",
     "Implement `isIndexUsable` for leading-wildcard LIKE and function-wrapped columns.", "Implement `classifyPlan` for H2-style plan text."],
    ["`rangeColumn == null` is allowed; no columns at all -> `IllegalArgumentException`.", "Predicate checks are case-insensitive and ignore surrounding whitespace."],
    ["Column order in a composite index matters: equality predicates first, range last.", "`String.join` builds the comma lists."],
    sol={"main/IndexAdvisor.java": IDX_SOL})

# ------------------------------------------------------------ task 4
T4_TEST = TEST_HEAD + r'''
class ViewTest {

    private Connection c;
    private Map<String, String> q;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "%TAG%");
        SqlLab.runScript(c, "sql/seed.sql", "%TAG%");
        q = SqlLab.namedBlocks("sql/answers.sql", "%TAG%");
        c.setAutoCommit(false);
        SqlLab.update(c, q.get("create_view_order_totals"));
        c.commit();
    }

    @AfterEach
    void tearDown() throws Exception {
        c.close();
    }
''' + FLAT + r'''
    @Test
    void viewExposesOneRowPerOrder() throws Exception {
        assertThat(SqlLab.scalar(c, "select count(*) from order_totals")).isEqualTo(3);
        assertThat(flat(SqlLab.query(c, "select order_id, total_cents from order_totals order by order_id")))
                .containsExactly("1:11000", "2:3000", "3:14000");
    }

    @Test
    void bigOrdersQueryUsesTheView() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("q_big_orders")))).containsExactly("1:11000", "3:14000");
    }

    @Test
    void domainCountsUseStringFunctions() throws Exception {
        assertThat(flat(SqlLab.query(c, q.get("q_domain_counts")))).containsExactly("x.io:2", "y.io:1");
    }

    @Test
    void viewReflectsNewDataAndRollbackWorks() throws Exception {
        SqlLab.update(c, "insert into orders values (4, 2)");
        SqlLab.update(c, "insert into order_items values (4, 'Z', 1, 20000)");
        assertThat(SqlLab.scalar(c, "select count(*) from order_totals")).isEqualTo(4);
        c.rollback();
        assertThat(SqlLab.scalar(c, "select count(*) from order_totals")).isEqualTo(3);
    }
}
'''

j4 = task("view-and-txn", "Views, Functions and Transactions", "Challenge", "SQL script + JDBC test",
    "Create a view that summarizes order totals, query it, use SQL string functions, and show that a view sees uncommitted data in its own transaction and respects ROLLBACK.",
    "h2",
    {"main/SqlLab.java": LAB,
     "sql/schema.sql": """-- PROVIDED
CREATE TABLE customers (id INT PRIMARY KEY, email VARCHAR(120) NOT NULL);
CREATE TABLE orders (id INT PRIMARY KEY, customer_id INT NOT NULL REFERENCES customers(id));
CREATE TABLE order_items (
    order_id INT NOT NULL REFERENCES orders(id), sku VARCHAR(20) NOT NULL,
    qty INT NOT NULL, unit_price_cents INT NOT NULL, PRIMARY KEY (order_id, sku)
);
""",
     "sql/seed.sql": """-- PROVIDED
INSERT INTO customers VALUES (1, 'ana@x.io');
INSERT INTO customers VALUES (2, 'bob@y.io');
INSERT INTO customers VALUES (3, 'cy@x.io');
INSERT INTO orders VALUES (1, 1);
INSERT INTO orders VALUES (2, 2);
INSERT INTO orders VALUES (3, 1);
INSERT INTO order_items VALUES (1, 'A', 2, 3000);
INSERT INTO order_items VALUES (1, 'B', 1, 5000);
INSERT INTO order_items VALUES (2, 'A', 1, 3000);
INSERT INTO order_items VALUES (3, 'C', 2, 7000);
""",
     "sql/answers.sql": """-- @create_view_order_totals
-- TODO(%TAG%): CREATE VIEW order_totals AS SELECT order_id, SUM(qty * unit_price_cents) AS total_cents FROM order_items GROUP BY order_id

-- @q_big_orders
-- TODO(%TAG%): SELECT order_id, total_cents FROM the VIEW where total_cents >= 10000 ORDER BY order_id

-- @q_domain_counts
-- TODO(%TAG%): email domain (text after '@') and number of customers per domain, ORDER BY domain.
--              Hint: SUBSTR(email, POSITION('@' IN email) + 1)
""",
     "test/ViewTest.java": T4_TEST},
    ["Define the `order_totals` view with columns `order_id` and `total_cents`.", "Query the view for big orders and compute customer counts per email domain with SQL functions."],
    ["The view must update automatically when new items are inserted.", "Rolled-back inserts must not appear in the view."],
    ["A view stores a query, not data.", "`GROUP BY` the expression you SELECT for the domain."],
    sol={"sql/answers.sql": """-- @create_view_order_totals
CREATE VIEW order_totals AS SELECT order_id, SUM(qty * unit_price_cents) AS total_cents FROM order_items GROUP BY order_id;
-- @q_big_orders
SELECT order_id, total_cents FROM order_totals WHERE total_cents >= 10000 ORDER BY order_id;
-- @q_domain_counts
SELECT SUBSTR(email, POSITION('@' IN email) + 1) d, COUNT(*) FROM customers GROUP BY SUBSTR(email, POSITION('@' IN email) + 1) ORDER BY d;
"""})

topics = [
    T("Joins",
      "A **join** combines rows from two tables on a condition. `INNER JOIN` keeps matches only; `LEFT/RIGHT OUTER JOIN` keep all rows of one side and fill NULLs for missing matches; `FULL OUTER JOIN` keeps both; `CROSS JOIN` is the Cartesian product; a **self join** joins a table with itself (e.g. employee -> manager).",
      "Normalized data (Day 25) is spread across tables; joins reassemble it. Choosing the wrong join type silently drops or duplicates rows — a top source of wrong reports.",
      ["Express relationships declaratively; the optimizer picks nested-loop, hash or merge join", "Outer joins answer 'what is missing?' (anti-join)", "Self joins model hierarchies without extra tables", "Set-based and fast with proper indexes"],
      ["Joining on non-indexed columns is slow on big tables", "One-to-many joins multiply rows, breaking aggregates", "Many-join queries get hard to read and plan"],
      "Using INNER JOIN where you needed LEFT JOIN silently hides employees without a department. Joining a one-to-many table before `SUM` double-counts. A missing ON clause produces a Cartesian product (millions of rows).",
      "```sql\nSELECT e.name, d.name FROM employees e JOIN departments d ON d.id = e.dept_id;           -- inner\nSELECT e.name FROM employees e LEFT JOIN departments d ON d.id = e.dept_id WHERE d.id IS NULL; -- anti-join\nSELECT e.name, m.name FROM employees e JOIN employees m ON m.id = e.manager_id;           -- self\n```\nFilter on the right table of a LEFT JOIN in `ON`, not `WHERE`, or you turn it into an inner join.",
      [("Inner vs left", "sql", "-- employees without department are dropped:\nSELECT e.name, d.name FROM employees e JOIN departments d ON d.id = e.dept_id;\n-- employees kept, d.name NULL when absent:\nSELECT e.name, d.name FROM employees e LEFT JOIN departments d ON d.id = e.dept_id;"),
       ("Anti-join", "sql", "SELECT d.name FROM departments d\nLEFT JOIN employees e ON e.dept_id = d.id\nWHERE e.id IS NULL;"),
       ("Full outer via UNION", "sql", "SELECT e.id, d.id FROM employees e LEFT JOIN departments d ON d.id = e.dept_id\nUNION\nSELECT e.id, d.id FROM employees e RIGHT JOIN departments d ON d.id = e.dept_id;")],
      [("Which join finds departments with no employees?", "LEFT JOIN from departments to employees with `WHERE e.id IS NULL` (anti-join)."),
       ("Why can a WHERE on the right table break a LEFT JOIN?", "Rows with NULL on the right fail the predicate and are removed, making it behave like an inner join."),
       ("What does a missing ON condition produce?", "A Cartesian product of both tables.")]),
    T("Aggregation: GROUP BY, HAVING and window-free reporting",
      "Aggregate functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`) collapse many rows into one value. `GROUP BY` forms groups; `HAVING` filters groups; `ORDER BY ... LIMIT` ranks them. Logical order: FROM/JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT.",
      "Reports, dashboards and invariants (e.g. money supply) are aggregations. Understanding evaluation order explains why aliases are not usable in WHERE and why HAVING exists.",
      ["Database does the heavy lifting close to the data", "Declarative and portable across engines", "Combine with joins for rich reporting", "`COUNT(DISTINCT x)` answers cardinality questions"],
      ["Aggregating huge tables is I/O heavy without summaries/indexes", "NULL handling surprises (`COUNT(col)` ignores NULLs, `COUNT(*)` does not)", "Integer division and AVG rounding differ between engines"],
      "Selecting a non-grouped column raises `column must appear in the GROUP BY clause`. Using WHERE for an aggregate condition raises `aggregate functions are not allowed in WHERE`. Averaging ints and expecting decimals gives truncated numbers.",
      "```sql\nSELECT region, SUM(amount_cents) AS total FROM sales GROUP BY region HAVING SUM(amount_cents) > 10000 ORDER BY region;\nSELECT rep, SUM(amount_cents) t FROM sales GROUP BY rep ORDER BY t DESC LIMIT 1;\n```",
      [("Totals per group", "sql", "SELECT region, COUNT(*) n, SUM(amount_cents) total FROM sales GROUP BY region ORDER BY region;"),
       ("HAVING", "sql", "SELECT region FROM sales GROUP BY region HAVING SUM(amount_cents) > 10000;"),
       ("Top-1 per ranking", "sql", "SELECT rep, SUM(amount_cents) t FROM sales GROUP BY rep ORDER BY t DESC LIMIT 1;")],
      [("WHERE vs HAVING?", "WHERE filters rows before grouping; HAVING filters groups after aggregation."),
       ("COUNT(*) vs COUNT(col)?", "COUNT(*) counts rows; COUNT(col) counts non-NULL values of col."),
       ("Why does `SELECT region, rep, SUM(x) ... GROUP BY region` fail?", "`rep` is neither grouped nor aggregated.")]),
    T("Indexes and EXPLAIN",
      "An **index** is a sorted structure (usually a B-tree) that lets the database find rows without scanning the table. `EXPLAIN` shows the plan: sequential scan vs index scan, join algorithm, estimated rows. Composite indexes follow the **leftmost prefix** rule; a predicate is **sargable** if an index can serve it.",
      "Most production slowness is a missing or unusable index. Backend engineers must read plans and reason about write cost vs read speed.",
      ["Turns O(n) scans into O(log n) lookups", "UNIQUE indexes enforce constraints", "Covering indexes avoid table lookups", "Partial/expression indexes (PostgreSQL) target hot queries"],
      ["Each index slows INSERT/UPDATE/DELETE and uses disk/RAM", "Wrong column order makes a composite index useless", "Planner may ignore an index for small tables or low selectivity — that is correct"],
      "`WHERE lower(email) = ?` and `LIKE '%x'` cannot use a plain index on `email`; implicit casts also disable indexes. Over-indexing slows writes and bloats storage.",
      "```sql\nCREATE INDEX idx_orders_customer_status_created ON orders (customer_id, status, created_at);\nEXPLAIN SELECT * FROM orders WHERE customer_id = 1 AND status = 'NEW' AND created_at > '2024-01-01';\n-- PostgreSQL: EXPLAIN (ANALYZE, BUFFERS) shows real timing\n```\nRule: equality columns first, then range, then ORDER BY columns.",
      [("Composite index design", "sql", "-- query: WHERE customer_id = ? AND status = ? ORDER BY created_at DESC\nCREATE INDEX idx_orders_cust_status_created ON orders (customer_id, status, created_at);"),
       ("Not sargable vs sargable", "sql", "WHERE lower(email) = 'a@x.io'   -- full scan\nWHERE email = 'a@x.io'          -- index lookup\nCREATE INDEX idx_users_lower_email ON users (lower(email)); -- PostgreSQL expression index"),
       ("Reading a plan (H2)", "text", "SELECT ... FROM PUBLIC.ORDERS /* PUBLIC.IDX_ORDERS_STATUS: STATUS = 'NEW' */   -> index scan\nSELECT ... FROM PUBLIC.ORDERS /* PUBLIC.ORDERS.tableScan */                     -> full scan")],
      [("Why order composite index columns equality-first?", "The B-tree can only narrow by a leftmost prefix; a range column ends the usable prefix."),
       ("Why can LIKE '%abc' not use a B-tree index?", "B-trees sort by the beginning of the string; a leading wildcard has no starting point."),
       ("What is the cost of an extra index?", "Slower writes and more storage/memory.")]),
    T("Views, functions, and transactions in practice",
      "A **view** is a stored query presented as a virtual table (PostgreSQL also has materialized views that store results). **Functions** include built-ins (`SUBSTR`, `COALESCE`, `NOW()`) and user-defined PL/pgSQL functions. **Transactions** wrap multiple statements; a view inside a transaction sees that transaction's own uncommitted changes.",
      "Views encapsulate complex joins and hide columns for security; functions avoid repeating logic; transactions guarantee consistency across multi-step operations.",
      ["Views simplify queries and enforce column-level access", "Built-in functions push formatting/parsing to the database", "Transactions + views give consistent snapshots", "Materialized views accelerate heavy reports"],
      ["Views hide complexity — a slow view is a slow query everywhere", "Materialized views go stale until refreshed", "PL/pgSQL logic in the database is harder to test and version"],
      "Nesting views several levels deep produces unreadable plans. Forgetting `COMMIT` leaves a connection holding locks (idle in transaction). Relying on H2-only functions breaks on PostgreSQL.",
      "```sql\nCREATE VIEW order_totals AS\n  SELECT order_id, SUM(qty * unit_price_cents) AS total_cents FROM order_items GROUP BY order_id;\nSELECT * FROM order_totals WHERE total_cents >= 10000;\n```\nPostgreSQL extras: `CREATE MATERIALIZED VIEW ...; REFRESH MATERIALIZED VIEW ...;` and `CREATE FUNCTION ... LANGUAGE plpgsql`.",
      [("View over aggregation", "sql", "CREATE VIEW order_totals AS SELECT order_id, SUM(qty*unit_price_cents) total_cents FROM order_items GROUP BY order_id;"),
       ("String functions", "sql", "SELECT SUBSTR(email, POSITION('@' IN email) + 1) AS domain, COUNT(*) FROM customers GROUP BY 1;"),
       ("Rollback and views", "java", "c.setAutoCommit(false);\ninsert(...);               // visible through the view in this transaction\nc.rollback();             // gone again")],
      [("Does a plain view store data?", "No — it stores the query and runs it on each access."),
       ("How is a materialized view different?", "It stores the result set and must be refreshed."),
       ("What does an uncommitted insert look like to another connection?", "Invisible under READ COMMITTED.")]),
]

day(26, "Joins, Aggregates, Indexes, Views, and Transactions", "SQL/JDBC",
    "Query-writing skills for real backends: joins, aggregation, indexing strategy, views, and transaction behavior (H2 in PostgreSQL mode)",
    ["Choose between inner, outer, anti and self joins", "Aggregate with GROUP BY/HAVING and rank results", "Recommend composite and unique indexes; recognize non-sargable predicates", "Create and query views; use SQL functions", "Reason about view visibility inside transactions"],
    ["Day 25 (DDL, DML, keys, ACID)"],
    topics, [j1, j2, j3, j4],
    [("INNER vs LEFT JOIN?", "INNER keeps only matches; LEFT keeps every left row with NULLs where no match."),
     ("Explain the leftmost-prefix rule.", "A composite index (a,b,c) can serve predicates on a, a+b, a+b+c but not b alone."),
     ("How do you find a slow query's problem?", "EXPLAIN (ANALYZE), look for seq scans on large tables, bad row estimates, missing indexes, sort spills."),
     ("WHERE vs HAVING?", "Row filter before grouping vs group filter after aggregation."),
     ("When is a materialized view appropriate?", "Expensive, read-heavy reports tolerating stale data between refreshes.")],
    ["Putting a right-table filter in WHERE of a LEFT JOIN.", "Summing after joining a one-to-many table (double counting).", "Assuming the optimizer uses every index — always check EXPLAIN.", "Creating indexes on low-selectivity columns (boolean) without reason."],
    ["PostgreSQL docs: Queries, Indexes, Performance Tips", "Markus Winand — Use The Index, Luke", "H2 grammar reference"],
    [("Sargable", "Search-ARGument-able: predicate usable by an index"), ("Anti-join", "Rows with no match in another table"), ("Seq scan", "Reading every row of a table"),
     ("Covering index", "Index containing all columns the query needs"), ("Materialized view", "View whose result is stored and refreshed")],
    "2–3 h theory + 3–5 h tasks")
