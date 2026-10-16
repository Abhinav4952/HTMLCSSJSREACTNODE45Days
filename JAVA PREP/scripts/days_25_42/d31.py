from sx import *

S = ["spring-boot-starter-web", "spring-boot-starter-validation"]

# ------------------------------------------------------------ task 1
CREQ = r'''package %PKG%;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Incoming payload. Rules: name not blank; email valid format; age 18..120; password at least 8 characters. */
public record CreateUserRequest(
        //A! add @NotBlank
        @NotBlank
        //E!
        String name,
        //A! add @Email and @NotBlank
        @NotBlank @Email
        //E!
        String email,
        //A! add @Min(18) and @Max(120)
        @Min(18) @Max(120)
        //E!
        int age,
        //A! add @Size(min = 8)
        @Size(min = 8)
        //E!
        String password) {
}
'''
URESP = "package %PKG%;\n\n/** Outgoing payload: never exposes the password. */\npublic record UserResponse(long id, String name, String email) {\n}\n"
UCTL = r'''package %PKG%;

import jakarta.validation.Valid;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final AtomicLong ids = new AtomicLong();

    /** POST /api/users -> 201 and a UserResponse (id from the counter); invalid payload -> 400 (automatic). */
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse create(
            //A! trigger validation of the body with @Valid
            @Valid
            //E!
            @RequestBody CreateUserRequest request) {
        //B! build a UserResponse from the request (no password) using ids.incrementAndGet()
        return new UserResponse(ids.incrementAndGet(), request.name().trim(), request.email().toLowerCase());
        //E!
    }
}
'''
UTEST = r'''package %PKG%;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    MockMvc mvc;

    private ResultActions submit(String name, String email, int age, String password) throws Exception {
        String json = "{\"name\":\"%s\",\"email\":\"%s\",\"age\":%d,\"password\":\"%s\"}".formatted(name, email, age, password);
        return mvc.perform(post("/api/users").contentType(MediaType.APPLICATION_JSON).content(json));
    }

    @Test
    void validRequestCreatesUserWithoutPassword() throws Exception {
        submit(" Ann ", "Ann@Example.com", 30, "longenough").andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").isNumber()).andExpect(jsonPath("$.name").value("Ann"))
                .andExpect(jsonPath("$.email").value("ann@example.com")).andExpect(jsonPath("$.password").doesNotExist());
    }

    @Test
    void blankNameRejected() throws Exception {
        submit("  ", "a@b.co", 30, "longenough").andExpect(status().isBadRequest());
    }

    @Test
    void badEmailRejected() throws Exception {
        submit("Ann", "not-an-email", 30, "longenough").andExpect(status().isBadRequest());
    }

    @Test
    void ageBoundsRejected() throws Exception {
        submit("Ann", "a@b.co", 17, "longenough").andExpect(status().isBadRequest());
        submit("Ann", "a@b.co", 121, "longenough").andExpect(status().isBadRequest());
        submit("Ann", "a@b.co", 18, "longenough").andExpect(status().isCreated());
    }

    @Test
    void shortPasswordRejected() throws Exception {
        submit("Ann", "a@b.co", 30, "short").andExpect(status().isBadRequest());
    }
}
'''
a1 = tk("create-user-validation", "Create User: DTOs and Bean Validation", "Warm-up",
    "Protect a POST endpoint with Bean Validation constraints on a request DTO and return a password-free response DTO.",
    {"main/Application.java": APP, "main/CreateUserRequest.java": CREQ, "main/UserResponse.java": URESP, "main/UserController.java": UCTL},
    {"test/UserControllerTest.java": UTEST},
    ["Add constraints to `CreateUserRequest`.", "Enable validation with `@Valid` in `UserController`.", "Map the request to `UserResponse` (trim name, lowercase email, no password)."],
    ["Missing validation -> the handler would run with bad data (NPE or silent success).", "Boundary ages 18 and 120 are valid."],
    ["Constraints live on record components.", "`@Valid` on the parameter triggers `MethodArgumentNotValidException` -> 400."],
    S)

# ------------------------------------------------------------ task 2
NF = "package %PKG%;\n\npublic class ResourceNotFoundException extends RuntimeException {\n    public ResourceNotFoundException(String message) {\n        super(message);\n    }\n}\n"
ACT = r'''package %PKG%;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED controller whose failures your advice must translate (do not edit). */
@RestController
@RequestMapping("/api/demo")
public class DemoController {

    public record Payload(@NotBlank String title) {
    }

    @GetMapping("/missing/{id}")
    public String missing(@PathVariable long id) {
        throw new ResourceNotFoundException("Item " + id + " not found");
    }

    @GetMapping("/conflict")
    public String conflict() {
        throw new IllegalStateException("Already processed");
    }

    @PostMapping("/validate")
    public String validate(@Valid @RequestBody Payload payload) {
        return payload.title();
    }
}
'''
ADV = r'''package %PKG%;

import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

//A! make this a global REST exception translator
@RestControllerAdvice
//E!
public class ApiExceptionHandler {

    /** 404 problem: title "Not Found", detail = exception message. */
    //A! register for ResourceNotFoundException
    @ExceptionHandler(ResourceNotFoundException.class)
    //E!
    public ProblemDetail notFound(ResourceNotFoundException ex) {
        //B! ProblemDetail.forStatusAndDetail(NOT_FOUND, message) with title "Not Found"
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setTitle("Not Found");
        return pd;
        //E!
    }

    /** 409 problem: title "Conflict", detail = exception message. */
    //A! register for IllegalStateException
    @ExceptionHandler(IllegalStateException.class)
    //E!
    public ProblemDetail conflict(IllegalStateException ex) {
        //B! build a 409 ProblemDetail
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.CONFLICT, ex.getMessage());
        pd.setTitle("Conflict");
        return pd;
        //E!
    }

    /** 400 problem: title "Validation failed"; custom property "errors" = map field -> message. */
    //A! register for MethodArgumentNotValidException
    @ExceptionHandler(MethodArgumentNotValidException.class)
    //E!
    public ProblemDetail invalid(MethodArgumentNotValidException ex) {
        //B! collect field errors into a map and set it as property errors
        ProblemDetail pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        pd.setTitle("Validation failed");
        Map<String, String> errors = new LinkedHashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(fe -> errors.put(fe.getField(), fe.getDefaultMessage()));
        pd.setProperty("errors", errors);
        return pd;
        //E!
    }
}
'''
ATEST = r'''package %PKG%;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(DemoController.class)
@Import(ApiExceptionHandler.class)
class ApiExceptionHandlerTest {

    @Autowired
    MockMvc mvc;

    @Test
    void notFoundBecomesProblemDetail() throws Exception {
        mvc.perform(get("/api/demo/missing/7")).andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.title").value("Not Found")).andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.detail").value("Item 7 not found"));
    }

    @Test
    void illegalStateBecomesConflict() throws Exception {
        mvc.perform(get("/api/demo/conflict")).andExpect(status().isConflict())
                .andExpect(jsonPath("$.title").value("Conflict")).andExpect(jsonPath("$.detail").value("Already processed"));
    }

    @Test
    void validationFailureListsFieldErrors() throws Exception {
        mvc.perform(post("/api/demo/validate").contentType(MediaType.APPLICATION_JSON).content("{\"title\":\"\"}"))
                .andExpect(status().isBadRequest()).andExpect(jsonPath("$.title").value("Validation failed"))
                .andExpect(jsonPath("$.errors.title").exists());
    }

    @Test
    void happyPathUntouched() throws Exception {
        mvc.perform(post("/api/demo/validate").contentType(MediaType.APPLICATION_JSON).content("{\"title\":\"ok\"}"))
                .andExpect(status().isOk()).andExpect(content().string("ok"));
    }
}
'''
a2 = tk("problem-detail-advice", "Global Errors with @RestControllerAdvice and ProblemDetail", "Core",
    "Centralize error translation into RFC 9457 problem responses: 404, 409 and a 400 that lists field errors.",
    {"main/Application.java": APP, "main/ResourceNotFoundException.java": NF, "main/DemoController.java": ACT, "main/ApiExceptionHandler.java": ADV},
    {"test/ApiExceptionHandlerTest.java": ATEST},
    ["Annotate `ApiExceptionHandler` as a controller advice and register the three handlers.", "Build `ProblemDetail` bodies with the specified titles and details.", "Expose per-field messages in an `errors` property."],
    ["Content type must be `application/problem+json`.", "Successful requests are unaffected."],
    ["`ProblemDetail.forStatusAndDetail(status, detail)`.", "`ex.getBindingResult().getFieldErrors()` gives field + message."],
    S)

# ------------------------------------------------------------ task 3
TODO = "package %PKG%;\n\npublic record Todo(long id, String title, boolean done) {\n}\n"
TDTO = "package %PKG%;\n\npublic record TodoDto(long id, String title, String status) {\n}\n"
TREPO = r'''package %PKG%;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.TreeMap;

/** PROVIDED in-memory repository (data layer). */
public class TodoRepository {
    private final Map<Long, Todo> data = new TreeMap<>();
    private long seq;

    public Todo save(Todo todo) {
        long id = todo.id() == 0 ? ++seq : todo.id();
        Todo saved = new Todo(id, todo.title(), todo.done());
        data.put(id, saved);
        return saved;
    }

    public Optional<Todo> findById(long id) {
        return Optional.ofNullable(data.get(id));
    }

    public List<Todo> findAll() {
        return new ArrayList<>(data.values());
    }
}
'''
TEXC = "package %PKG%;\n\npublic class DuplicateTodoException extends RuntimeException {\n    public DuplicateTodoException(String title) {\n        super(\"Duplicate todo: \" + title);\n    }\n}\n"
TNF = "package %PKG%;\n\npublic class TodoNotFoundException extends RuntimeException {\n    public TodoNotFoundException(long id) {\n        super(\"Todo \" + id + \" not found\");\n    }\n}\n"
TMAP = r'''package %PKG%;

/** Mapping layer: domain <-> DTO. */
public final class TodoMapper {

    private TodoMapper() {
    }

    /** status is "DONE" or "OPEN". */
    public static TodoDto toDto(Todo todo) {
        //B! map to TodoDto with status DONE or OPEN
        return new TodoDto(todo.id(), todo.title(), todo.done() ? "DONE" : "OPEN");
        //E!
    }
}
'''
TSVC = r'''package %PKG%;

import java.util.List;

/** Business layer. Knows nothing about HTTP. */
public class TodoService {

    private final TodoRepository repository;

    public TodoService(TodoRepository repository) {
        this.repository = repository;
    }

    /** Trims the title; blank -> IllegalArgumentException; case-insensitive duplicate -> DuplicateTodoException. New todos are open. */
    public TodoDto create(String title) {
        //B! validate, reject duplicates (ignore case), save and map
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("title must not be blank");
        }
        String clean = title.trim();
        boolean exists = repository.findAll().stream().anyMatch(t -> t.title().equalsIgnoreCase(clean));
        if (exists) {
            throw new DuplicateTodoException(clean);
        }
        return TodoMapper.toDto(repository.save(new Todo(0, clean, false)));
        //E!
    }

    /** Marks a todo as done. Unknown id -> TodoNotFoundException. Completing an already done todo -> IllegalStateException. */
    public TodoDto complete(long id) {
        //B! load, check state, save the done copy and map
        Todo todo = repository.findById(id).orElseThrow(() -> new TodoNotFoundException(id));
        if (todo.done()) {
            throw new IllegalStateException("Todo " + id + " already done");
        }
        return TodoMapper.toDto(repository.save(new Todo(id, todo.title(), true)));
        //E!
    }

    /** All todos as DTOs, optionally only the open ones. */
    public List<TodoDto> list(boolean onlyOpen) {
        //B! map all (or only open) todos
        return repository.findAll().stream().filter(t -> !onlyOpen || !t.done()).map(TodoMapper::toDto).toList();
        //E!
    }
}
'''
TCTL = r'''package %PKG%;

import java.util.List;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/** PROVIDED web layer: depends ONLY on the service (never on the repository). */
@RestController
@RequestMapping("/api/todos")
public class TodoController {

    private final TodoService service;

    public TodoController(TodoService service) {
        this.service = service;
    }

    @PostMapping
    public TodoDto create(@RequestBody TodoDto body) {
        return service.create(body.title());
    }

    @PostMapping("/{id}/complete")
    public TodoDto complete(@PathVariable long id) {
        return service.complete(id);
    }

    @GetMapping
    public List<TodoDto> list(@RequestParam(defaultValue = "false") boolean onlyOpen) {
        return service.list(onlyOpen);
    }
}
'''
TTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.lang.reflect.Constructor;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class TodoServiceTest {

    TodoRepository repo;
    TodoService service;

    @BeforeEach
    void setUp() {
        repo = new TodoRepository();
        service = new TodoService(repo);
    }

    @Test
    void createTrimsAndStartsOpen() {
        TodoDto dto = service.create("  Write tests ");
        assertThat(dto.id()).isEqualTo(1);
        assertThat(dto.title()).isEqualTo("Write tests");
        assertThat(dto.status()).isEqualTo("OPEN");
    }

    @Test
    void blankTitleRejected() {
        assertThatThrownBy(() -> service.create("  ")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.create(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void duplicateIgnoringCaseRejected() {
        service.create("Milk");
        assertThatThrownBy(() -> service.create(" milk ")).isInstanceOf(DuplicateTodoException.class);
    }

    @Test
    void completeFlow() {
        service.create("A");
        assertThat(service.complete(1).status()).isEqualTo("DONE");
        assertThatThrownBy(() -> service.complete(1)).isInstanceOf(IllegalStateException.class);
        assertThatThrownBy(() -> service.complete(99)).isInstanceOf(TodoNotFoundException.class);
    }

    @Test
    void listCanFilterOpen() {
        service.create("A");
        service.create("B");
        service.complete(1);
        assertThat(service.list(false)).hasSize(2);
        List<TodoDto> open = service.list(true);
        assertThat(open).extracting(TodoDto::title).containsExactly("B");
    }

    @Test
    void controllerDependsOnServiceOnly() {
        Constructor<?>[] ctors = TodoController.class.getDeclaredConstructors();
        assertThat(ctors).hasSize(1);
        assertThat(ctors[0].getParameterTypes()).containsExactly(TodoService.class);
    }
}
'''
a3 = tk("layered-todo-service", "Layered Architecture: Controller, Service, Repository, Mapper", "Core",
    "Implement the business and mapping layers of a todo API so HTTP concerns, rules and storage stay separate.",
    {"main/Application.java": APP, "main/Todo.java": TODO, "main/TodoDto.java": TDTO, "main/TodoRepository.java": TREPO,
     "main/DuplicateTodoException.java": TEXC, "main/TodoNotFoundException.java": TNF, "main/TodoMapper.java": TMAP,
     "main/TodoService.java": TSVC, "main/TodoController.java": TCTL},
    {"test/TodoServiceTest.java": TTEST},
    ["Implement `TodoMapper.toDto`.", "Implement `TodoService.create`, `complete`, `list` with the documented rules and exceptions."],
    ["Duplicate detection ignores case and surrounding whitespace.", "A second `complete` fails with `IllegalStateException`."],
    ["Keep rules in the service, not the controller.", "Records are immutable: save a new `Todo` copy with `done=true`."],
    S)

# ------------------------------------------------------------ task 4
SP_ANN = r'''package %PKG%;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/** PROVIDED constraint: at least 8 chars with an upper-case letter, a lower-case letter and a digit. */
@Target({ElementType.FIELD, ElementType.PARAMETER, ElementType.RECORD_COMPONENT})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = StrongPasswordValidator.class)
public @interface StrongPassword {
    String message() default "password is too weak";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
'''
SP_VAL = r'''package %PKG%;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class StrongPasswordValidator implements ConstraintValidator<StrongPassword, String> {

    /** null is VALID here (combine with @NotNull when required). */
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        //B! null valid; otherwise length >= 8 with upper, lower and digit
        if (value == null) {
            return true;
        }
        boolean up = false, low = false, dig = false;
        for (char c : value.toCharArray()) {
            up |= Character.isUpperCase(c);
            low |= Character.isLowerCase(c);
            dig |= Character.isDigit(c);
        }
        return value.length() >= 8 && up && low && dig;
        //E!
    }
}
'''
DR_ANN = r'''package %PKG%;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/** PROVIDED class-level constraint: end must be strictly after start. */
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = DateRangeValidator.class)
public @interface ValidDateRange {
    String message() default "end must be after start";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
'''
DR_VAL = r'''package %PKG%;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

public class DateRangeValidator implements ConstraintValidator<ValidDateRange, Booking> {

    /** Valid when either date is null (let @NotNull report that) or end is strictly after start. */
    @Override
    public boolean isValid(Booking value, ConstraintValidatorContext context) {
        //B! null-tolerant strict end-after-start check
        if (value == null || value.start() == null || value.end() == null) {
            return true;
        }
        return value.end().isAfter(value.start());
        //E!
    }
}
'''
BOOKING = r'''package %PKG%;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDate;

@ValidDateRange
public record Booking(@NotBlank String guest, @NotNull LocalDate start, @NotNull LocalDate end) {
}
'''
ACCOUNT = r'''package %PKG%;

import jakarta.validation.constraints.NotNull;

public record Registration(@NotNull @StrongPassword String password) {
}
'''
CTEST = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validation;
import jakarta.validation.Validator;
import java.time.LocalDate;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class CustomConstraintsTest {

    static final Validator V = Validation.buildDefaultValidatorFactory().getValidator();

    @ParameterizedTest
    @CsvSource({"Abcdefg1,true", "abcdefg1,false", "ABCDEFG1,false", "Abcdefgh,false", "Ab1,false"})
    void strongPasswordRules(String pw, boolean ok) {
        assertThat(V.validate(new Registration(pw)).isEmpty()).isEqualTo(ok);
    }

    @Test
    void nullPasswordReportedByNotNullOnly() {
        Set<ConstraintViolation<Registration>> v = V.validate(new Registration(null));
        assertThat(v).hasSize(1);
        assertThat(v.iterator().next().getConstraintDescriptor().getAnnotation().annotationType().getSimpleName()).isEqualTo("NotNull");
    }

    @Test
    void validRange() {
        assertThat(V.validate(new Booking("Ann", LocalDate.of(2025, 1, 1), LocalDate.of(2025, 1, 2)))).isEmpty();
    }

    @Test
    void sameDayAndReversedRangesRejected() {
        assertThat(V.validate(new Booking("Ann", LocalDate.of(2025, 1, 1), LocalDate.of(2025, 1, 1)))).hasSize(1);
        Set<ConstraintViolation<Booking>> v = V.validate(new Booking("Ann", LocalDate.of(2025, 2, 1), LocalDate.of(2025, 1, 1)));
        assertThat(v).extracting(ConstraintViolation::getMessage).containsExactly("end must be after start");
    }

    @Test
    void missingDatesReportedOnlyByNotNull() {
        Set<ConstraintViolation<Booking>> v = V.validate(new Booking("Ann", null, LocalDate.of(2025, 1, 1)));
        assertThat(v).hasSize(1);
        assertThat(v.iterator().next().getPropertyPath().toString()).isEqualTo("start");
    }
}
'''
a4 = tk("custom-constraints", "Custom Bean Validation Constraints", "Challenge",
    "Implement a field-level (@StrongPassword) and a class-level (@ValidDateRange) ConstraintValidator and verify them with the Jakarta Validator API.",
    {"main/Application.java": APP, "main/StrongPassword.java": SP_ANN, "main/StrongPasswordValidator.java": SP_VAL,
     "main/ValidDateRange.java": DR_ANN, "main/DateRangeValidator.java": DR_VAL, "main/Booking.java": BOOKING, "main/Registration.java": ACCOUNT},
    {"test/CustomConstraintsTest.java": CTEST},
    ["Implement `StrongPasswordValidator.isValid`.", "Implement `DateRangeValidator.isValid`."],
    ["Null values are valid for custom constraints; `@NotNull` reports them once.", "Same-day range is invalid."],
    ["Single responsibility: each constraint checks one thing and ignores null.", "`LocalDate.isAfter` is strict."],
    S)

topics = [
    T("DTOs, Bean Validation and @Valid",
      "A **DTO** (data transfer object) is a class/record that defines exactly what crosses the API boundary. **Bean Validation** (Jakarta Validation, implemented by Hibernate Validator) declares rules with annotations (`@NotBlank`, `@Email`, `@Min`, `@Size`, `@Pattern`, `@Positive`...). `@Valid` on a `@RequestBody` argument makes Spring validate it and raise `MethodArgumentNotValidException` (400) on violations; `@Validated` enables validation of `@RequestParam`/`@PathVariable` (yielding `HandlerMethodValidationException` in Spring 6.1+).",
      "Never trust client input. Declarative rules keep validation next to the data, are reusable and produce uniform errors. Separate DTOs prevent mass-assignment (a client setting `role=ADMIN`) and keep the API stable while entities evolve.",
      ["Rules are visible and declarative", "Same constraints reusable in persistence and UI", "Standard error flow", "DTOs hide internal fields and shape responses"],
      ["Mapping boilerplate between DTOs and entities", "Cross-field rules need custom constraints", "Annotation messages need i18n for production"],
      "Without validation, nulls and malformed data propagate into services and databases (NPEs, constraint violations at commit). Binding requests straight to entities lets clients overwrite fields such as `id`, `role`, `createdAt`.",
      "```java\npublic record CreateUserRequest(@NotBlank String name, @Email String email, @Min(18) int age) {}\n@PostMapping ResponseEntity<UserResponse> create(@Valid @RequestBody CreateUserRequest r)\n```\nRequires `spring-boot-starter-validation`. Groups (`@Validated(OnCreate.class)`) select rule sets. `@NotNull` vs `@NotBlank` vs `@NotEmpty`: null / not blank text / not empty collection or string.",
      [("Constraint set", "java", "record SignUp(@NotBlank @Size(max = 50) String name,\n               @NotBlank @Email String email,\n               @Pattern(regexp = \"^[A-Z]{2}\\\\d{4}$\") String code) {}"),
       ("Validating a path variable", "java", "@Validated @RestController class C {\n  @GetMapping(\"/{id}\") Item get(@PathVariable @Positive long id) {...}\n}"),
       ("Nested validation", "java", "record Order(@NotEmpty List<@Valid Line> lines) {}\nrecord Line(@NotBlank String sku, @Positive int qty) {}")],
      [("@NotNull vs @NotBlank?", "`@NotNull` rejects only null; `@NotBlank` also rejects empty/whitespace strings."),
       ("What does @Valid trigger?", "Validation of the annotated argument; failures raise `MethodArgumentNotValidException`."),
       ("Why use separate request/response DTOs?", "To control exposed fields, avoid mass assignment and decouple the API from the persistence model.")]),
    T("@RestControllerAdvice, ProblemDetail and error handling",
      "`@RestControllerAdvice` is a global `@ControllerAdvice` + `@ResponseBody`: its `@ExceptionHandler` methods translate exceptions from any controller into responses. **ProblemDetail** is Spring 6's model for RFC 9457 (`application/problem+json`) with `type`, `title`, `status`, `detail`, `instance` and custom properties. Enable it for built-in MVC exceptions with `spring.mvc.problemdetails.enabled=true` or by extending `ResponseEntityExceptionHandler`.",
      "Consistent, machine-readable errors let clients react (show field errors, retry, report) without parsing ad-hoc JSON. Central handling removes try/catch noise from controllers.",
      ["One place for error policy", "Standard format understood by tooling", "Controllers stay focused on the happy path", "Easy to add correlation ids and error codes"],
      ["Global handlers can mask exceptions if too broad (`Exception.class`)", "Handler order/specificity matters", "Must avoid leaking stack traces or internals"],
      "Without central handling, unhandled exceptions become 500 with Boot's default error JSON (possibly with message/trace depending on config). Each controller reinvents try/catch and formats differ.",
      "```java\n@RestControllerAdvice\nclass ApiErrors {\n  @ExceptionHandler(NotFound.class)\n  ProblemDetail notFound(NotFound e) {\n    ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());\n    pd.setTitle(\"Not Found\");\n    return pd;\n  }\n}\n```\nMost specific exception type wins. Use `@ResponseStatus` on an exception class for the simple cases.",
      [("Custom property", "java", "pd.setProperty(\"errors\", Map.of(\"email\", \"must be a well-formed email address\"));"),
       ("Extend base handler", "java", "@RestControllerAdvice\nclass Handler extends ResponseEntityExceptionHandler {}\n// + spring.mvc.problemdetails.enabled=true"),
       ("Exception with status", "java", "@ResponseStatus(HttpStatus.NOT_FOUND)\nclass NotFound extends RuntimeException {}")],
      [("What media type does ProblemDetail use?", "`application/problem+json`."),
       ("Which exception signals a failed @Valid body?", "`MethodArgumentNotValidException`."),
       ("Why not catch `Exception` globally and return 500 details?", "It hides root causes and may leak internals; handle known types and let the rest log and return a generic 500.")]),
    T("Layered architecture: controller, service, repository, mapper",
      "Typical Spring layering: **controller** (HTTP: binding, status codes), **service** (business rules and transactions), **repository** (persistence), plus **mappers** that convert between entities/domain objects and DTOs. Dependencies point inward: controller -> service -> repository; lower layers never depend on HTTP types.",
      "Separation lets you test rules without a web server, swap storage, and keep controllers thin. Transaction boundaries and security rules live naturally in the service layer.",
      ["Testability (unit test services with fakes)", "Clear ownership of responsibilities", "Reuse of services across controllers, jobs and messaging", "Easier refactoring"],
      ["More classes for small apps", "Pass-through services add noise", "Mappers need maintenance (or a library such as MapStruct)"],
      "Fat controllers mix parsing, rules and SQL, so logic cannot be reused or tested without HTTP. Letting controllers call repositories skips transactions and business checks.",
      "```text\ncontroller  -> service -> repository -> database\n   |          |\n  DTO       domain/entity\n```\nConstructor injection everywhere; one public method per use case; throw domain exceptions (`TodoNotFoundException`) and translate them in the advice.",
      [("Thin controller", "java", "@PostMapping TodoDto create(@Valid @RequestBody CreateTodo r) { return service.create(r.title()); }"),
       ("Service rule", "java", "if (repo.existsByTitleIgnoreCase(title)) throw new DuplicateTodoException(title);"),
       ("Mapper", "java", "static TodoDto toDto(Todo t) { return new TodoDto(t.id(), t.title(), t.done() ? \"DONE\" : \"OPEN\"); }")],
      [("Where do business rules belong?", "In the service layer."),
       ("Why should controllers not use repositories directly?", "It bypasses business rules/transactions and couples HTTP to persistence."),
       ("What does a mapper protect against?", "Leaking entity internals and mass assignment.")]),
]

day(31, "REST II: DTOs, Bean Validation, Error Handling and Layered Design", "Spring Boot",
    "Production-shaped REST APIs: validated DTOs, uniform error responses and a layered codebase",
    ["Model requests/responses with DTO records", "Validate input with Bean Validation and write custom constraints", "Translate exceptions to ProblemDetail with @RestControllerAdvice", "Organize code in controller/service/repository/mapper layers"],
    ["Day 30 REST I"],
    topics, [a1, a2, a3, a4],
    [("Why DTOs instead of entities in the API?", "Stability, security (mass assignment) and avoiding lazy-loading/serialization problems."),
     ("How does Spring turn validation errors into 400?", "Argument resolution raises MethodArgumentNotValidException which the default or custom handler maps to 400."),
     ("What is ProblemDetail?", "Spring's RFC 9457 error representation."),
     ("Controller vs service responsibility?", "Controller adapts HTTP; service owns rules and transactions."),
     ("How do you validate a path variable?", "`@Validated` on the controller plus constraints on the parameter.")],
    ["Forgetting `spring-boot-starter-validation`.", "Putting `@Valid` on the wrong parameter or omitting it.", "Catching `Exception` in the advice.", "Returning entities from controllers."],
    ["Spring Framework Reference: Error Responses", "Jakarta Bean Validation specification", "RFC 9457 Problem Details"],
    [("DTO", "Object defining an API payload"), ("ProblemDetail", "RFC 9457 error model"), ("ConstraintValidator", "Custom validation logic"),
     ("Controller advice", "Global exception/model handling"), ("Mass assignment", "Client setting fields it should not")],
    "2–3 h theory + 3–5 h tasks", spring=True)
