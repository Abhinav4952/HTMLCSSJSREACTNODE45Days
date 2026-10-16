from common import *

H2RT = dep("com.h2database", "h2", None, "runtime")
NFE = "package %PKG%;\n\n/** PROVIDED. Maps to HTTP 404. */\npublic class NotFoundException extends RuntimeException {\n\n    public NotFoundException(String message) {\n        super(message);\n    }\n}\n"
FBE = "package %PKG%;\n\n/** PROVIDED. Maps to HTTP 403. */\npublic class ForbiddenException extends RuntimeException {\n\n    public ForbiddenException(String message) {\n        super(message);\n    }\n}\n"

# ---- task 1: ownership guard
GUARD = r'''package %PKG%;

import java.util.Optional;

/** Object-level authorization: who may touch a resource, and what do we reveal when they may not? */
public class OwnershipGuard {

    public enum DenialPolicy {
        /** Existence is hidden: non-owners get the same answer as for a missing resource (404). */
        HIDE_AS_404,
        /** Honest answer: the resource exists but you may not touch it (403). */
        FORBID_403
    }

    private final DenialPolicy policy;

    public OwnershipGuard(DenialPolicy policy) {
        this.policy = policy;
    }

    /**
     * empty -> NotFoundException; owner or admin -> the resource;
     * other callers -> NotFoundException (HIDE_AS_404) or ForbiddenException (FORBID_403).
     */
    public Resource require(Optional<Resource> found, long callerId, boolean admin) {
        // TODO(%TAG%): implement the decision table above
        throw new UnsupportedOperationException("TODO(%TAG%): implement require");
    }
}
'''
GUARD_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.Optional;
import org.junit.jupiter.api.Test;

class OwnershipGuardTest {

    private final Resource doc = new Resource(1L, 10L);
    private final OwnershipGuard hide = new OwnershipGuard(OwnershipGuard.DenialPolicy.HIDE_AS_404);
    private final OwnershipGuard forbid = new OwnershipGuard(OwnershipGuard.DenialPolicy.FORBID_403);

    @Test
    void ownerGetsTheResource() {
        assertThat(hide.require(Optional.of(doc), 10L, false)).isSameAs(doc);
        assertThat(forbid.require(Optional.of(doc), 10L, false)).isSameAs(doc);
    }

    @Test
    void adminGetsTheResource() {
        assertThat(hide.require(Optional.of(doc), 99L, true)).isSameAs(doc);
        assertThat(forbid.require(Optional.of(doc), 99L, true)).isSameAs(doc);
    }

    @Test
    void missingResourceIsAlways404() {
        assertThatThrownBy(() -> hide.require(Optional.empty(), 10L, false)).isInstanceOf(NotFoundException.class);
        assertThatThrownBy(() -> forbid.require(Optional.empty(), 10L, true)).isInstanceOf(NotFoundException.class);
    }

    @Test
    void strangerIsHiddenUnderHidePolicy() {
        assertThatThrownBy(() -> hide.require(Optional.of(doc), 99L, false)).isInstanceOf(NotFoundException.class);
    }

    @Test
    void strangerIsForbiddenUnderForbidPolicy() {
        assertThatThrownBy(() -> forbid.require(Optional.of(doc), 99L, false)).isInstanceOf(ForbiddenException.class);
    }

    @Test
    void messagesDoNotLeakTheOwner() {
        assertThatThrownBy(() -> hide.require(Optional.of(doc), 99L, false)).hasMessageNotContaining("10");
        assertThatThrownBy(() -> forbid.require(Optional.of(doc), 99L, false)).hasMessageNotContaining("10");
    }
}
'''
o1 = task("ownership-guard", "Ownership Guard: 403 vs 404 Policy", "Warm-up", "Java",
    "Encode the object-level authorization decision table (owner, admin, stranger, missing) and the two classic disclosure policies.",
    "plain", {"main/Resource.java": "package %PKG%;\n\n/** PROVIDED. */\npublic record Resource(long id, long ownerId) {\n}\n", "main/NotFoundException.java": NFE, "main/ForbiddenException.java": FBE,
              "main/OwnershipGuard.java": GUARD, "test/OwnershipGuardTest.java": GUARD_TEST},
    ["Missing resource -> `NotFoundException` regardless of caller.", "Owner or admin -> return the resource.", "Stranger -> 404 (hide) or 403 (forbid) depending on the policy.", "Exception messages must not reveal the owner id."],
    ["Admin on a missing resource still gets 404.", "Messages leaking internals."],
    ["Use a `switch` on the enum for the denial."])

# ---- task 2: pagination
NOTE = r'''package %PKG%;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.LocalDateTime;

/** PROVIDED. */
@Entity
@Table(name = "notes")
public class Note {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "owner_id", nullable = false)
    private Long ownerId;

    @Column(nullable = false)
    private String title;

    @Column(name = "created_at", nullable = false)
    private LocalDateTime createdAt;

    protected Note() {
    }

    public Note(Long ownerId, String title, LocalDateTime createdAt) {
        this.ownerId = ownerId;
        this.title = title;
        this.createdAt = createdAt;
    }

    public Long getId() {
        return id;
    }

    public Long getOwnerId() {
        return ownerId;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }
}
'''
NREPO = "package %PKG%;\n\nimport org.springframework.data.domain.Page;\nimport org.springframework.data.domain.Pageable;\nimport org.springframework.data.jpa.repository.JpaRepository;\n\n/** PROVIDED. */\npublic interface NoteRepository extends JpaRepository<Note, Long> {\n\n    Page<Note> findByOwnerIdAndTitleContainingIgnoreCase(Long ownerId, String titlePart, Pageable pageable);\n}\n"
PAGE = "package %PKG%;\n\nimport java.util.List;\n\n/** PROVIDED. Stable JSON shape for paged results. */\npublic record PageResponse<T>(List<T> content, int page, int size, long totalElements, int totalPages) {\n}\n"
SEARCH = r'''package %PKG%;

import java.util.Set;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class NoteSearchService {

    public static final int MAX_SIZE = 50;
    private static final Set<String> SORTABLE = Set.of("createdAt", "title");

    private final NoteRepository notes;

    public NoteSearchService(NoteRepository notes) {
        this.notes = notes;
    }

    /**
     * Owner-scoped, paged, sorted title search.
     * <ul>
     *   <li>page &lt; 0 or size &lt; 1 -> IllegalArgumentException; size is clamped to MAX_SIZE</li>
     *   <li>sortBy must be in {createdAt, title} (whitelist!) else IllegalArgumentException; direction "asc"/"desc" (any case), else IAE</li>
     *   <li>null query is treated as ""; returned PageResponse reports the EFFECTIVE (clamped) size</li>
     * </ul>
     */
    @Transactional(readOnly = true)
    public PageResponse<Note> search(Long ownerId, String query, int page, int size, String sortBy, String direction) {
        // TODO(%TAG%): validate, build PageRequest.of(page, size, Sort.by(dir, sortBy)), query the repository, map the Page
        throw new UnsupportedOperationException("TODO(%TAG%): implement search");
    }
}
'''
SEARCH_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.LocalDateTime;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(NoteSearchService.class)
class NoteSearchServiceTest {

    @Autowired
    private NoteRepository repo;
    @Autowired
    private NoteSearchService service;

    @BeforeEach
    void seed() {
        LocalDateTime base = LocalDateTime.of(2025, 1, 1, 0, 0);
        for (int i = 1; i <= 12; i++) {
            repo.save(new Note(1L, String.format("Note %02d", i), base.plusMinutes(i)));
        }
        for (int i = 1; i <= 3; i++) {
            repo.save(new Note(2L, "Other " + i, base.plusMinutes(i)));
        }
    }

    @Test
    void pagesAndTotalsAreReported() {
        PageResponse<Note> p = service.search(1L, "note", 0, 5, "title", "asc");
        assertThat(p.content()).hasSize(5);
        assertThat(p.totalElements()).isEqualTo(12);
        assertThat(p.totalPages()).isEqualTo(3);
        assertThat(p.content().get(0).getTitle()).isEqualTo("Note 01");
        assertThat(service.search(1L, "note", 2, 5, "title", "asc").content()).hasSize(2);
    }

    @Test
    void sortsByCreatedAtDescending() {
        PageResponse<Note> p = service.search(1L, "", 0, 3, "createdAt", "DESC");
        assertThat(p.content()).extracting(Note::getTitle).containsExactly("Note 12", "Note 11", "Note 10");
    }

    @Test
    void searchIsScopedToTheOwner() {
        assertThat(service.search(2L, null, 0, 10, "title", "asc").totalElements()).isEqualTo(3);
        assertThat(service.search(2L, "note", 0, 10, "title", "asc").totalElements()).isZero();
    }

    @Test
    void sizeIsClamped() {
        assertThat(service.search(1L, "", 0, 1000, "title", "asc").size()).isEqualTo(NoteSearchService.MAX_SIZE);
    }

    @Test
    void invalidArgumentsAreRejected() {
        assertThatThrownBy(() -> service.search(1L, "", -1, 5, "title", "asc")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.search(1L, "", 0, 0, "title", "asc")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.search(1L, "", 0, 5, "ownerId", "asc")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.search(1L, "", 0, 5, "title", "sideways")).isInstanceOf(IllegalArgumentException.class);
    }
}
'''
o2 = task("paged-note-search", "Owner-Scoped Paged Search", "Core", "Spring Boot (JPA)",
    "Build the capstone's list endpoint logic: owner scoping, pagination, whitelisted sorting and a stable page envelope.",
    "boot", {"main/Application.java": APP, "main/Note.java": NOTE, "main/NoteRepository.java": NREPO, "main/PageResponse.java": PAGE, "main/NoteSearchService.java": SEARCH,
             "test/NoteSearchServiceTest.java": SEARCH_TEST},
    ["Validate page, size, sort field (whitelist) and direction.", "Clamp size to `MAX_SIZE`.", "Query by owner and case-insensitive title fragment through the repository.", "Return a `PageResponse` with the effective page size."],
    ["Null query.", "Sorting by a field that must not be exposed (e.g. `ownerId`).", "Huge page size."],
    ["`Sort.Direction.fromString` throws IAE for bad values (wrap or rely on it).", "`Page#getTotalPages()` and `getTotalElements()`."],
    starters=["spring-boot-starter-data-jpa"], deps=[H2RT])

# ---- task 3: error contract
CTRL = r'''package %PKG%;

import jakarta.validation.Valid;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED. Endpoints that deliberately fail in different ways. */
@RestController
@RequestMapping("/things")
public class ThingController {

    public record CreateThing(@NotBlank String name, @Min(1) int quantity) {
    }

    @GetMapping("/{id}")
    public Map<String, Object> get(@PathVariable long id) {
        if (id == 0) {
            throw new NotFoundException("thing 0 not found");
        }
        if (id == 403) {
            throw new ForbiddenException("not your thing");
        }
        if (id == 99) {
            throw new IllegalStateException("db password is hunter2");
        }
        return Map.of("id", id);
    }

    @PostMapping
    public Map<String, Object> create(@Valid @RequestBody CreateThing body) {
        return Map.of("name", body.name());
    }
}
'''
GEH = r'''package %PKG%;

import org.springframework.http.ProblemDetail;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * One consistent error contract (RFC 9457 ProblemDetail). Every response must set status, title (the HTTP reason
 * phrase, e.g. "Not Found") and detail.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    /** 404, detail = exception message. */
    @ExceptionHandler(NotFoundException.class)
    public ProblemDetail handleNotFound(NotFoundException ex) {
        // TODO(%TAG%): ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ...) + title
        throw new UnsupportedOperationException("TODO(%TAG%): implement handleNotFound");
    }

    /** 403, detail = exception message. */
    @ExceptionHandler(ForbiddenException.class)
    public ProblemDetail handleForbidden(ForbiddenException ex) {
        // TODO(%TAG%): 403 problem detail
        throw new UnsupportedOperationException("TODO(%TAG%): implement handleForbidden");
    }

    /** 400, detail "Validation failed", property "errors" = map field name -> first message. */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        // TODO(%TAG%): collect ex.getBindingResult().getFieldErrors() into a LinkedHashMap and setProperty("errors", map)
        throw new UnsupportedOperationException("TODO(%TAG%): implement handleValidation");
    }

    /** 400, detail "Malformed request body" (never echo the parser message). */
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ProblemDetail handleUnreadable(HttpMessageNotReadableException ex) {
        // TODO(%TAG%): 400 problem detail
        throw new UnsupportedOperationException("TODO(%TAG%): implement handleUnreadable");
    }

    /** 500, detail "Unexpected error" - NEVER include the exception message (it may contain secrets). Log it instead. */
    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnexpected(Exception ex) {
        // TODO(%TAG%): log the exception, return a generic 500 problem detail
        throw new UnsupportedOperationException("TODO(%TAG%): implement handleUnexpected");
    }
}
'''
EC_TEST = r'''package %PKG%;

import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.not;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ThingController.class)
class ErrorContractTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void okPathStillWorks() throws Exception {
        mvc.perform(get("/things/5")).andExpect(status().isOk()).andExpect(jsonPath("$.id").value(5));
    }

    @Test
    void notFoundIsAProblemDetail() throws Exception {
        mvc.perform(get("/things/0")).andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.title").value("Not Found"))
                .andExpect(jsonPath("$.detail").value("thing 0 not found"));
    }

    @Test
    void forbiddenIsAProblemDetail() throws Exception {
        mvc.perform(get("/things/403")).andExpect(status().isForbidden())
                .andExpect(jsonPath("$.status").value(403))
                .andExpect(jsonPath("$.title").value("Forbidden"))
                .andExpect(jsonPath("$.detail").value("not your thing"));
    }

    @Test
    void unexpectedErrorsDoNotLeakDetails() throws Exception {
        mvc.perform(get("/things/99")).andExpect(status().isInternalServerError())
                .andExpect(jsonPath("$.status").value(500))
                .andExpect(jsonPath("$.detail").value("Unexpected error"))
                .andExpect(content().string(not(containsString("hunter2"))));
    }

    @Test
    void validationErrorsListFields() throws Exception {
        mvc.perform(post("/things").contentType(MediaType.APPLICATION_JSON).content("{\"name\":\"\",\"quantity\":0}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.status").value(400))
                .andExpect(jsonPath("$.detail").value("Validation failed"))
                .andExpect(jsonPath("$.errors.name").exists())
                .andExpect(jsonPath("$.errors.quantity").exists());
    }

    @Test
    void malformedJsonIs400WithoutParserDetails() throws Exception {
        mvc.perform(post("/things").contentType(MediaType.APPLICATION_JSON).content("{bad"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.detail").value("Malformed request body"));
    }
}
'''
o3 = task("error-contract", "Global Error Contract (ProblemDetail)", "Core", "Spring Boot (Web)",
    "Replace ad-hoc error responses with one RFC 9457 `ProblemDetail` contract: consistent fields, field-level validation errors and no information leaks.",
    "boot", {"main/Application.java": APP, "main/NotFoundException.java": NFE, "main/ForbiddenException.java": FBE, "main/ThingController.java": CTRL,
             "main/GlobalExceptionHandler.java": GEH, "test/ErrorContractTest.java": EC_TEST},
    ["404 and 403 handlers with status/title/detail.", "Validation handler with an `errors` object (field -> message).", "Malformed JSON handler with a generic detail.", "Catch-all 500 handler that logs and returns a generic message."],
    ["Secret text inside exception messages.", "Several violations on one field (keep the first).", "Specific handlers must win over the catch-all."],
    ["`ProblemDetail.forStatusAndDetail(HttpStatus.X, detail)` then `setTitle(...)`.", "`HttpStatus.NOT_FOUND.getReasonPhrase()`."],
    starters=["spring-boot-starter-web", "spring-boot-starter-validation"])

# ---- task 5 (challenge): NoteService
NSVC = r'''package %PKG%;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class NoteService {

    private final NoteRepository notes;

    public NoteService(NoteRepository notes) {
        this.notes = notes;
    }

    /** Owner or admin may read; everyone else (and missing ids) get NotFoundException (policy: hide existence). */
    @Transactional(readOnly = true)
    public Note get(long callerId, boolean admin, long noteId) {
        // TODO(%TAG%): load the note and apply the ownership rule
        throw new UnsupportedOperationException("TODO(%TAG%): implement get");
    }

    /** Same access rule as get; blank title -> IllegalArgumentException (checked BEFORE touching the database). Persists the change. */
    @Transactional
    public Note rename(long callerId, boolean admin, long noteId, String newTitle) {
        // TODO(%TAG%): validate, authorize, change the title, save
        throw new UnsupportedOperationException("TODO(%TAG%): implement rename");
    }

    /** Owner or admin may delete; others get NotFoundException and the row survives. */
    @Transactional
    public void delete(long callerId, boolean admin, long noteId) {
        // TODO(%TAG%): authorize and delete
        throw new UnsupportedOperationException("TODO(%TAG%): implement delete");
    }
}
'''
NSVC_TEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.time.LocalDateTime;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(NoteService.class)
class NoteServiceTest {

    @Autowired
    private NoteRepository repo;
    @Autowired
    private NoteService service;

    private long noteId;

    @BeforeEach
    void seed() {
        noteId = repo.save(new Note(1L, "private plans", LocalDateTime.of(2025, 1, 1, 0, 0))).getId();
    }

    @Test
    void ownerCanReadRenameAndDelete() {
        assertThat(service.get(1L, false, noteId).getTitle()).isEqualTo("private plans");
        assertThat(service.rename(1L, false, noteId, "public plans").getTitle()).isEqualTo("public plans");
        assertThat(repo.findById(noteId).orElseThrow().getTitle()).isEqualTo("public plans");
        service.delete(1L, false, noteId);
        assertThat(repo.existsById(noteId)).isFalse();
    }

    @Test
    void strangerSeesNotFoundForEverything() {
        assertThatThrownBy(() -> service.get(2L, false, noteId)).isInstanceOf(NotFoundException.class);
        assertThatThrownBy(() -> service.rename(2L, false, noteId, "hacked")).isInstanceOf(NotFoundException.class);
        assertThatThrownBy(() -> service.delete(2L, false, noteId)).isInstanceOf(NotFoundException.class);
        assertThat(repo.findById(noteId).orElseThrow().getTitle()).isEqualTo("private plans");
    }

    @Test
    void adminCanAccessAnyNote() {
        assertThat(service.get(99L, true, noteId).getId()).isEqualTo(noteId);
        service.delete(99L, true, noteId);
        assertThat(repo.existsById(noteId)).isFalse();
    }

    @Test
    void unknownIdIsNotFound() {
        assertThatThrownBy(() -> service.get(1L, true, 123456L)).isInstanceOf(NotFoundException.class);
    }

    @Test
    void blankTitleIsRejectedBeforeAnyLookup() {
        assertThatThrownBy(() -> service.rename(2L, false, noteId, "  ")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.rename(1L, false, noteId, null)).isInstanceOf(IllegalArgumentException.class);
    }
}
'''
o4 = task("note-service-ownership-challenge", "Ownership-Enforcing Note Service (Challenge)", "Challenge", "Spring Boot (JPA)",
    "Integrate ownership checks with JPA: read, rename and delete notes with a hide-existence policy, admin override and validation order.",
    "boot", {"main/Application.java": APP, "main/Note.java": NOTE, "main/NoteRepository.java": NREPO, "main/NotFoundException.java": NFE, "main/NoteService.java": NSVC, "test/NoteServiceTest.java": NSVC_TEST},
    ["`get`, `rename`, `delete` enforce: owner or admin only; strangers and missing ids both yield `NotFoundException`.", "`rename` validates the title first (IAE), then authorizes, then persists.", "Failed authorization must leave data untouched."],
    ["Unknown id.", "Admin on someone else's note.", "Validation vs authorization order."],
    ["Write one private `loadAuthorized(callerId, admin, id)` helper and reuse it.", "Inside `@Transactional`, changing a managed entity is persisted at commit; `save` makes intent explicit."],
    starters=["spring-boot-starter-data-jpa"], deps=[H2RT])

TOPICS = [
    T("Object-level authorization and the ownership model",
      "Authentication and role checks are not enough: a logged-in USER must only touch **their own** records (OWASP API1: Broken Object Level Authorization). Every query/command that loads a resource by id must verify ownership (or admin) in the service layer.",
      "The most common API breach is changing an id in the URL and reading someone else's data. Role rules (`hasRole`) cannot express 'this note belongs to caller'.",
      ["Closes IDOR/BOLA vulnerabilities", "Policy is explicit and testable", "Centralizable in one guard/service helper"],
      ["Must be applied on every access path (including bulk and search)", "Tempting to forget in new endpoints"],
      "Without ownership checks, `GET /notes/123` returns any user's note; scoping only list endpoints but not detail endpoints is a classic gap.",
      "Pattern: `repo.findById(id).filter(n -> admin || n.ownerId == caller).orElseThrow(NotFound)`. Or scope queries: `findByIdAndOwnerId`.\n**403 vs 404 policy:** 404 hides that the resource exists (preferred for private data); 403 is more honest and easier to debug. Pick one policy per API and document it.",
      [("Scoped query", "java", "Optional<Note> n = repo.findByIdAndOwnerId(id, callerId);"),
       ("Guard", "java", "if (!admin && note.getOwnerId() != caller) throw new NotFoundException(\"note not found\");")],
      [("What is BOLA/IDOR?", "Accessing objects of other users by guessing/changing identifiers."),
       ("Why can 403 leak information?", "It confirms that the id exists.")]),
    T("Pagination, sorting, and filtering",
      "List endpoints must never return unbounded data. Spring Data's `Pageable`/`Page<T>` provide page index, size, sort and totals. Expose a stable envelope (`content`, `page`, `size`, `totalElements`, `totalPages`) rather than the raw `Page` type.",
      "Unbounded lists exhaust memory and DB; arbitrary sort fields leak or break queries.",
      ["Predictable memory/latency", "Standard client contract", "Sort/filter in the database"],
      ["Offset pagination gets slow on deep pages (use keyset for huge data)", "Counting total rows costs a query"],
      "Accepting `size=1000000` or `sort=passwordHash` from the client is a DoS and a data-exposure bug.",
      "```java\nPageable p = PageRequest.of(page, Math.min(size, 50), Sort.by(Sort.Direction.DESC, \"createdAt\"));\nPage<Note> result = repo.findByOwnerIdAndTitleContainingIgnoreCase(ownerId, q, p);\n```\nWhitelist sortable fields; clamp size; escape LIKE wildcards if you build patterns yourself.",
      [("Envelope", "json", "{\"content\":[...],\"page\":0,\"size\":20,\"totalElements\":57,\"totalPages\":3}")],
      [("Why whitelist sort fields?", "Sorting by arbitrary properties can expose or break internals."),
       ("Offset vs keyset pagination?", "Offset is simple but slow deep in the table; keyset uses the last seen key and scales.")]),
    T("Consistent error contract and the test pyramid",
      "Clients need one predictable error shape. Spring 6 supports RFC 9457 `ProblemDetail` (`type`, `title`, `status`, `detail`, `instance` + extensions like `errors`). A `@RestControllerAdvice` maps domain exceptions to statuses and never leaks internals. Tests follow the **pyramid**: many fast unit tests, fewer slice tests (`@WebMvcTest`, `@DataJpaTest`), few full `@SpringBootTest` integration tests.",
      "A uniform contract simplifies clients; layered tests give fast feedback and precise failures.",
      ["Predictable client handling", "Security: no stack traces/SQL in responses", "Fast test suite"],
      ["Central handler must be kept in sync with new exceptions", "Slice tests need careful scoping (imports, mocks)"],
      "Default Boot error JSON differs per exception; leaking `exception.getMessage()` for unexpected errors reveals secrets and structure.",
      "```java\n@ExceptionHandler(NotFoundException.class)\nProblemDetail notFound(NotFoundException e) {\n  ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());\n  pd.setTitle(\"Not Found\");\n  return pd;\n}\n```",
      [("Validation errors", "json", "{\"status\":400,\"title\":\"Bad Request\",\"detail\":\"Validation failed\",\"errors\":{\"name\":\"must not be blank\"}}")],
      [("What belongs in a 500 response?", "A generic message and a correlation id; details go to logs."),
       ("Which test type verifies JSON error shapes?", "`@WebMvcTest` with MockMvc.")]),
]

day(48, "Capstone API Slice II: Ownership, Pagination, Errors, and Tests", "Capstone",
    "Object-level authorization, safe list endpoints, a consistent error contract, and hardening against bad input",
    ["Enforce owner-only access with an explicit 403/404 policy", "Implement paged, sorted, owner-scoped search with whitelisting", "Return a single ProblemDetail-based error contract without leaks", "Integrate ownership checks with JPA services (rename/delete) and validation order", "Apply the test pyramid (unit, slice, integration)"],
    ["Day 47 Capstone slice I", "Day 38 Spring Security basics"],
    TOPICS, [o1, o2, o3, o4],
    [("What is BOLA?", "Broken object-level authorization: missing ownership checks on id-based access."),
     ("403 or 404 for someone else's resource?", "404 to hide existence (common for private data), 403 when existence is public; be consistent."),
     ("How do you prevent huge responses?", "Mandatory pagination with a max size."),
     ("What is ProblemDetail?", "Standard (RFC 9457) JSON error format supported by Spring 6."),
     ("What goes in the test pyramid base?", "Fast unit tests of services/guards.")],
    ["Scoping list endpoints but not detail endpoints.", "Returning raw exception messages.", "Allowing arbitrary sort fields.", "Validating after the database lookup.", "Using `@SpringBootTest` for everything."],
    ["OWASP API Security Top 10 (API1 BOLA)", "Spring Framework Reference: Error Responses", "Spring Data JPA Reference: Paging and Sorting"],
    [("BOLA/IDOR", "Accessing others' objects via ids"), ("ProblemDetail", "RFC 9457 error format"), ("Keyset pagination", "Paging by last-seen key"), ("Slice test", "Test loading only part of the context"),
     ("Whitelist", "Explicit list of allowed values")],
    "2-3 h theory + 5-7 h tasks", spring=True)
