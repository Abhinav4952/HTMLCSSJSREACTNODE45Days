from sx import *

S = ["spring-boot-starter-aop"]
TYPE = "Spring AOP"

CFG = r'''package %PKG%;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

/** PROVIDED: enables @AspectJ support and scans this package for services and aspects. */
@Configuration
@EnableAspectJAutoProxy
@ComponentScan(basePackageClasses = AopConfig.class)
public class AopConfig {
}
'''
REC = r'''package %PKG%;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.springframework.stereotype.Component;

/** PROVIDED: collects events so tests can observe advice execution order. */
@Component
public class CallRecorder {
    private final List<String> events = Collections.synchronizedList(new ArrayList<>());

    public void add(String event) {
        events.add(event);
    }

    public List<String> events() {
        return List.copyOf(events);
    }

    public void clear() {
        events.clear();
    }
}
'''

# ------------------------------------------------------------ task 1
ORDER_SVC = r'''package %PKG%;

import org.springframework.stereotype.Service;

/** PROVIDED target bean. */
@Service
public class OrderService {

    public String place(String item) {
        return "order:" + item;
    }

    public void fail() {
        throw new IllegalStateException("boom");
    }
}
'''
AUDIT = r'''package %PKG%;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

//A! declare this class as an aspect and a Spring bean (@Aspect + @Component)
@Aspect
@Component
//E!
public class AuditAspect {

    private final CallRecorder recorder;

    public AuditAspect(CallRecorder recorder) {
        this.recorder = recorder;
    }

    /** All methods of OrderService. */
    @Pointcut("execution(* %PKG%.OrderService.*(..))")
    public void orderOps() {
    }

    /** records "before:<method name>" */
    //A! run before orderOps()
    @Before("orderOps()")
    //E!
    public void before(JoinPoint jp) {
        //B! record before:<method>
        recorder.add("before:" + jp.getSignature().getName());
        //E!
    }

    /** records "returned:<method>=<result>" (only when the method completes normally) */
    //A! run after normal return, binding the result to the parameter named result
    @AfterReturning(pointcut = "orderOps()", returning = "result")
    //E!
    public void returned(JoinPoint jp, Object result) {
        //B! record returned:<method>=<result>
        recorder.add("returned:" + jp.getSignature().getName() + "=" + result);
        //E!
    }

    /** records "threw:<method>:<exception simple name>" (only when an exception escapes) */
    //A! run after an exception, binding it to the parameter named ex
    @AfterThrowing(pointcut = "orderOps()", throwing = "ex")
    //E!
    public void threw(JoinPoint jp, Throwable ex) {
        //B! record threw:<method>:<exception simple class name>
        recorder.add("threw:" + jp.getSignature().getName() + ":" + ex.getClass().getSimpleName());
        //E!
    }

    /** records "finally:<method>" (always) */
    //A! run after the method no matter how it ended
    @After("orderOps()")
    //E!
    public void atEnd(JoinPoint jp) {
        //B! record finally:<method>
        recorder.add("finally:" + jp.getSignature().getName());
        //E!
    }
}
'''
T1 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class AdviceTypesTest {

    AnnotationConfigApplicationContext ctx;
    OrderService service;
    CallRecorder recorder;

    @BeforeEach
    void start() {
        ctx = new AnnotationConfigApplicationContext(AopConfig.class);
        service = ctx.getBean(OrderService.class);
        recorder = ctx.getBean(CallRecorder.class);
        recorder.clear();
    }

    @AfterEach
    void stop() {
        ctx.close();
    }

    @Test
    void serviceIsProxied() {
        assertThat(AopUtils.isAopProxy(service)).isTrue();
    }

    @Test
    void normalCallRunsBeforeReturnedAndFinally() {
        assertThat(service.place("pen")).isEqualTo("order:pen");
        assertThat(recorder.events()).containsExactly("before:place", "returned:place=order:pen", "finally:place");
    }

    @Test
    void failingCallRunsBeforeThrewAndFinally() {
        assertThatThrownBy(() -> service.fail()).isInstanceOf(IllegalStateException.class).hasMessage("boom");
        assertThat(recorder.events()).containsExactly("before:fail", "threw:fail:IllegalStateException", "finally:fail");
    }

    @Test
    void adviceDoesNotRunForOtherBeans() {
        recorder.add("manual");
        assertThat(recorder.events()).containsExactly("manual");
    }
}
'''
a1 = tk("advice-types-order-service", "Before, AfterReturning, AfterThrowing and After", "Warm-up",
    "Write an @Aspect with the four classic advice types and observe their order for success and failure.",
    {"main/AopConfig.java": CFG, "main/CallRecorder.java": REC, "main/OrderService.java": ORDER_SVC, "main/AuditAspect.java": AUDIT},
    {"test/AdviceTypesTest.java": T1},
    ["Mark `AuditAspect` as an aspect and bean.", "Annotate the four advice methods and implement the recorded messages."],
    ["`@AfterReturning` must not run when an exception escapes; `@AfterThrowing` must not run on success.", "`@After` always runs (like `finally`).", "Aspects only apply to Spring beans called through the proxy."],
    ["`returning`/`throwing` names must match the advice method parameter names.", "`JoinPoint#getSignature().getName()` gives the method name."],
    S, ttype=TYPE)

# ------------------------------------------------------------ task 2
TIMED = "package %PKG%;\n\nimport java.lang.annotation.ElementType;\nimport java.lang.annotation.Retention;\nimport java.lang.annotation.RetentionPolicy;\nimport java.lang.annotation.Target;\n\n/** Marker: measure the duration of this method. */\n@Target(ElementType.METHOD)\n@Retention(RetentionPolicy.RUNTIME)\npublic @interface Timed {\n}\n"
METRICS = r'''package %PKG%;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Component;

/** PROVIDED registry of call counts and total nanoseconds by method name. */
@Component
public class MetricsRegistry {
    private final Map<String, AtomicLong> counts = new ConcurrentHashMap<>();
    private final Map<String, AtomicLong> totals = new ConcurrentHashMap<>();

    public void record(String name, long nanos) {
        counts.computeIfAbsent(name, k -> new AtomicLong()).incrementAndGet();
        totals.computeIfAbsent(name, k -> new AtomicLong()).addAndGet(nanos);
    }

    public long count(String name) {
        AtomicLong c = counts.get(name);
        return c == null ? 0 : c.get();
    }

    public long totalNanos(String name) {
        AtomicLong t = totals.get(name);
        return t == null ? 0 : t.get();
    }
}
'''
REPORT = r'''package %PKG%;

import org.springframework.stereotype.Service;

@Service
public class ReportService {

    @Timed
    public String build() throws InterruptedException {
        Thread.sleep(5);
        return "report";
    }

    @Timed
    public String explode() {
        throw new IllegalArgumentException("bad report");
    }

    public String untimed() {
        return "plain";
    }
}
'''
TEXTSVC = r'''package %PKG%;

import org.springframework.stereotype.Service;

@Service
public class TextService {

    public String shout(String s) {
        return s.toUpperCase() + "!";
    }

    public String echo(String s) {
        return s;
    }

    public int twice(int n) {
        return n * 2;
    }
}
'''
TIMING = r'''package %PKG%;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

//A! make this an aspect bean
@Aspect
@Component
//E!
public class TimingAspect {

    private final MetricsRegistry registry;

    public TimingAspect(MetricsRegistry registry) {
        this.registry = registry;
    }

    /**
     * Around every method annotated with @Timed: measure with System.nanoTime(), ALWAYS record the duration under the
     * method name (also when the method throws), and let the original result/exception pass through unchanged.
     */
    //A! @Around on methods annotated with Timed (pointcut: @annotation(%PKG%.Timed))
    @Around("@annotation(%PKG%.Timed)")
    //E!
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        //B! time pjp.proceed() in try/finally and record under pjp.getSignature().getName()
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            registry.record(pjp.getSignature().getName(), System.nanoTime() - start);
        }
        //E!
    }
}
'''
TRIM = r'''package %PKG%;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

//A! make this an aspect bean
@Aspect
@Component
//E!
public class TrimAspect {

    /**
     * Around every TextService method whose only parameter is a String: replace String arguments by their trimmed
     * version before proceeding (pjp.proceed(newArgs)). Pointcut: execution(* %PKG%.TextService.*(String)).
     */
    //A! @Around with execution(* %PKG%.TextService.*(String))
    @Around("execution(* %PKG%.TextService.*(String))")
    //E!
    public Object trim(ProceedingJoinPoint pjp) throws Throwable {
        //B! copy args, trim strings, proceed with the new arguments
        Object[] args = pjp.getArgs().clone();
        for (int i = 0; i < args.length; i++) {
            if (args[i] instanceof String s) {
                args[i] = s.trim();
            }
        }
        return pjp.proceed(args);
        //E!
    }
}
'''
T2 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class AroundAdviceTest {

    AnnotationConfigApplicationContext ctx;
    ReportService reports;
    TextService text;
    MetricsRegistry metrics;

    @BeforeEach
    void start() {
        ctx = new AnnotationConfigApplicationContext(AopConfig.class);
        reports = ctx.getBean(ReportService.class);
        text = ctx.getBean(TextService.class);
        metrics = ctx.getBean(MetricsRegistry.class);
    }

    @AfterEach
    void stop() {
        ctx.close();
    }

    @Test
    void timedMethodIsMeasuredAndResultPassesThrough() throws Exception {
        assertThat(reports.build()).isEqualTo("report");
        assertThat(metrics.count("build")).isEqualTo(1);
        assertThat(metrics.totalNanos("build")).isGreaterThanOrEqualTo(4_000_000L);
    }

    @Test
    void exceptionsAreRecordedAndRethrownUnchanged() {
        assertThatThrownBy(() -> reports.explode()).isInstanceOf(IllegalArgumentException.class).hasMessage("bad report");
        assertThat(metrics.count("explode")).isEqualTo(1);
    }

    @Test
    void untimedMethodsAreNotRecorded() {
        reports.untimed();
        assertThat(metrics.count("untimed")).isZero();
    }

    @Test
    void stringArgumentsAreTrimmedByAroundAdvice() {
        assertThat(text.shout("  hi  ")).isEqualTo("HI!");
        assertThat(text.echo("\t x \n")).isEqualTo("x");
    }

    @Test
    void otherSignaturesAreUntouched() {
        assertThat(text.twice(21)).isEqualTo(42);
    }
}
'''
a2 = tk("around-timing-and-args", "@Around: Timing and Argument Rewriting", "Core",
    "Use around advice for cross-cutting timing (with try/finally) and to rewrite method arguments before proceeding.",
    {"main/AopConfig.java": CFG, "main/Timed.java": TIMED, "main/MetricsRegistry.java": METRICS, "main/ReportService.java": REPORT,
     "main/TextService.java": TEXTSVC, "main/TimingAspect.java": TIMING, "main/TrimAspect.java": TRIM},
    {"test/AroundAdviceTest.java": T2},
    ["Implement `TimingAspect` (annotation-driven pointcut, always record).", "Implement `TrimAspect` and pass modified arguments to `proceed`."],
    ["Always call `proceed()` exactly once unless you intentionally short-circuit.", "Rethrow exceptions; never swallow them in an around advice.", "`pjp.getArgs()` returns a copy-safe array but modify a clone for clarity."],
    ["`try/finally` guarantees the metric is recorded on failure.", "`pjp.proceed(Object[])` replaces the arguments."],
    S, ttype=TYPE)

# ------------------------------------------------------------ task 3
AUDITED = "package %PKG%.sample;\n\nimport java.lang.annotation.ElementType;\nimport java.lang.annotation.Retention;\nimport java.lang.annotation.RetentionPolicy;\nimport java.lang.annotation.Target;\n\n@Target(ElementType.METHOD)\n@Retention(RetentionPolicy.RUNTIME)\npublic @interface Audited {\n}\n"
USVC = "package %PKG%.sample;\n\npublic class UserService {\n    public String find(long id) {\n        return \"u\" + id;\n    }\n\n    @Audited\n    public void save(String name) {\n    }\n\n    public int count() {\n        return 0;\n    }\n}\n"
OSVC = "package %PKG%.sample;\n\npublic class OrderService {\n    public void place(String item, int qty) {\n    }\n\n    public void cancel(long id) {\n    }\n}\n"
UCTL = "package %PKG%.sample.web;\n\nimport %PKG%.sample.Audited;\n\npublic class UserController {\n    public String get(long id) {\n        return \"u\" + id;\n    }\n\n    // not audited on purpose\n    public void save(String name) {\n    }\n}\n"
PCS = r'''package %PKG%;

/**
 * AspectJ pointcut expressions (as Strings) for the sample classes in %PKG%.sample:
 *   UserService:      find(long), save(String) [@Audited], count()
 *   OrderService:     place(String, int), cancel(long)
 *   web.UserController: get(long), save(String)
 */
public final class PointcutExpressions {

    private PointcutExpressions() {
    }

    /** every method of every class whose simple name ends with "Service" in package %PKG%.sample (not sub-packages) */
    public static String allInServices() {
        //B! execution(...) with a *Service type pattern
        return "execution(* %PKG%.sample.*Service.*(..))";
        //E!
    }

    /** every method named save that takes exactly one String parameter, in any class of any package */
    public static String saveWithString() {
        //B! execution with any declaring type
        return "execution(* *..*.save(String))";
        //E!
    }

    /** every method with exactly two parameters of any type */
    public static String twoArguments() {
        //B! execution with (*, *)
        return "execution(* *(*, *))";
        //E!
    }

    /** every method of classes in %PKG%.sample.web and its sub-packages (use within) */
    public static String webLayer() {
        //B! within(...) with a .. pattern
        return "within(%PKG%.sample.web..*)";
        //E!
    }

    /** every method carrying the @Audited annotation */
    public static String audited() {
        //B! @annotation(...)
        return "@annotation(%PKG%.sample.Audited)";
        //E!
    }

    /** everything in %PKG%.sample (all sub-packages) EXCEPT the web layer: combine execution(...) && !within(...) */
    public static String serviceLayerOnly() {
        //B! boolean combination
        return "execution(* %PKG%.sample..*(..)) && !within(%PKG%.sample.web..*)";
        //E!
    }
}
'''
T3 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;

import %PKG%.sample.OrderService;
import %PKG%.sample.UserService;
import %PKG%.sample.web.UserController;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.aop.aspectj.AspectJExpressionPointcut;

class PointcutExpressionsTest {

    record Target(Class<?> type, String method, Class<?>... params) {
        Method resolve() throws Exception {
            return type.getMethod(method, params);
        }

        @Override
        public String toString() {
            return type.getSimpleName() + "." + method;
        }
    }

    static final List<Target> ALL = List.of(
            new Target(UserService.class, "find", long.class),
            new Target(UserService.class, "save", String.class),
            new Target(UserService.class, "count"),
            new Target(OrderService.class, "place", String.class, int.class),
            new Target(OrderService.class, "cancel", long.class),
            new Target(UserController.class, "get", long.class),
            new Target(UserController.class, "save", String.class));

    private static List<String> matched(String expression) throws Exception {
        AspectJExpressionPointcut pc = new AspectJExpressionPointcut();
        pc.setExpression(expression);
        List<String> out = new ArrayList<>();
        for (Target t : ALL) {
            if (pc.matches(t.resolve(), t.type())) {
                out.add(t.toString());
            }
        }
        return out;
    }

    @Test
    void allInServices() throws Exception {
        assertThat(matched(PointcutExpressions.allInServices())).containsExactly(
                "UserService.find", "UserService.save", "UserService.count", "OrderService.place", "OrderService.cancel");
    }

    @Test
    void saveWithString() throws Exception {
        assertThat(matched(PointcutExpressions.saveWithString())).containsExactly("UserService.save", "UserController.save");
    }

    @Test
    void twoArguments() throws Exception {
        assertThat(matched(PointcutExpressions.twoArguments())).containsExactly("OrderService.place");
    }

    @Test
    void webLayer() throws Exception {
        assertThat(matched(PointcutExpressions.webLayer())).containsExactly("UserController.get", "UserController.save");
    }

    @Test
    void audited() throws Exception {
        assertThat(matched(PointcutExpressions.audited())).containsExactly("UserService.save");
    }

    @Test
    void serviceLayerOnly() throws Exception {
        assertThat(matched(PointcutExpressions.serviceLayerOnly())).containsExactly(
                "UserService.find", "UserService.save", "UserService.count", "OrderService.place", "OrderService.cancel");
    }
}
'''
a3 = tk("pointcut-expressions-lab", "Pointcut Expression Lab", "Core",
    "Practice AspectJ pointcut designators (execution, within, @annotation, boolean combinations) and verify them against real methods.",
    {"main/PointcutExpressions.java": PCS, "main/sample/Audited.java": AUDITED, "main/sample/UserService.java": USVC,
     "main/sample/OrderService.java": OSVC, "main/sample/web/UserController.java": UCTL},
    {"test/PointcutExpressionsTest.java": T3},
    ["Write six pointcut expressions in `PointcutExpressions` according to their Javadoc."],
    ["`execution` matches method signatures; `within` matches the declaring type's package/class.", "`..` in a package pattern includes sub-packages; `.` alone does not.", "Spring AOP supports only method-execution join points on beans."],
    ["Format: `execution(modifiers? return-type declaring-type?.name(params))`.", "Combine with `&&`, `||`, `!`."],
    S, ttype=TYPE)

# ------------------------------------------------------------ task 4
PCUT = r'''package %PKG%;

import org.aspectj.lang.annotation.Pointcut;

/** PROVIDED: a shared, named pointcut that aspects can reference. */
public class Pointcuts {

    @Pointcut("execution(* %PKG%.PaymentService.pay(..))")
    public void payment() {
    }
}
'''
PAY = r'''package %PKG%;

import org.springframework.stereotype.Service;

@Service
public class PaymentService {

    private final CallRecorder recorder;

    public PaymentService(CallRecorder recorder) {
        this.recorder = recorder;
    }

    public String pay(String user) {
        recorder.add("pay:" + user);
        if ("bad".equals(user)) {
            throw new IllegalStateException("declined");
        }
        return "paid:" + user;
    }
}
'''
SEC = r'''package %PKG%;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

//A! aspect bean with the HIGHEST precedence of the two (@Order(1))
@Aspect
@Component
@Order(1)
//E!
public class SecurityAspect {

    private final CallRecorder recorder;

    public SecurityAspect(CallRecorder recorder) {
        this.recorder = recorder;
    }

    /** records "security:in" before proceeding and "security:out" afterwards, even when the call fails. */
    //A! @Around using the named pointcut Pointcuts.payment()
    @Around("%PKG%.Pointcuts.payment()")
    //E!
    public Object guard(ProceedingJoinPoint pjp) throws Throwable {
        //B! record in, proceed, record out in finally
        recorder.add("security:in");
        try {
            return pjp.proceed();
        } finally {
            recorder.add("security:out");
        }
        //E!
    }
}
'''
TX = r'''package %PKG%;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

//A! aspect bean with LOWER precedence than SecurityAspect (@Order(2))
@Aspect
@Component
@Order(2)
//E!
public class TxAspect {

    private final CallRecorder recorder;

    public TxAspect(CallRecorder recorder) {
        this.recorder = recorder;
    }

    /** records "tx:begin"; after success "tx:commit"; on any Throwable "tx:rollback" and rethrows it. */
    //A! @Around using the named pointcut Pointcuts.payment()
    @Around("%PKG%.Pointcuts.payment()")
    //E!
    public Object transaction(ProceedingJoinPoint pjp) throws Throwable {
        //B! begin, proceed, commit or rollback
        recorder.add("tx:begin");
        try {
            Object result = pjp.proceed();
            recorder.add("tx:commit");
            return result;
        } catch (Throwable t) {
            recorder.add("tx:rollback");
            throw t;
        }
        //E!
    }
}
'''
T4 = r'''package %PKG%;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

class AspectOrderingTest {

    AnnotationConfigApplicationContext ctx;
    PaymentService service;
    CallRecorder recorder;

    @BeforeEach
    void start() {
        ctx = new AnnotationConfigApplicationContext(AopConfig.class);
        service = ctx.getBean(PaymentService.class);
        recorder = ctx.getBean(CallRecorder.class);
        recorder.clear();
    }

    @AfterEach
    void stop() {
        ctx.close();
    }

    @Test
    void classBasedProxyBecausePaymentServiceHasNoInterface() {
        assertThat(AopUtils.isCglibProxy(service)).isTrue();
    }

    @Test
    void successOrderIsOnionShaped() {
        assertThat(service.pay("alice")).isEqualTo("paid:alice");
        assertThat(recorder.events()).containsExactly("security:in", "tx:begin", "pay:alice", "tx:commit", "security:out");
    }

    @Test
    void failureRollsBackInsideSecurity() {
        assertThatThrownBy(() -> service.pay("bad")).isInstanceOf(IllegalStateException.class).hasMessage("declined");
        assertThat(recorder.events()).containsExactly("security:in", "tx:begin", "pay:bad", "tx:rollback", "security:out");
    }
}
'''
a4 = tk("aspect-ordering-challenge", "Aspect Ordering with @Order", "Challenge",
    "Combine two around aspects on a shared named pointcut and control their nesting with @Order.",
    {"main/AopConfig.java": CFG, "main/CallRecorder.java": REC, "main/Pointcuts.java": PCUT, "main/PaymentService.java": PAY,
     "main/SecurityAspect.java": SEC, "main/TxAspect.java": TX},
    {"test/AspectOrderingTest.java": T4},
    ["Make both classes aspect beans with explicit precedence (`@Order(1)` outer, `@Order(2)` inner).", "Reference the shared pointcut `Pointcuts.payment()` from both advices.", "Implement both around bodies so the recorded sequence is onion-shaped."],
    ["Lower `@Order` value = higher precedence = outermost.", "An exception must travel through `tx:rollback` first, then `security:out`.", "Without `@Order` the order is undefined."],
    ["Think of the aspects as nested try/finally blocks.", "Named pointcuts from another class are referenced as `fully.qualified.Class.method()`."],
    S, ttype=TYPE)

topics = [
    T("AOP concepts: aspects, join points, pointcuts and advice",
      "**Aspect-oriented programming** modularizes cross-cutting concerns (logging, security checks, transactions, metrics). Vocabulary: **aspect** (the module), **join point** (a point in execution - in Spring AOP always a method execution on a Spring bean), **pointcut** (predicate selecting join points), **advice** (code run at them: `@Before`, `@After`, `@AfterReturning`, `@AfterThrowing`, `@Around`), **weaving** (applying aspects). Spring AOP weaves at runtime by creating **proxies** (JDK dynamic proxies for interfaces, CGLIB subclasses otherwise).",
      "Without AOP, concerns like transactions or auditing are copy-pasted into every service method, obscuring business logic. `@Transactional`, `@Cacheable`, `@Async` and Spring Security method security are all implemented as AOP advice.",
      ["Removes duplication of cross-cutting code", "Business classes stay focused", "Declarative and centrally changeable", "Foundation of many Spring features"],
      ["Proxy-based: self-invocation bypasses advice", "Only public method calls on Spring beans are advised (by default)", "Debugging through proxies is harder", "Hidden behavior can surprise readers"],
      "Hand-written try/finally timing code in 50 methods drifts and gets forgotten. Conversely, putting business rules in aspects hides logic where nobody looks. Calling `this.method()` inside a bean skips the proxy, so advice silently does not run.",
      "```java\n@Aspect @Component\nclass AuditAspect {\n  @Pointcut(\"execution(* com.acme.OrderService.*(..))\") void orderOps() {}\n  @Before(\"orderOps()\")        void before(JoinPoint jp) {...}\n  @AfterReturning(pointcut = \"orderOps()\", returning = \"r\") void ok(Object r) {...}\n  @AfterThrowing(pointcut = \"orderOps()\", throwing = \"ex\")  void failed(Throwable ex) {...}\n  @After(\"orderOps()\")         void always() {...}\n}\n```\nEnable with `spring-boot-starter-aop` (auto-configured) or `@EnableAspectJAutoProxy`.",
      [("Proxy check", "java", "AopUtils.isAopProxy(bean); AopUtils.isCglibProxy(bean);"),
       ("Self-invocation pitfall", "java", "public void a() { this.b(); }   // b()'s advice does NOT run\n@Transactional public void b() {...}"),
       ("Dependency", "xml", "<dependency><groupId>org.springframework.boot</groupId><artifactId>spring-boot-starter-aop</artifactId></dependency>")],
      [("What is a join point in Spring AOP?", "A method execution on a Spring-managed bean."),
       ("Which advice always runs?", "`@After` (like finally)."),
       ("Why does self-invocation skip advice?", "The call does not go through the proxy.")]),
    T("Pointcut expressions",
      "AspectJ pointcut designators select join points: `execution(modifiers? ret declaring.name(params) throws?)` (the workhorse), `within(type pattern)`, `this`/`target`, `args`, `@annotation(...)`, `@within(...)`, `bean(name)`. Wildcards: `*` one segment/any single element, `..` any number of packages or parameters. Combine with `&&`, `||`, `!`. Name reusable ones with `@Pointcut`.",
      "A precise pointcut decides what gets advised: too broad slows the app and surprises; too narrow misses calls.",
      ["Declarative selection by structure or annotation", "Composable and reusable", "Annotation-based pointcuts decouple from package layout"],
      ["Strings are not compile-checked (typos match nothing silently)", "Package refactors break `execution` patterns", "Complex expressions are hard to read"],
      "A typo in a package name results in an aspect that never fires - and no error. Overly broad `execution(* *(..))` advises framework beans and can break startup.",
      "```text\nexecution(* com.acme.service.*.*(..))       all methods of classes directly in service\nexecution(* com.acme..*Service.*(..))        any *Service in com.acme and sub-packages\nexecution(* *..*.save(String))               any save(String)\nwithin(com.acme.web..*)                      all types in web package tree\n@annotation(com.acme.Audited)                methods annotated with @Audited\nexecution(* com.acme..*(..)) && !within(com.acme.web..*)\n```\nPrefer annotation-driven pointcuts for opt-in behavior (`@Timed`).",
      [("Named pointcut", "java", "@Pointcut(\"within(@org.springframework.stereotype.Service *)\")\nvoid services() {}"),
       ("Binding arguments", "java", "@Before(\"execution(* *(..)) && args(id,..)\")\nvoid log(long id) {...}"),
       ("Test a pointcut", "java", "AspectJExpressionPointcut pc = new AspectJExpressionPointcut(); pc.setExpression(expr);\nboolean m = pc.matches(method, targetClass);")],
      [("`..` in a package pattern means?", "Any number of sub-packages."),
       ("execution vs within?", "execution matches method signatures; within matches the declaring type location."),
       ("How can you unit-test a pointcut?", "With `AspectJExpressionPointcut#matches`.")]),
    T("Around advice, ordering and common pitfalls",
      "`@Around` wraps the call: you receive a `ProceedingJoinPoint`, decide whether/when to call `proceed()` (optionally with replaced arguments), may transform the result or exception, and can short-circuit (e.g. cache hit). Multiple aspects form an onion; `@Order(n)` (or `Ordered`) sets precedence - the lowest value is the outermost. Within one aspect the order is Around, Before, After, AfterReturning/AfterThrowing on the way in.",
      "Timing, caching, retry, transaction and security checks need control over the call itself. Ordering decides correctness: authentication must run before the transaction opens, retries outside of transactions.",
      ["Full control over invocation", "Composable via ordering", "Single place for retry/metrics/cache logic"],
      ["Forgetting `proceed()` silently skips the target", "Swallowing exceptions hides failures", "Ordering bugs are subtle", "Performance overhead when pointcuts are broad"],
      "An around advice that catches `Exception` and returns null converts failures into silent nulls. Two aspects without `@Order` run in unspecified order, so a test passes locally and fails in CI. Private methods, final classes/methods (CGLIB) and `this.` calls are not advised.",
      "```java\n@Around(\"@annotation(com.acme.Timed)\")\nObject time(ProceedingJoinPoint pjp) throws Throwable {\n  long t0 = System.nanoTime();\n  try { return pjp.proceed(); }\n  finally { metrics.record(pjp.getSignature().getName(), System.nanoTime() - t0); }\n}\n@Aspect @Order(1) class SecurityAspect {...}   // outermost\n@Aspect @Order(2) class TxAspect {...}\n```",
      [("Rewrite arguments", "java", "Object[] args = pjp.getArgs().clone(); args[0] = ((String) args[0]).trim(); return pjp.proceed(args);"),
       ("Short-circuit (cache)", "java", "Object hit = cache.get(key); if (hit != null) return hit; return cache.put(key, pjp.proceed());"),
       ("Retry", "java", "for (int i = 0; ; i++) { try { return pjp.proceed(); } catch (TransientException e) { if (i == 2) throw e; } }")],
      [("What is the outermost aspect with @Order(1) and @Order(2)?", "@Order(1)."),
       ("Must an around advice call proceed()?", "Not always (short-circuit), but normally exactly once."),
       ("Why might advice not run on a bean method?", "Self-invocation, private/final methods, or the object is not a Spring bean.")]),
]

day(40, "Spring AOP: Aspects, Pointcuts and Advice", "Spring Boot",
    "Cross-cutting concerns with proxies: advice types, pointcut expressions, around advice and aspect ordering",
    ["Explain aspects, join points, pointcuts, advice and proxies", "Write @Before/@AfterReturning/@AfterThrowing/@After/@Around advice", "Compose pointcut expressions and test them", "Control aspect precedence with @Order", "Recognize AOP pitfalls (self-invocation, final/private methods)"],
    ["Day 28-29 Spring Core and Boot", "Day 35 @Transactional (an AOP application)"],
    topics, [a1, a2, a3, a4],
    [("How does Spring AOP work?", "Runtime proxies (JDK or CGLIB) intercept method calls and run advice."),
     ("JDK proxy vs CGLIB?", "JDK proxies implement interfaces; CGLIB subclasses the class (Boot defaults to CGLIB)."),
     ("Name AOP-based Spring features.", "@Transactional, @Cacheable, @Async, @PreAuthorize."),
     ("Spring AOP vs AspectJ?", "Spring AOP is proxy-based and method-only; AspectJ weaves bytecode and supports more join points."),
     ("How do you order aspects?", "@Order or implementing Ordered; lowest value is outermost.")],
    ["Self-invocation.", "Missing `proceed()`.", "Swallowing exceptions.", "Overly broad pointcuts.", "Final classes/methods with CGLIB."],
    ["Spring Framework Reference: Aspect Oriented Programming with Spring", "AspectJ pointcut language cheat sheet"],
    [("Aspect", "Module encapsulating a cross-cutting concern"), ("Join point", "Point in execution (method call)"), ("Pointcut", "Selector for join points"),
     ("Advice", "Code run at a join point"), ("Proxy", "Wrapper object that applies advice")],
    "2–3 h theory + 3–5 h tasks", spring=True)
