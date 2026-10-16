from sx import *

S = ["spring-boot-starter-data-jpa"]
DEPS = [H2]

HDR = '''package %PKG%;

import jakarta.persistence.*;
import java.util.*;

'''
PROPS = lambda n: {"tres/application.properties": h2props("34", str(n))}
CNT = '''    private int count(String table) {
        Integer n = jdbc.queryForObject("select count(*) from " + table, Integer.class);
        return n == null ? 0 : n;
    }

    private boolean loaded(Object entity, String attribute) {
        return em.getEntityManager().getEntityManagerFactory().getPersistenceUnitUtil().isLoaded(entity, attribute);
    }
'''
TEST_HDR = '''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.jdbc.core.JdbcTemplate;

@DataJpaTest
'''

# ------------------------------------------------------------ task 1
ACC = HDR + r'''/** One account owns exactly one profile (FK column profile_id on accounts). */
@Entity
@Table(name = "accounts")
public class Account {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String email;

    //A! owning side of a one-to-one: LAZY, cascade ALL, orphanRemoval, join column profile_id
    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "profile_id")
    //E!
    private Profile profile;

    protected Account() {
    }

    public Account(String email) {
        this.email = email;
    }

    public Long getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public Profile getProfile() {
        return profile;
    }

    public void setProfile(Profile profile) {
        this.profile = profile;
    }
}
'''
PROF = HDR + r'''@Entity
@Table(name = "profiles")
public class Profile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String bio;

    protected Profile() {
    }

    public Profile(String bio) {
        this.bio = bio;
    }

    public Long getId() {
        return id;
    }

    public String getBio() {
        return bio;
    }
}
'''
T1 = TEST_HDR + r'''class OneToOneTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    JdbcTemplate jdbc;

''' + CNT + r'''
    private Account saved() {
        Account a = new Account("a@x.io");
        a.setProfile(new Profile("hi"));
        return em.persistAndFlush(a);
    }

    @Test
    void savingAccountCascadesToProfile() {
        saved();
        assertThat(count("profiles")).isEqualTo(1);
    }

    @Test
    void foreignKeyLivesOnAccounts() {
        Account a = saved();
        Long fk = jdbc.queryForObject("select profile_id from accounts where id = ?", Long.class, a.getId());
        assertThat(fk).isEqualTo(a.getProfile().getId());
    }

    @Test
    void profileIsLazy() {
        Account a = saved();
        em.clear();
        Account loaded = em.find(Account.class, a.getId());
        assertThat(loaded.getProfile()).isNotNull();
        assertThat(loaded(loaded, "profile")).isFalse();
        assertThat(loaded.getProfile().getBio()).isEqualTo("hi");
    }

    @Test
    void replacingProfileDeletesTheOrphan() {
        Account a = saved();
        a.setProfile(new Profile("new"));
        em.flush();
        assertThat(count("profiles")).isEqualTo(1);
        assertThat(jdbc.queryForObject("select bio from profiles", String.class)).isEqualTo("new");
    }

    @Test
    void removingAccountRemovesProfile() {
        Account a = saved();
        em.remove(a);
        em.flush();
        assertThat(count("accounts")).isZero();
        assertThat(count("profiles")).isZero();
    }
}
'''.replace("boolean loaded(Object", "boolean loaded(Object").replace("assertThat(loaded(loaded, \"profile\"))", "assertThat(loaded(loaded, \"profile\"))")
# avoid local variable shadowing the helper name
T1 = T1.replace("Account loaded = em.find", "Account acc = em.find").replace("loaded.getProfile()", "acc.getProfile()").replace("loaded(loaded, \"profile\")", "loaded(acc, \"profile\")")
a1 = tk("one-to-one-profile", "One-to-One: Account and Profile", "Warm-up",
    "Map a unidirectional one-to-one with a foreign key, lazy fetching, cascade and orphan removal.",
    {"main/Application.java": APP, "main/Account.java": ACC, "main/Profile.java": PROF},
    {"test/OneToOneTest.java": T1, **PROPS(1)},
    ["Annotate `Account.profile` as the owning side of a one-to-one (LAZY, cascade ALL, orphanRemoval, join column `profile_id`)."],
    ["Replacing the profile must delete the previous one (orphanRemoval).", "Lazy to-one needs a proxy: the entity cannot be final."],
    ["`@OneToOne` defaults to EAGER; override with `fetch = LAZY`.", "`@JoinColumn` on the owning side names the FK column."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 2
CUST = HDR + r'''@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    //A! inverse side: mappedBy "customer", cascade ALL, orphanRemoval
    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
    //E!
    private List<PurchaseOrder> orders = new ArrayList<>();

    protected Customer() {
    }

    public Customer(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<PurchaseOrder> getOrders() {
        return orders;
    }

    /** Keep BOTH sides of the association in sync. */
    public void addOrder(PurchaseOrder order) {
        //B! add to the list and set the back reference
        orders.add(order);
        order.setCustomer(this);
        //E!
    }

    /** Keep BOTH sides in sync; orphanRemoval then deletes the row. */
    public void removeOrder(PurchaseOrder order) {
        //B! remove from the list and clear the back reference
        orders.remove(order);
        order.setCustomer(null);
        //E!
    }
}
'''
ORD = HDR + r'''@Entity
@Table(name = "purchase_orders")
public class PurchaseOrder {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String reference;

    //A! owning side: many-to-one, LAZY, join column customer_id, not nullable
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "customer_id", nullable = false)
    //E!
    private Customer customer;

    protected PurchaseOrder() {
    }

    public PurchaseOrder(String reference) {
        this.reference = reference;
    }

    public Long getId() {
        return id;
    }

    public String getReference() {
        return reference;
    }

    public Customer getCustomer() {
        return customer;
    }

    void setCustomer(Customer customer) {
        this.customer = customer;
    }
}
'''
T2 = TEST_HDR + r'''class OneToManyTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    JdbcTemplate jdbc;

''' + CNT + r'''
    private Customer saved() {
        Customer c = new Customer("Ann");
        c.addOrder(new PurchaseOrder("A-1"));
        c.addOrder(new PurchaseOrder("A-2"));
        return em.persistAndFlush(c);
    }

    @Test
    void helpersKeepBothSidesInSync() {
        Customer c = new Customer("Ann");
        PurchaseOrder o = new PurchaseOrder("X");
        c.addOrder(o);
        assertThat(c.getOrders()).containsExactly(o);
        assertThat(o.getCustomer()).isSameAs(c);
        c.removeOrder(o);
        assertThat(c.getOrders()).isEmpty();
        assertThat(o.getCustomer()).isNull();
    }

    @Test
    void persistCascadesToOrders() {
        saved();
        assertThat(count("purchase_orders")).isEqualTo(2);
    }

    @Test
    void foreignKeyIsOnTheManySide() {
        Customer c = saved();
        Integer n = jdbc.queryForObject("select count(*) from purchase_orders where customer_id = ?", Integer.class, c.getId());
        assertThat(n).isEqualTo(2);
    }

    @Test
    void noJoinTableBecauseOfMappedBy() {
        saved();
        Integer n = jdbc.queryForObject("select count(*) from information_schema.tables where table_name like 'customers_%'", Integer.class);
        assertThat(n).isZero();
    }

    @Test
    void orphanRemovalDeletesRemovedOrder() {
        Customer c = saved();
        c.removeOrder(c.getOrders().get(0));
        em.flush();
        assertThat(count("purchase_orders")).isEqualTo(1);
    }

    @Test
    void removingCustomerRemovesOrders() {
        Customer c = saved();
        em.remove(c);
        em.flush();
        assertThat(count("purchase_orders")).isZero();
    }

    @Test
    void manyToOneIsLazy() {
        saved();
        em.clear();
        PurchaseOrder o = em.getEntityManager().createQuery("select o from PurchaseOrder o where o.reference = 'A-1'", PurchaseOrder.class).getSingleResult();
        assertThat(loaded(o, "customer")).isFalse();
    }
}
'''
a2 = tk("one-to-many-orders", "One-to-Many: Customer and Orders", "Core",
    "Build a bidirectional one-to-many: mappedBy inverse side, owning many-to-one, sync helpers, cascade and orphanRemoval.",
    {"main/Application.java": APP, "main/Customer.java": CUST, "main/PurchaseOrder.java": ORD},
    {"test/OneToManyTest.java": T2, **PROPS(2)},
    ["Annotate `Customer.orders` (inverse side) and `PurchaseOrder.customer` (owning side).", "Implement `addOrder`/`removeOrder` so both sides stay consistent."],
    ["Without `mappedBy` Hibernate invents a join table.", "`@ManyToOne` defaults to EAGER; set LAZY.", "orphanRemoval only triggers when the child is removed from the collection."],
    ["The side with the foreign key is the owning side.", "Helpers are the only place that should touch both fields."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 3
STU = HDR + r'''@Entity
@Table(name = "students")
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    //A! owning side of the many-to-many: join table enrollments(student_id, course_id); NO cascade
    @ManyToMany
    @JoinTable(name = "enrollments",
            joinColumns = @JoinColumn(name = "student_id"),
            inverseJoinColumns = @JoinColumn(name = "course_id"))
    //E!
    private Set<Course> courses = new HashSet<>();

    protected Student() {
    }

    public Student(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Set<Course> getCourses() {
        return courses;
    }

    public void enroll(Course course) {
        //B! add to both sides
        courses.add(course);
        course.getStudents().add(this);
        //E!
    }

    public void drop(Course course) {
        //B! remove from both sides
        courses.remove(course);
        course.getStudents().remove(this);
        //E!
    }
}
'''
COU = HDR + r'''@Entity
@Table(name = "courses")
public class Course {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String code;

    private String title;

    //A! inverse side: mappedBy courses
    @ManyToMany(mappedBy = "courses")
    //E!
    private Set<Student> students = new HashSet<>();

    protected Course() {
    }

    public Course(String code, String title) {
        this.code = code;
        this.title = title;
    }

    public Long getId() {
        return id;
    }

    public String getCode() {
        return code;
    }

    public String getTitle() {
        return title;
    }

    public Set<Student> getStudents() {
        return students;
    }

    /** Business-key equality: two courses are equal when their codes are equal (and non-null). */
    @Override
    public boolean equals(Object o) {
        //B! equal when same class and equal code
        if (this == o) {
            return true;
        }
        if (!(o instanceof Course other)) {
            return false;
        }
        return code != null && code.equals(other.code);
        //E!
    }

    @Override
    public int hashCode() {
        //B! consistent with equals (use the code)
        return Objects.hashCode(code);
        //E!
    }
}
'''
T3 = TEST_HDR + r'''class ManyToManyTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    JdbcTemplate jdbc;

''' + CNT + r'''
    private Course course(String code) {
        return em.persist(new Course(code, "T-" + code));
    }

    @Test
    void enrollWritesJoinTableRows() {
        Course java = course("JAVA");
        Course sql = course("SQL");
        Student ann = new Student("Ann");
        ann.enroll(java);
        ann.enroll(sql);
        em.persistAndFlush(ann);
        assertThat(count("enrollments")).isEqualTo(2);
        assertThat(java.getStudents()).containsExactly(ann);
    }

    @Test
    void dropRemovesOnlyTheLink() {
        Course java = course("JAVA");
        Student ann = new Student("Ann");
        ann.enroll(java);
        em.persistAndFlush(ann);
        ann.drop(java);
        em.flush();
        assertThat(count("enrollments")).isZero();
        assertThat(count("courses")).isEqualTo(1);
        assertThat(java.getStudents()).isEmpty();
    }

    @Test
    void deletingStudentKeepsCoursesButClearsLinks() {
        Course java = course("JAVA");
        Student ann = new Student("Ann");
        ann.enroll(java);
        em.persistAndFlush(ann);
        em.remove(ann);
        em.flush();
        assertThat(count("enrollments")).isZero();
        assertThat(count("courses")).isEqualTo(1);
    }

    @Test
    void noCascadeFromStudentToCourse() {
        Student ann = new Student("Ann");
        ann.enroll(new Course("NEW", "not persisted"));
        assertThatThrownBy(() -> em.persistAndFlush(ann)).isInstanceOf(RuntimeException.class);
    }

    @Test
    void courseEqualityUsesBusinessKey() {
        Course a = new Course("J1", "x");
        Course b = new Course("J1", "y");
        assertThat(a).isEqualTo(b).hasSameHashCodeAs(b);
        assertThat(a).isNotEqualTo(new Course("J2", "x")).isNotEqualTo(null).isNotEqualTo("J1");
        assertThat(new java.util.HashSet<>(java.util.List.of(a, b))).hasSize(1);
        assertThat(new Course(null, "x")).isNotEqualTo(new Course(null, "x"));
    }
}
'''
a3 = tk("many-to-many-enrollment", "Many-to-Many: Students and Courses", "Core",
    "Model many-to-many with an explicit join table, helper methods, no accidental cascade, and business-key equals/hashCode.",
    {"main/Application.java": APP, "main/Student.java": STU, "main/Course.java": COU},
    {"test/ManyToManyTest.java": T3, **PROPS(3)},
    ["Map `Student.courses` (owning, join table `enrollments`) and `Course.students` (inverse).", "Implement `enroll`/`drop` and `Course.equals/hashCode` on the business key `code`."],
    ["Never cascade REMOVE on many-to-many: it deletes shared rows.", "Use `Set`, not `List`, to avoid delete-all/re-insert of join rows.", "Two courses with null codes are not equal."],
    ["`mappedBy` points at the field name on the owning side.", "`Objects.hashCode(code)` is null-safe."],
    S, deps=DEPS)

# ------------------------------------------------------------ task 4
AUT = HDR + r'''@Entity
@Table(name = "authors")
public class Author {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    //A! inverse one-to-many to Book (mappedBy author, cascade ALL, orphanRemoval, LAZY)
    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    //E!
    private List<Book> books = new ArrayList<>();

    protected Author() {
    }

    public Author(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<Book> getBooks() {
        return books;
    }

    public void addBook(Book book) {
        //B! add and set back reference
        books.add(book);
        book.setAuthor(this);
        //E!
    }

    public void removeBook(Book book) {
        //B! remove and clear back reference
        books.remove(book);
        book.setAuthor(null);
        //E!
    }
}
'''
BKK = HDR + r'''@Entity
@Table(name = "books")
public class Book {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;

    //A! many-to-one to Author: LAZY, join column author_id, not nullable
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "author_id", nullable = false)
    //E!
    private Author author;

    //A! one-to-one to BookDetail owned by Book: LAZY, cascade ALL, orphanRemoval, join column detail_id
    @OneToOne(fetch = FetchType.LAZY, cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "detail_id")
    //E!
    private BookDetail detail;

    //A! many-to-many to Tag through join table book_tags(book_id, tag_id); no cascade
    @ManyToMany
    @JoinTable(name = "book_tags", joinColumns = @JoinColumn(name = "book_id"), inverseJoinColumns = @JoinColumn(name = "tag_id"))
    //E!
    private Set<Tag> tags = new HashSet<>();

    protected Book() {
    }

    public Book(String title, int pages) {
        this.title = title;
        this.detail = new BookDetail(pages);
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public Author getAuthor() {
        return author;
    }

    void setAuthor(Author author) {
        this.author = author;
    }

    public BookDetail getDetail() {
        return detail;
    }

    public Set<Tag> getTags() {
        return tags;
    }

    public void tag(Tag tag) {
        //B! add to both sides
        tags.add(tag);
        tag.getBooks().add(this);
        //E!
    }
}
'''
BDET = HDR + r'''@Entity
@Table(name = "book_details")
public class BookDetail {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int pages;

    protected BookDetail() {
    }

    public BookDetail(int pages) {
        this.pages = pages;
    }

    public Long getId() {
        return id;
    }

    public int getPages() {
        return pages;
    }
}
'''
TAG = HDR + r'''@Entity
@Table(name = "tags")
public class Tag {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    //A! inverse many-to-many (mappedBy tags)
    @ManyToMany(mappedBy = "tags")
    //E!
    private Set<Book> books = new HashSet<>();

    protected Tag() {
    }

    public Tag(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Set<Book> getBooks() {
        return books;
    }
}
'''
T4 = TEST_HDR + r'''class LibraryModelTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    JdbcTemplate jdbc;

''' + CNT + r'''
    private Author saved() {
        Tag java = em.persist(new Tag("java"));
        Tag spring = em.persist(new Tag("spring"));
        Author a = new Author("Ann");
        Book b1 = new Book("JPA", 300);
        Book b2 = new Book("Boot", 200);
        b1.tag(java);
        b1.tag(spring);
        b2.tag(spring);
        a.addBook(b1);
        a.addBook(b2);
        return em.persistAndFlush(a);
    }

    @Test
    void cascadesFromAuthorThroughBooksToDetails() {
        saved();
        assertThat(count("books")).isEqualTo(2);
        assertThat(count("book_details")).isEqualTo(2);
        assertThat(count("book_tags")).isEqualTo(3);
        assertThat(count("tags")).isEqualTo(2);
    }

    @Test
    void associationsAreLazy() {
        Author a = saved();
        em.clear();
        Author found = em.find(Author.class, a.getId());
        assertThat(loaded(found, "books")).isFalse();
        Long bookId = found.getBooks().get(0).getId();
        em.clear();
        Book fresh = em.find(Book.class, bookId);
        assertThat(loaded(fresh, "author")).isFalse();
        assertThat(loaded(fresh, "detail")).isFalse();
        assertThat(loaded(fresh, "tags")).isFalse();
    }

    @Test
    void removingBookRemovesItsDetailButNotTags() {
        Author a = saved();
        a.removeBook(a.getBooks().get(0));
        em.flush();
        assertThat(count("books")).isEqualTo(1);
        assertThat(count("book_details")).isEqualTo(1);
        assertThat(count("tags")).isEqualTo(2);
        assertThat(count("book_tags")).isEqualTo(1);
    }

    @Test
    void removingAuthorRemovesBooksAndDetailsButKeepsTags() {
        Author a = saved();
        em.remove(a);
        em.flush();
        assertThat(count("books")).isZero();
        assertThat(count("book_details")).isZero();
        assertThat(count("book_tags")).isZero();
        assertThat(count("tags")).isEqualTo(2);
    }

    @Test
    void tagKnowsItsBooks() {
        Author a = saved();
        Tag spring = a.getBooks().get(0).getTags().stream().filter(t -> t.getName().equals("spring")).findFirst().orElseThrow();
        assertThat(spring.getBooks()).hasSize(2);
    }
}
'''
a4 = tk("library-model-challenge", "Library Model: 1:1, 1:N and N:M Together", "Challenge",
    "Combine all three relationship types in one aggregate and decide cascade, orphanRemoval and fetch settings for each edge.",
    {"main/Application.java": APP, "main/Author.java": AUT, "main/Book.java": BKK, "main/BookDetail.java": BDET, "main/Tag.java": TAG},
    {"test/LibraryModelTest.java": T4, **PROPS(4)},
    ["Map `Author.books`, `Book.author`, `Book.detail`, `Book.tags` and `Tag.books`.", "Implement `addBook`, `removeBook`, `tag`.", "Decide where cascade is safe (author->book->detail) and where it is not (tags)."],
    ["Removing an author must not remove shared tags.", "All associations must be LAZY at runtime.", "`orphanRemoval` on Book.detail removes details together with removed books."],
    ["Think in aggregates: Author owns Books, Books own details; Tags are shared references.", "Reuse patterns from tasks 1-3."],
    S, deps=DEPS)

topics = [
    T("One-to-one, one-to-many and many-to-one",
      "Relationships are mapped with `@OneToOne`, `@OneToMany`, `@ManyToOne`. The **owning side** holds the foreign key (`@JoinColumn`); the **inverse side** uses `mappedBy`. A bidirectional one-to-many is owned by the `@ManyToOne` side. Convenience methods (`addOrder`, `removeOrder`) keep both in-memory sides consistent.",
      "Relational data is connected by keys; the object model needs references. Correct ownership decides which table gets the FK and whether Hibernate generates extra join tables.",
      ["Navigate relations as object references", "Cascade lifecycle operations along aggregates", "FK constraints enforced by the DB", "orphanRemoval models true composition"],
      ["Bidirectional associations require discipline", "Easy to create N+1 problems (Day 35)", "Mistaken ownership gives silent no-ops (no FK written)"],
      "Setting only the inverse side (`customer.getOrders().add(o)`) writes nothing because the owning side `o.customer` is still null. Without `mappedBy` a one-to-many creates an unwanted join table.",
      "```java\n@OneToMany(mappedBy = \"customer\", cascade = CascadeType.ALL, orphanRemoval = true)\nprivate List<PurchaseOrder> orders = new ArrayList<>();\n\n@ManyToOne(fetch = FetchType.LAZY, optional = false)\n@JoinColumn(name = \"customer_id\", nullable = false)\nprivate Customer customer;\n```\nDefaults: `@ManyToOne`/`@OneToOne` EAGER, `@OneToMany`/`@ManyToMany` LAZY.",
      [("Helper", "java", "public void addOrder(PurchaseOrder o) { orders.add(o); o.setCustomer(this); }"),
       ("One-to-one", "java", "@OneToOne(fetch = LAZY, cascade = ALL, orphanRemoval = true)\n@JoinColumn(name = \"profile_id\")\nprivate Profile profile;"),
       ("Unidirectional one-to-many (avoid)", "java", "@OneToMany @JoinColumn(name = \"customer_id\") List<Order> orders;   // extra UPDATEs")],
      [("Which side owns a bidirectional one-to-many?", "The many-to-one side (it has the FK)."),
       ("What does mappedBy tell Hibernate?", "That the other side owns the relationship and no join table is needed."),
       ("Default fetch of @ManyToOne?", "EAGER - usually override to LAZY.")]),
    T("Many-to-many and join tables",
      "`@ManyToMany` maps a link table. The owning side declares `@JoinTable` with `joinColumns` and `inverseJoinColumns`; the other side uses `mappedBy`. Use `Set` to avoid re-inserting all rows on changes. When the link has attributes (enrolled_at, grade), model it as an explicit entity with two `@ManyToOne`.",
      "Many-to-many exists everywhere (students/courses, posts/tags, users/roles). Correct mapping prevents duplicate links and accidental deletes of shared data.",
      ["Concise for pure links", "Join table managed automatically", "Works naturally with Sets"],
      ["No place for link attributes", "Cascade REMOVE is dangerous", "Large collections load entirely when initialized"],
      "Cascading REMOVE across a many-to-many deletes entities other aggregates still reference. Using `List` can make Hibernate delete and re-insert every link row for one change. Mutable-field equals/hashCode breaks HashSet membership.",
      "```java\n@ManyToMany\n@JoinTable(name = \"enrollments\",\n    joinColumns = @JoinColumn(name = \"student_id\"),\n    inverseJoinColumns = @JoinColumn(name = \"course_id\"))\nprivate Set<Course> courses = new HashSet<>();\n```\nEquality: prefer a business key (`code`) or a stable id strategy; never include lazy collections in equals/hashCode.",
      [("Inverse side", "java", "@ManyToMany(mappedBy = \"courses\")\nprivate Set<Student> students = new HashSet<>();"),
       ("Link entity", "java", "@Entity class Enrollment {\n  @ManyToOne Student student; @ManyToOne Course course; LocalDate enrolledAt; int grade; }"),
       ("Business-key equals", "java", "public boolean equals(Object o) { return o instanceof Course c && code != null && code.equals(c.code); }")],
      [("Set or List for many-to-many?", "Set, to avoid delete-all/insert-all of link rows."),
       ("What if the link needs attributes?", "Make an explicit link entity."),
       ("Should many-to-many cascade REMOVE?", "No.")]),
    T("Cascade, orphanRemoval and fetch types",
      "**Cascade** propagates persist/merge/remove/refresh/detach from parent to children (`CascadeType.ALL`). **orphanRemoval** deletes a child removed from the parent's collection or replaced. **FetchType** LAZY loads on first access via proxies/uninitialized collections; EAGER loads together with the owner. Lazy access outside a session throws `LazyInitializationException`.",
      "Aggregates (order + lines) share a lifecycle: cascade avoids saving each child manually. Fetch strategy controls performance: eager associations multiply queries and joins.",
      ["Simplifies aggregate persistence", "orphanRemoval models composition cleanly", "LAZY avoids loading unused graphs"],
      ["Cascade across shared references deletes too much", "LAZY requires fetching strategy awareness (join fetch, entity graphs)", "orphanRemoval + replacing a collection instance breaks (mutate it instead)"],
      "EAGER everywhere loads half the database per query. Cascade ALL on a shared reference deletes data other rows still need. Replacing (`setOrders(new ArrayList<>())`) a collection with orphanRemoval throws `HibernateException: A collection with cascade=all-delete-orphan was no longer referenced`.",
      "```java\n@OneToMany(mappedBy = \"author\", cascade = CascadeType.ALL, orphanRemoval = true) // aggregate children\n@ManyToMany                                                                      // shared: no cascade\n```\nCheck loading state in tests: `PersistenceUnitUtil.isLoaded(entity, \"attribute\")`.",
      [("Aggregate", "text", "Author -> Books -> BookDetail   (cascade ALL + orphanRemoval)\nBook <-> Tag                    (no cascade, shared)"),
       ("Lazy check", "java", "emf.getPersistenceUnitUtil().isLoaded(book, \"author\")"),
       ("Safe collection update", "java", "author.getBooks().clear(); author.getBooks().addAll(newBooks);")],
      [("What does orphanRemoval do?", "Deletes children removed from the parent collection or replaced."),
       ("Why LAZY by default?", "To avoid loading unnecessary graphs and N+1 explosions with eager joins."),
       ("When must you not use CascadeType.REMOVE?", "On references shared with other aggregates (e.g. tags).")]),
]

day(34, "Spring Data JPA III: Relationships, Cascade and Fetching", "Spring Boot",
    "Mapping associations between entities: ownership, join tables, cascading and lazy/eager loading",
    ["Map 1:1, 1:N/N:1 and N:M relationships", "Explain owning vs inverse side and mappedBy", "Choose cascade, orphanRemoval and fetch strategies", "Verify mappings with @DataJpaTest, JdbcTemplate and PersistenceUnitUtil"],
    ["Day 33 queries and projections"],
    topics, [a1, a2, a3, a4],
    [("Owning vs inverse side?", "Owning side has the FK/join table; inverse uses mappedBy."),
     ("Why helper methods?", "To keep both in-memory sides in sync."),
     ("Cascade vs orphanRemoval?", "Cascade propagates operations; orphanRemoval deletes removed children."),
     ("Default fetch types?", "To-one EAGER, to-many LAZY."),
     ("LazyInitializationException?", "Accessing a lazy association after the session closed.")],
    ["Setting only the inverse side.", "Cascade REMOVE on shared entities.", "List instead of Set for many-to-many.", "Replacing an orphanRemoval collection instance."],
    ["Hibernate ORM User Guide: Associations", "Spring Data JPA Reference"],
    [("Owning side", "Side whose table holds the FK"), ("mappedBy", "Marks the inverse side"), ("Cascade", "Propagating operations"),
     ("orphanRemoval", "Delete removed children"), ("Join table", "Link table for N:M")],
    "2–3 h theory + 3–5 h tasks", spring=True)
