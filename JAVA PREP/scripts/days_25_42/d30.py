from sx import *

S = ["spring-boot-starter-web"]
WEB_TEST_DEP = []

# ------------------------------------------------------------ task 1
GREET = r'''package %PKG%;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

//A! annotate the class as a REST controller mapped under /api/greetings
@RestController
@RequestMapping("/api/greetings")
//E!
public class GreetingController {

    /** GET /api/greetings/{name} -> "Hello, {name}!" (plain text). */
    //A! add the GET mapping for /{name}
    @GetMapping("/{name}")
    //E!
    public String greet(/*A!*/ @PathVariable String name) {
        //B! return "Hello, <name>!"
        return "Hello, " + name + "!";
        //E!
    }

    /** GET /api/greetings?name=Ann&times=3 -> "Hello, Ann! Hello, Ann! Hello, Ann!" (defaults: name=World, times=1). */
    //A! add the GET mapping for the collection path (no path suffix)
    @GetMapping
    //E!
    public String repeat(@RequestParam(defaultValue = "World") String name,
                         @RequestParam(defaultValue = "1") int times) {
        //B! join `times` copies of the greeting with single spaces; times < 1 must produce an empty string
        if (times < 1) {
            return "";
        }
        return String.join(" ", java.util.Collections.nCopies(times, "Hello, " + name + "!"));
        //E!
    }
}
'''
GREET = GREET.replace("/*A!*/ ", "")
GREET_TEST = r'''package %PKG%;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(GreetingController.class)
class GreetingControllerTest {

    @Autowired
    MockMvc mvc;

    @Test
    void pathVariableGreeting() throws Exception {
        mvc.perform(get("/api/greetings/Ann")).andExpect(status().isOk()).andExpect(content().string("Hello, Ann!"));
    }

    @Test
    void queryDefaults() throws Exception {
        mvc.perform(get("/api/greetings")).andExpect(status().isOk()).andExpect(content().string("Hello, World!"));
    }

    @Test
    void repeatsGreeting() throws Exception {
        mvc.perform(get("/api/greetings").param("name", "Bo").param("times", "3"))
                .andExpect(content().string("Hello, Bo! Hello, Bo! Hello, Bo!"));
    }

    @Test
    void zeroTimesIsEmpty() throws Exception {
        mvc.perform(get("/api/greetings").param("times", "0")).andExpect(status().isOk()).andExpect(content().string(""));
    }

    @Test
    void badNumberIs400() throws Exception {
        mvc.perform(get("/api/greetings").param("times", "abc")).andExpect(status().isBadRequest());
    }
}
'''
a1 = tk("greeting-endpoints", "Greeting Endpoints: Path and Query Parameters", "Warm-up",
    "Turn a plain class into a REST controller using @RestController, @RequestMapping, @GetMapping, @PathVariable and @RequestParam with defaults.",
    {"main/Application.java": APP, "main/GreetingController.java": GREET},
    {"test/GreetingControllerTest.java": GREET_TEST},
    ["Mark `GreetingController` as a REST controller under `/api/greetings`.", "Map `greet` to `GET /{name}` and `repeat` to `GET` with query defaults.", "Implement both bodies; `times < 1` returns an empty string."],
    ["Non-numeric `times` yields 400 automatically (type conversion failure).", "Default values apply when parameters are absent."],
    ["`@RestController` = `@Controller` + `@ResponseBody`.", "`@RequestParam(defaultValue=...)` makes the parameter optional."],
    S)

# ------------------------------------------------------------ task 2
BOOK = '''package %PKG%;

public record Book(Long id, String title, String author) {
}
'''
BSVC = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;

/** PROVIDED in-memory store (do not edit). */
@Service
public class BookService {
    private final Map<Long, Book> books = new ConcurrentHashMap<>();
    private final AtomicLong seq = new AtomicLong();

    public List<Book> findAll() {
        return new ArrayList<>(books.values().stream().sorted(java.util.Comparator.comparing(Book::id)).toList());
    }

    public Optional<Book> findById(long id) {
        return Optional.ofNullable(books.get(id));
    }

    public Book create(String title, String author) {
        Book b = new Book(seq.incrementAndGet(), title, author);
        books.put(b.id(), b);
        return b;
    }

    public boolean delete(long id) {
        return books.remove(id) != null;
    }
}
'''
BREQ = '''package %PKG%;

public record CreateBookRequest(String title, String author) {
}
'''
BCTL = r'''package %PKG%;

import java.net.URI;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/books")
public class BookController {

    private final BookService service;

    public BookController(BookService service) {
        this.service = service;
    }

    /** GET /api/books -> 200 + JSON array. */
    @GetMapping
    public List<Book> list() {
        //B! return all books
        return service.findAll();
        //E!
    }

    /** GET /api/books/{id} -> 200 + book, or 404 with empty body. */
    @GetMapping("/{id}")
    public ResponseEntity<Book> get(@PathVariable long id) {
        //B! 200 with the book or 404 (ResponseEntity.notFound)
        return service.findById(id).map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
        //E!
    }

    /** POST /api/books -> 201, Location: /api/books/{newId}, body = created book. */
    @PostMapping
    public ResponseEntity<Book> create(@RequestBody CreateBookRequest request) {
        //B! create the book and answer 201 Created with a Location header and the book as body
        Book b = service.create(request.title(), request.author());
        return ResponseEntity.created(URI.create("/api/books/" + b.id())).body(b);
        //E!
    }

    /** DELETE /api/books/{id} -> 204 when deleted, 404 when unknown. */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable long id) {
        //B! 204 No Content when removed, otherwise 404
        return service.delete(id) ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
        //E!
    }
}
'''
BTEST = r'''package %PKG%;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(BookController.class)
@Import(BookService.class)
@org.springframework.test.annotation.DirtiesContext(classMode = org.springframework.test.annotation.DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class BookControllerTest {

    @Autowired
    MockMvc mvc;

    private void create(String json) throws Exception {
        mvc.perform(post("/api/books").contentType(MediaType.APPLICATION_JSON).content(json)).andExpect(status().isCreated());
    }

    @Test
    void emptyListInitially() throws Exception {
        mvc.perform(get("/api/books")).andExpect(status().isOk()).andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void createReturns201WithLocation() throws Exception {
        mvc.perform(post("/api/books").contentType(MediaType.APPLICATION_JSON).content("{\"title\":\"Dune\",\"author\":\"Herbert\"}"))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", "/api/books/1"))
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.title").value("Dune"));
    }

    @Test
    void getExistingAndMissing() throws Exception {
        create("{\"title\":\"A\",\"author\":\"B\"}");
        mvc.perform(get("/api/books/1")).andExpect(status().isOk()).andExpect(jsonPath("$.author").value("B"));
        mvc.perform(get("/api/books/99")).andExpect(status().isNotFound());
    }

    @Test
    void listContainsCreatedBooks() throws Exception {
        create("{\"title\":\"A\",\"author\":\"B\"}");
        create("{\"title\":\"C\",\"author\":\"D\"}");
        mvc.perform(get("/api/books")).andExpect(jsonPath("$", hasSize(2))).andExpect(jsonPath("$[1].title").value("C"));
    }

    @Test
    void deleteIs204ThenMissingIs404() throws Exception {
        create("{\"title\":\"A\",\"author\":\"B\"}");
        mvc.perform(delete("/api/books/1")).andExpect(status().isNoContent());
        mvc.perform(delete("/api/books/1")).andExpect(status().isNotFound());
    }

    @Test
    void malformedJsonIs400() throws Exception {
        mvc.perform(post("/api/books").contentType(MediaType.APPLICATION_JSON).content("{oops")).andExpect(status().isBadRequest());
    }
}
'''
a2 = tk("books-response-entity", "Books API with ResponseEntity", "Core",
    "Implement list/get/create/delete endpoints using ResponseEntity to control status codes and the Location header.",
    {"main/Application.java": APP, "main/Book.java": BOOK, "main/BookService.java": BSVC, "main/CreateBookRequest.java": BREQ,
     "main/BookController.java": BCTL},
    {"test/BookControllerTest.java": BTEST},
    ["Implement `list`, `get`, `create`, `delete` in `BookController`.", "`create` must return 201 with `Location: /api/books/{id}` and the created book.", "Unknown ids must produce 404 for `get` and `delete`."],
    ["Malformed JSON body -> 400 (handled by Spring).", "`delete` twice: 204 then 404."],
    ["`ResponseEntity.created(URI).body(x)`.", "`ResponseEntity.notFound().build()` has no body."],
    S)

# ------------------------------------------------------------ task 3
EVENT = r'''package %PKG%;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * JSON contract:
 *  - "name" is serialized as "event_name"
 *  - "date" is a string like 2025-03-09
 *  - "internalNote" never appears in JSON (in or out)
 *  - null fields are omitted from output
 */
//A! add @JsonInclude(JsonInclude.Include.NON_NULL) on the record
@JsonInclude(JsonInclude.Include.NON_NULL)
//E!
public record Event(
        //A! rename to event_name with @JsonProperty
        @JsonProperty("event_name")
        //E!
        String name,
        //A! format as yyyy-MM-dd text with @JsonFormat(shape = STRING, pattern = "yyyy-MM-dd")
        @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
        //E!
        LocalDate date,
        BigDecimal amount,
        //A! exclude from JSON with @JsonIgnore
        @JsonIgnore
        //E!
        String internalNote,
        String venue) {
}
'''
EVTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.math.BigDecimal;
import java.time.LocalDate;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.json.JsonTest;

@JsonTest
class EventJsonTest {

    @Autowired
    ObjectMapper mapper;

    @Test
    void serializesWithRenamedFormattedFields() throws Exception {
        Event e = new Event("Conf", LocalDate.of(2025, 3, 9), new BigDecimal("12.50"), "secret", "Hall A");
        JsonNode n = mapper.readTree(mapper.writeValueAsString(e));
        assertThat(n.get("event_name").asText()).isEqualTo("Conf");
        assertThat(n.get("date").asText()).isEqualTo("2025-03-09");
        assertThat(n.get("amount").decimalValue()).isEqualByComparingTo("12.50");
        assertThat(n.has("name")).isFalse();
    }

    @Test
    void internalNoteIsNeverSerialized() throws Exception {
        Event e = new Event("Conf", LocalDate.of(2025, 3, 9), BigDecimal.ONE, "secret", null);
        assertThat(mapper.writeValueAsString(e)).doesNotContain("secret").doesNotContain("internalNote");
    }

    @Test
    void nullsAreOmitted() throws Exception {
        Event e = new Event("Conf", LocalDate.of(2025, 3, 9), null, null, null);
        JsonNode n = mapper.readTree(mapper.writeValueAsString(e));
        assertThat(n.has("amount")).isFalse();
        assertThat(n.has("venue")).isFalse();
    }

    @Test
    void deserializesAndIgnoresInternalNote() throws Exception {
        String json = "{\"event_name\":\"Talk\",\"date\":\"2025-01-02\",\"amount\":3,\"internalNote\":\"hack\",\"venue\":\"B\"}";
        Event e = mapper.readerFor(Event.class).without(com.fasterxml.jackson.databind.DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES).readValue(json);
        assertThat(e.name()).isEqualTo("Talk");
        assertThat(e.date()).isEqualTo(LocalDate.of(2025, 1, 2));
        assertThat(e.internalNote()).isNull();
    }
}
'''
a3 = tk("jackson-event-contract", "Jackson JSON Contract", "Core",
    "Shape a record's JSON representation with Jackson annotations: rename, format, ignore and omit nulls — verified against Spring Boot's auto-configured ObjectMapper.",
    {"main/Application.java": APP, "main/Event.java": EVENT},
    {"test/EventJsonTest.java": EVTEST},
    ["Add `@JsonInclude(NON_NULL)` to the record.", "Rename `name` to `event_name`.", "Format `date` as `yyyy-MM-dd` text.", "Hide `internalNote` in both directions."],
    ["Null `amount`/`venue` must not appear in output.", "Incoming `internalNote` must be ignored (stay null)."],
    ["On records, annotate the component; Jackson 2.15+ propagates it correctly.", "Boot already registers `JavaTimeModule` and disables timestamp dates."],
    S + ["spring-boot-starter-json"])

# ------------------------------------------------------------ task 4
NSVC = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;

/** PROVIDED in-memory store (do not edit). */
@Service
public class NoteService {
    private final Map<Long, Note> notes = new ConcurrentHashMap<>();
    private final AtomicLong seq = new AtomicLong();

    public Note add(String text) {
        Note n = new Note(seq.incrementAndGet(), text);
        notes.put(n.id(), n);
        return n;
    }

    public List<Note> all() {
        return new ArrayList<>(notes.values().stream().sorted(java.util.Comparator.comparing(Note::id)).toList());
    }

    public Optional<Note> update(long id, String text) {
        return notes.computeIfPresent(id, (k, old) -> new Note(k, text)) == null ? Optional.empty() : Optional.of(notes.get(id));
    }
}
'''
NOTE = "package %PKG%;\n\npublic record Note(Long id, String text) {\n}\n"
NCTL = r'''package %PKG%;

import java.util.List;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/notes")
public class NoteController {

    private final NoteService service;

    public NoteController(NoteService service) {
        this.service = service;
    }

    /**
     * GET /api/notes?contains=x&limit=n
     *  - contains: optional case-insensitive substring filter on text
     *  - limit: optional max number of items returned (>= 0)
     *  - header X-Total-Count = number of notes matching the filter BEFORE limiting
     */
    @GetMapping
    public ResponseEntity<List<Note>> search(@RequestParam(required = false) String contains,
                                             @RequestParam(required = false) Integer limit) {
        //B! filter, count, limit; return 200 with the X-Total-Count header
        List<Note> filtered = service.all().stream()
                .filter(n -> contains == null || n.text().toLowerCase().contains(contains.toLowerCase()))
                .toList();
        List<Note> page = limit == null ? filtered : filtered.stream().limit(Math.max(0, limit)).toList();
        return ResponseEntity.ok().header("X-Total-Count", String.valueOf(filtered.size())).body(page);
        //E!
    }

    /**
     * PUT /api/notes/{id} with JSON {"text": "..."}:
     *  - 200 + updated note
     *  - 404 if the note does not exist
     *  - 400 with JSON {"error": "text must not be blank"} if text is null/blank
     * (check validity BEFORE the lookup)
     */
    @PutMapping("/{id}")
    public ResponseEntity<?> update(@PathVariable long id, @RequestBody Map<String, String> body) {
        //B! validate text (400 + error body), then update and answer 200 or 404
        String text = body.get("text");
        if (text == null || text.isBlank()) {
            return ResponseEntity.badRequest().body(Map.of("error", "text must not be blank"));
        }
        return service.update(id, text).<ResponseEntity<?>>map(ResponseEntity::ok).orElseGet(() -> ResponseEntity.notFound().build());
        //E!
    }
}
'''
NTEST = r'''package %PKG%;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(NoteController.class)
@Import(NoteService.class)
@org.springframework.test.annotation.DirtiesContext(classMode = org.springframework.test.annotation.DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class NoteControllerTest {

    @Autowired
    MockMvc mvc;
    @Autowired
    NoteService service;

    @BeforeEach
    void seed() {
        service.add("Buy milk");
        service.add("Call Mom");
        service.add("Milk the cow");
    }

    @Test
    void listsAllWithTotalHeader() throws Exception {
        mvc.perform(get("/api/notes")).andExpect(status().isOk()).andExpect(jsonPath("$", hasSize(3)))
                .andExpect(header().string("X-Total-Count", "3"));
    }

    @Test
    void filtersCaseInsensitively() throws Exception {
        mvc.perform(get("/api/notes").param("contains", "MILK")).andExpect(jsonPath("$", hasSize(2)))
                .andExpect(header().string("X-Total-Count", "2"));
    }

    @Test
    void limitCutsPageButNotTotal() throws Exception {
        mvc.perform(get("/api/notes").param("limit", "1")).andExpect(jsonPath("$", hasSize(1)))
                .andExpect(header().string("X-Total-Count", "3"));
        mvc.perform(get("/api/notes").param("limit", "0")).andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void updateReturnsNewNote() throws Exception {
        mvc.perform(put("/api/notes/2").contentType(MediaType.APPLICATION_JSON).content("{\"text\":\"Call Dad\"}"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.text").value("Call Dad")).andExpect(jsonPath("$.id").value(2));
    }

    @Test
    void updateUnknownIs404() throws Exception {
        mvc.perform(put("/api/notes/42").contentType(MediaType.APPLICATION_JSON).content("{\"text\":\"x\"}")).andExpect(status().isNotFound());
    }

    @Test
    void blankTextIs400EvenForUnknownId() throws Exception {
        mvc.perform(put("/api/notes/42").contentType(MediaType.APPLICATION_JSON).content("{\"text\":\"  \"}"))
                .andExpect(status().isBadRequest()).andExpect(jsonPath("$.error").value("text must not be blank"));
        mvc.perform(put("/api/notes/1").contentType(MediaType.APPLICATION_JSON).content("{}")).andExpect(status().isBadRequest());
    }
}
'''
a4 = tk("notes-search-and-update", "Notes API: Filters, Headers and Status Codes", "Challenge",
    "Combine optional query parameters, a custom response header and explicit 400/404 handling in one controller.",
    {"main/Application.java": APP, "main/Note.java": NOTE, "main/NoteService.java": NSVC, "main/NoteController.java": NCTL},
    {"test/NoteControllerTest.java": NTEST},
    ["Implement `search` with `contains`, `limit` and the `X-Total-Count` header.", "Implement `update` with 200/404/400 behavior; validation happens before lookup."],
    ["`limit=0` returns an empty array; total still counts matches.", "Missing `text` key behaves like blank."],
    ["Stream filter first, count, then `limit`.", "Use `ResponseEntity.ok().header(name, value).body(x)`."],
    S)

topics = [
    T("@RestController, request mappings and the DispatcherServlet",
      "A `@RestController` is a `@Controller` whose return values are written straight to the HTTP response body via `HttpMessageConverter`s (JSON through Jackson). `@RequestMapping` and the shortcuts `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping` bind HTTP method + path to a Java method. Every request enters the `DispatcherServlet`, which finds a handler through `HandlerMapping`, resolves arguments, invokes the method and converts the result.",
      "REST APIs are how browsers, mobile apps and other services talk to your backend. A consistent mapping model lets you express resources (`/api/books/{id}`) and verbs declaratively instead of parsing servlet requests yourself.",
      ["Declarative routing with annotations", "Automatic argument binding and conversion", "Pluggable message converters (JSON, XML, text)", "Same model for MVC and testing (MockMvc)"],
      ["Annotation-heavy code can hide the request flow", "Ambiguous mappings fail at startup", "Content negotiation rules are subtle"],
      "With `@Controller` instead of `@RestController`, a returned String is interpreted as a view name and you get a 404 or template error. Two methods mapping to the same method+path throw `IllegalStateException: Ambiguous mapping` at startup.",
      "```java\n@RestController\n@RequestMapping(\"/api/books\")\nclass BookController {\n  @GetMapping(\"/{id}\") Book get(@PathVariable long id) {...}\n  @PostMapping(consumes = \"application/json\") ... \n}\n```\nClass-level `@RequestMapping` prefixes every method path. `produces`/`consumes` narrow by media type. `@RequestMapping(method = GET)` is the long form of `@GetMapping`.",
      [("Minimal controller", "java", "@RestController\nclass HelloController {\n    @GetMapping(\"/hello\")\n    String hello() { return \"hi\"; }\n}"),
       ("Class + method paths", "java", "@RestController\n@RequestMapping(\"/api/v1/orders\")\nclass OrderController {\n    @GetMapping(\"/{id}/items\") List<Item> items(@PathVariable long id) {...}\n}"),
       ("Narrowing by media type", "java", "@PostMapping(path = \"/import\", consumes = \"text/csv\", produces = \"application/json\")\nImportResult importCsv(@RequestBody String csv) {...}")],
      [("What does @RestController add over @Controller?", "`@ResponseBody` on every method, so return values are serialized to the body instead of resolved as views."),
       ("Which component picks the handler method?", "`HandlerMapping` inside the `DispatcherServlet`."),
       ("What happens with two identical mappings?", "Startup fails with an ambiguous mapping error.")]),
    T("Path variables, query parameters, request bodies and headers",
      "`@PathVariable` binds URI template segments, `@RequestParam` binds query/form parameters (with `required` and `defaultValue`), `@RequestBody` deserializes the body, `@RequestHeader` reads headers. Spring converts strings to `int`, `UUID`, enums, dates and so on using the `ConversionService`; failures produce HTTP 400.",
      "Clients express intent in different places: identity in the path, filters in the query, payload in the body, metadata in headers. Using each place correctly keeps APIs cacheable, predictable and easy to document.",
      ["Strong typing of inputs", "Defaults and optional parameters are one attribute away", "Automatic 400 on malformed input", "Works with records as request bodies"],
      ["Binding errors give generic messages unless handled (Day 31)", "Too many query parameters become unreadable (use a DTO with `@ModelAttribute`)", "Large bodies need limits"],
      "Reading an id from the query when it identifies a resource breaks caching and REST semantics. A missing required `@RequestParam` returns 400 `MissingServletRequestParameterException`. A `@RequestBody` with the wrong `Content-Type` yields 415.",
      "```java\n@GetMapping(\"/{id}\") Book get(@PathVariable long id)\n@GetMapping List<Book> list(@RequestParam(defaultValue = \"0\") int page, @RequestParam(required = false) String q)\n@PostMapping Book create(@RequestBody CreateBookRequest r)\n@GetMapping Foo h(@RequestHeader(\"X-Trace-Id\") String id)\n```\nName is inferred from the parameter name when compiled with `-parameters` (Boot's parent enables it).",
      [("Optional filter", "java", "@GetMapping\nList<Note> search(@RequestParam(required = false) String contains) {...}"),
       ("Body as record", "java", "record CreateBookRequest(String title, String author) {}\n@PostMapping Book create(@RequestBody CreateBookRequest r) {...}"),
       ("Multiple variables", "java", "@GetMapping(\"/{orderId}/lines/{lineNo}\")\nLine line(@PathVariable long orderId, @PathVariable int lineNo) {...}")],
      [("Path variable or query parameter for an entity id?", "Path variable; it identifies the resource."),
       ("What status results from `?times=abc` for an int parameter?", "400 Bad Request (type mismatch)."),
       ("How do you make a query parameter optional?", "`required = false` or `defaultValue`.")]),
    T("ResponseEntity, status codes and Jackson",
      "`ResponseEntity<T>` lets a method choose status, headers and body explicitly (`created(uri)`, `noContent()`, `notFound()`, `ok().header(..)`). `@ResponseStatus` fixes a status declaratively. Jackson converts objects to JSON; annotations (`@JsonProperty`, `@JsonIgnore`, `@JsonFormat`, `@JsonInclude`) and `spring.jackson.*` properties shape the contract.",
      "Status codes are part of the API contract: 201 + `Location` tells clients where the new resource lives, 204 says there is no body, 404/409/422 describe failures. Jackson settings decide what is exposed and how dates and numbers look.",
      ["Full control of the HTTP response", "Standards-compliant semantics (RFC 9110)", "Boot auto-configures a sane ObjectMapper", "Contract evolution via annotations without changing domain logic"],
      ["`ResponseEntity<?>` loses type information in signatures", "Leaking entities directly couples JSON to the database (use DTOs, Day 31)", "Jackson defaults (unknown properties) differ between plain Jackson and Boot"],
      "Returning 200 with `{\"error\": ...}` for failures breaks clients and monitoring. Serializing a JPA entity with lazy associations can throw or leak data. Without `@JsonIgnore` on secrets they end up in responses.",
      "```java\nreturn ResponseEntity.created(URI.create(\"/api/books/\" + id)).body(book);   // 201\nreturn ResponseEntity.noContent().build();                                  // 204\nreturn ResponseEntity.notFound().build();                                   // 404\n```\n```yaml\nspring.jackson.default-property-inclusion: non_null\nspring.jackson.serialization.write-dates-as-timestamps: false\n```",
      [("Create with Location", "java", "return ResponseEntity.created(URI.create(\"/api/books/\" + b.id())).body(b);"),
       ("Header + body", "java", "return ResponseEntity.ok().header(\"X-Total-Count\", \"42\").body(items);"),
       ("Jackson annotations", "java", "record User(@JsonProperty(\"user_name\") String name, @JsonIgnore String passwordHash) {}")],
      [("Which status should POST create return?", "201 Created with a Location header."),
       ("When use 204?", "Successful request with no response body (e.g. DELETE)."),
       ("Why avoid returning entities directly?", "It couples the API to the persistence model and can leak fields or trigger lazy loading.")]),
]

day(30, "REST I: Controllers, Mappings, Request Binding, ResponseEntity and Jackson", "Spring Boot",
    "Building HTTP APIs with Spring MVC: mappings, request binding, status codes and JSON shaping",
    ["Write @RestController classes with the right mapping annotations", "Bind path variables, query parameters, headers and JSON bodies", "Control status codes and headers with ResponseEntity", "Shape JSON output with Jackson annotations", "Test controllers with MockMvc"],
    ["Day 29 Spring Boot starters and configuration"],
    topics, [a1, a2, a3, a4],
    [("What is the difference between @Controller and @RestController?", "`@RestController` adds `@ResponseBody`, so return values are written to the response body."),
     ("How does Spring MVC pick a handler?", "DispatcherServlet asks HandlerMappings; the matching HandlerMethod is invoked through a HandlerAdapter."),
     ("PUT vs PATCH vs POST?", "POST creates/acts, PUT replaces idempotently, PATCH partially updates."),
     ("What does @RequestBody do?", "Reads the body and converts it with an HttpMessageConverter (Jackson for JSON)."),
     ("How do you customize JSON output?", "Jackson annotations, `spring.jackson.*` properties or a Jackson2ObjectMapperBuilderCustomizer.")],
    ["Using @Controller and getting view resolution errors.", "Returning 200 for errors.", "Forgetting `Content-Type: application/json` on requests (415).", "Mapping ids in query strings instead of paths."],
    ["Spring Framework Reference: Web MVC annotated controllers", "Jackson annotations wiki", "RFC 9110 HTTP Semantics"],
    [("DispatcherServlet", "Front controller of Spring MVC"), ("HttpMessageConverter", "Converts bodies to/from Java objects"), ("ResponseEntity", "Status + headers + body wrapper"),
     ("Location header", "URL of a newly created resource"), ("MockMvc", "Servlet-free MVC test client")],
    "2–3 h theory + 3–5 h tasks", spring=True)
