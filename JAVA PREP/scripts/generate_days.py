#!/usr/bin/env python3
"""Generate JAVA PREP Day folders with theory, README, and 4 Maven tasks each."""
from __future__ import annotations

import os
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# day_num, title, phase, learning_objectives, prerequisites, theory_sections, tasks[(slug, title, difficulty, summary, methods)]
DAYS: list[dict] = []


def day(
    num: int,
    title: str,
    phase: str,
    objectives: list[str],
    prereqs: list[str],
    theory: list[tuple[str, str]],
    tasks: list[dict],
    interview: list[str] | None = None,
) -> None:
    DAYS.append(
        {
            "num": num,
            "title": title,
            "phase": phase,
            "objectives": objectives,
            "prereqs": prereqs,
            "theory": theory,
            "tasks": tasks,
            "interview": interview or [],
        }
    )


def task(slug: str, title: str, difficulty: str, summary: str, class_name: str, methods: list[tuple[str, str, str]]) -> dict:
    """methods: (signature_without_semicolon, todo_text, test_description)"""
    return {
        "slug": slug,
        "title": title,
        "difficulty": difficulty,
        "summary": summary,
        "class_name": class_name,
        "methods": methods,
    }


# ---------------------------------------------------------------------------
# DAYS 01-12 Core / OCA
# ---------------------------------------------------------------------------
day(
    1,
    "JDK, JVM, Class Structure, Packages, and First Maven Project",
    "Core Java",
    [
        "Distinguish JDK, JRE, and JVM and explain what each provides",
        "Compile and run a Java class from the command line",
        "Write a valid class with a main method and package declaration",
        "Create and interpret a minimal Maven pom.xml and directory layout",
    ],
    ["None — first day of the course", "Java 21 and Maven installed (see setup/JAVA_AND_MAVEN_SETUP.md)"],
    [
        (
            "JDK, JRE, and JVM",
            "The **JVM** executes bytecode. The **JRE** historically bundled the JVM plus libraries to *run* apps. "
            "The **JDK** adds compilers (`javac`), tools (`jar`, `jcmd`), and APIs to *build* apps. "
            "Modern Temurin distributions ship a full JDK; you develop with the JDK, and production images may slim to a runtime build via `jlink`. "
            "**Why it matters:** interviews ask this constantly; wrong answers signal you have never shipped Java. "
            "**Without the JDK** you cannot compile. **Without a matching major version** (21 vs 17) you get class-file version errors.",
        ),
        (
            "Compiling and running (`javac` / `java`)",
            "Source `.java` → `javac` → `.class` bytecode → `java` launches the JVM and loads the main class. "
            "Package folders must match package names. Example: `com.javaprep.Hello` lives at `com/javaprep/Hello.java`. "
            "Classpath (`-cp`) lists jars and directories of classes. Maven hides this; you still must understand it.",
        ),
        (
            "Class structure and `main`",
            "A public top-level class name must match its file name. `public static void main(String[] args)` is the entry point. "
            "Fields hold state; methods hold behavior. Comments: `//`, `/* */`, and Javadoc `/** */`.",
        ),
        (
            "Packages and imports",
            "Packages organize namespaces and access control (package-private). "
            "`import` brings simple names into scope; `import static` imports static members. "
            "Avoid star-imports in course code except for tests if needed.",
        ),
        (
            "Maven project shape",
            "`pom.xml` defines coordinates (`groupId`, `artifactId`, `version`), dependencies, and the `maven-compiler-plugin` for Java 21. "
            "Standard layout: `src/main/java`, `src/test/java`, `src/main/resources`. `mvn test` compiles and runs JUnit.",
        ),
    ],
    [
        task(
            "hello-main-and-args",
            "Hello Main and Args",
            "Warm-up",
            "Return a greeting that includes the first command-line argument, or a default if none.",
            "HelloGreeter",
            [
                (
                    "public static String greet(String[] args)",
                    "return 'Hello, <name>!' using args[0] when present and non-blank; otherwise 'Hello, World!'",
                    "greets with first arg or World",
                )
            ],
        ),
        task(
            "package-and-import-lab",
            "Package and Import Lab",
            "Core",
            "Build a small util in one package and consume it from another without fully-qualified names in the consumer.",
            "MathUtil",
            [
                (
                    "public static int add(int a, int b)",
                    "return a + b",
                    "adds two ints",
                ),
                (
                    "public static int multiply(int a, int b)",
                    "return a * b",
                    "multiplies two ints",
                ),
            ],
        ),
        task(
            "classpath-class-lookup",
            "Classpath Class Lookup",
            "Stretch",
            "Given a simple name and a map of available FQCNs, resolve which class would be found (simulate import priority).",
            "ClassLookup",
            [
                (
                    "public static String resolve(String simpleName, java.util.Map<String, String> fqcnBySimple)",
                    "return the FQCN for simpleName if present; otherwise throw IllegalArgumentException with a clear message",
                    "resolves or throws",
                )
            ],
        ),
        task(
            "maven-coordinates-reader",
            "Maven Coordinates Reader",
            "Challenge",
            "Parse groupId:artifactId:version from a GAV string and validate each segment is non-blank.",
            "GavParser",
            [
                (
                    "public static String[] parse(String gav)",
                    "split on ':' into exactly 3 non-blank parts; throw IllegalArgumentException otherwise",
                    "parses valid GAV and rejects bad input",
                )
            ],
        ),
    ],
    [
        "What is the difference between JDK, JRE, and JVM?",
        "Why must a public class name match its file name?",
        "What does `mvn test` do in the Maven lifecycle?",
    ],
)

day(
    2,
    "Primitives, References, Variables, Scope, var, and GC Basics",
    "Core Java",
    [
        "List all Java primitive types and their approximate ranges",
        "Explain reference vs primitive assignment and null",
        "Apply default initialization rules for fields vs local variables",
        "Use `var` correctly and describe when GC may reclaim objects",
    ],
    ["Day 01 — class structure and Maven"],
    [
        (
            "Primitive types",
            "`byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean`. "
            "Integer literals default to `int`; use `L` for long. Floating defaults to `double`; use `f` for float. "
            "`char` is UTF-16 code unit. Prefer `int`/`long`/`double`/`boolean` in application code.",
        ),
        (
            "References vs primitives",
            "Primitives store values; references store addresses (or null). Assigning a reference copies the pointer, not the object. "
            "Two references can point to the same object — mutations are visible through both.",
        ),
        (
            "Declaration, initialization, and scope",
            "Local variables must be definitely assigned before use. Instance/static fields get defaults (0, false, null). "
            "Scope is block-based. Shadowing is allowed but confusing — avoid in course code.",
        ),
        (
            "`var` local-variable type inference",
            "`var` requires an initializer and cannot be used for fields or method parameters. "
            "The inferred type is fixed at compile time — not dynamic typing.",
        ),
        (
            "Garbage collection basics",
            "Objects become eligible when unreachable. You cannot force collection. "
            "`finalize` is deprecated/removed for practical use — never rely on it.",
        ),
    ],
    [
        task(
            "primitive-defaults-report",
            "Primitive Defaults Report",
            "Warm-up",
            "Report default values for uninitialized instance fields of each primitive family.",
            "DefaultValues",
            [
                (
                    "public int getIntDefault()",
                    "return the default int field value (0)",
                    "int default is 0",
                ),
                (
                    "public boolean getBooleanDefault()",
                    "return the default boolean field value (false)",
                    "boolean default is false",
                ),
                (
                    "public Object getReferenceDefault()",
                    "return the default reference field value (null)",
                    "reference default is null",
                ),
            ],
        ),
        task(
            "reference-aliasing-lab",
            "Reference Aliasing Lab",
            "Core",
            "Demonstrate and detect whether two int-array references alias the same array.",
            "ArrayAlias",
            [
                (
                    "public static boolean sameArray(int[] a, int[] b)",
                    "return true if a and b refer to the same array object (not merely equal contents)",
                    "detects identity aliasing",
                ),
                (
                    "public static void mutateShared(int[] a, int index, int value)",
                    "set a[index]=value; throw IndexOutOfBoundsException if invalid; throw NullPointerException if a is null",
                    "mutates shared array safely",
                ),
            ],
        ),
        task(
            "scope-and-shadowing",
            "Scope and Shadowing",
            "Stretch",
            "Compute a value using intentional shadowing rules as specified in tests.",
            "ScopeDemo",
            [
                (
                    "public static int compute(int x)",
                    "return x + 10 using a local shadowed name as described in TODO; document the result path",
                    "applies block shadowing correctly",
                )
            ],
        ),
        task(
            "var-inference-guard",
            "Var Inference Guard",
            "Challenge",
            "Classify candidate declarations: valid var, invalid var, or needs explicit type.",
            "VarClassifier",
            [
                (
                    "public static String classify(String declaration)",
                    "return 'VALID', 'INVALID', or 'NEEDS_EXPLICIT' for simplified declaration snippets described in tests",
                    "classifies var declarations",
                )
            ],
        ),
    ],
)

day(
    3,
    "Operators, Numeric Promotion, Casting, and Overflow",
    "Core Java",
    [
        "Apply arithmetic, relational, logical, and assignment operators",
        "Predict numeric promotion results",
        "Use casting safely and explain overflow wraparound",
        "Use compound assignment correctly",
    ],
    ["Day 02 — primitives and references"],
    [
        (
            "Arithmetic and unary operators",
            "`+ - * / %`, unary `+ -`, `++ --` (pre/post). Integer division truncates toward zero. "
            "Division by zero throws `ArithmeticException` for ints; for doubles yields Infinity/NaN.",
        ),
        (
            "Numeric promotion",
            "Binary numeric promotion lifts smaller types toward `int`/`long`/`float`/`double` per JLS rules. "
            "`byte + byte` promotes to `int`.",
        ),
        (
            "Casting and overflow",
            "Narrowing casts truncate. Integer overflow wraps silently (two's complement). "
            "Use `Math.addExact` when overflow must be detected.",
        ),
        (
            "Relational, logical, and compound assignment",
            "`==` on primitives compares values; on references compares identity. "
            "`&&`/`||` short-circuit; `&`/`|` on booleans do not. Compound `+=` includes a cast.",
        ),
    ],
    [
        task(
            "arithmetic-safe-ops",
            "Arithmetic Safe Ops",
            "Warm-up",
            "Implement divide and remainder with clear exception behavior.",
            "ArithmeticOps",
            [
                (
                    "public static int divide(int a, int b)",
                    "return a/b; throw ArithmeticException if b==0",
                    "divides or throws",
                ),
                (
                    "public static int remainder(int a, int b)",
                    "return a%b; throw ArithmeticException if b==0",
                    "remainder or throws",
                ),
            ],
        ),
        task(
            "promotion-predictor",
            "Promotion Predictor",
            "Core",
            "Return the binary numeric promotion result type name for two operand type names.",
            "PromotionPredictor",
            [
                (
                    "public static String resultType(String left, String right)",
                    "return 'int','long','float', or 'double' per JLS binary numeric promotion for the given type names",
                    "predicts promotion type",
                )
            ],
        ),
        task(
            "overflow-detector",
            "Overflow Detector",
            "Stretch",
            "Add two ints detecting overflow using Math.addExact semantics.",
            "OverflowDetector",
            [
                (
                    "public static int addExact(int a, int b)",
                    "return sum or throw ArithmeticException on overflow (use Math.addExact or equivalent)",
                    "detects int overflow",
                )
            ],
        ),
        task(
            "compound-assignment-lab",
            "Compound Assignment Lab",
            "Challenge",
            "Apply compound assignment on a byte and return the new value (with implicit cast).",
            "CompoundAssign",
            [
                (
                    "public static byte addToByte(byte current, int delta)",
                    "return (byte)(current + delta) as compound += would",
                    "applies compound assign cast",
                )
            ],
        ),
    ],
)

day(
    4,
    "Control Flow: if, switch, Switch Expressions, Loops, and Labels",
    "Core Java",
    [
        "Write correct if/else and classic switch statements",
        "Use switch expressions and yield",
        "Master while, do-while, for, and enhanced for",
        "Use labeled break/continue intentionally",
    ],
    ["Day 03 — operators"],
    [
        (
            "if / else",
            "Conditions must be boolean. Prefer early returns over deep nesting.",
        ),
        (
            "Classic switch and switch expressions",
            "Classic switch falls through unless `break`. Switch expressions (Java 14+) are exhaustive for enums and use `->` or `yield`. "
            "Prefer expressions for mapping values.",
        ),
        (
            "Loops",
            "`while`, `do-while`, `for`, enhanced-for. Know when enhanced-for cannot modify the underlying structure safely with iterators.",
        ),
        (
            "Labels, break, continue",
            "Labels qualify which loop to break/continue. Overuse harms readability — use for nested-loop escapes.",
        ),
    ],
    [
        task(
            "grade-classifier",
            "Grade Classifier",
            "Warm-up",
            "Map a numeric score to a letter grade with if/else.",
            "GradeClassifier",
            [
                (
                    "public static char grade(int score)",
                    "A>=90 B>=80 C>=70 D>=60 else F; throw IllegalArgumentException if score not in 0..100",
                    "classifies grades",
                )
            ],
        ),
        task(
            "switch-expression-http",
            "Switch Expression HTTP",
            "Core",
            "Map HTTP status families with a switch expression.",
            "HttpStatusFamily",
            [
                (
                    "public static String family(int code)",
                    "1xx informational, 2xx success, 3xx redirect, 4xx client, 5xx server; else throw IllegalArgumentException",
                    "maps status families",
                )
            ],
        ),
        task(
            "loop-aggregators",
            "Loop Aggregators",
            "Stretch",
            "Sum and count positives using explicit loops (no streams).",
            "LoopAggregators",
            [
                (
                    "public static long sum(int[] values)",
                    "sum all values; empty array returns 0; null throws NullPointerException",
                    "sums array",
                ),
                (
                    "public static int countPositives(int[] values)",
                    "count values > 0; null throws NPE",
                    "counts positives",
                ),
            ],
        ),
        task(
            "labeled-break-search",
            "Labeled Break Search",
            "Challenge",
            "Find first pair (i,j) with i<j and a[i]+a[j]==target using labeled break.",
            "PairSearch",
            [
                (
                    "public static int[] findPair(int[] a, int target)",
                    "return int[]{i,j} of first pair or empty array if none; null input throws NPE",
                    "finds pair with labeled break",
                )
            ],
        ),
    ],
)

day(
    5,
    "Strings, String Pool, StringBuilder, Equality, and Text Blocks",
    "Core Java",
    [
        "Explain String immutability and the string pool",
        "Use common String APIs correctly",
        "Choose StringBuilder for heavy concatenation",
        "Contrast == vs equals; write text blocks",
    ],
    ["Day 04 — control flow"],
    [
        (
            "Immutability and the pool",
            "String objects are immutable. Literals may be interned in the pool. `new String(\"x\")` is a different object. "
            "`==` is identity; `equals` is content.",
        ),
        (
            "Important String methods",
            "`length`, `charAt`, `substring`, `indexOf`, `contains`, `startsWith`, `strip`, `isBlank`, `split`, `formatted` / `String.format`.",
        ),
        (
            "StringBuilder",
            "Mutable buffer for loops of concatenation. Prefer over `+=` in hot loops. Not thread-safe (use StringBuffer rarely).",
        ),
        (
            "Text blocks",
            "`\"\"\"...\"\"\"` for multi-line literals; useful for SQL/JSON samples in tests and docs.",
        ),
    ],
    [
        task(
            "string-normalize",
            "String Normalize",
            "Warm-up",
            "Normalize whitespace and case for comparisons.",
            "StringNormalize",
            [
                (
                    "public static String normalize(String input)",
                    "strip, collapse internal whitespace to single spaces, lower-case; null throws NPE",
                    "normalizes strings",
                )
            ],
        ),
        task(
            "equals-vs-identity",
            "Equals vs Identity",
            "Core",
            "Compare strings both by identity and by content.",
            "StringCompare",
            [
                (
                    "public static boolean sameReference(String a, String b)",
                    "return a == b (identity)",
                    "identity compare",
                ),
                (
                    "public static boolean sameContent(String a, String b)",
                    "return Objects.equals(a,b) content equality",
                    "content compare",
                ),
            ],
        ),
        task(
            "stringbuilder-join",
            "StringBuilder Join",
            "Stretch",
            "Join strings with a delimiter using StringBuilder (no String.join).",
            "Joiner",
            [
                (
                    "public static String join(String delimiter, String... parts)",
                    "join parts with delimiter; null delimiter or parts throws NPE; null part treated as empty string",
                    "joins with StringBuilder",
                )
            ],
        ),
        task(
            "text-block-template",
            "Text Block Template",
            "Challenge",
            "Build a multi-line message using a text block and placeholders.",
            "TextBlockTemplate",
            [
                (
                    "public static String welcome(String name, int day)",
                    "return a multi-line welcome including name and day number using a text block",
                    "formats text block welcome",
                )
            ],
        ),
    ],
)

day(
    6,
    "Arrays, Sorting, Searching, and Varargs",
    "Core Java",
    [
        "Create and traverse 1D and 2D arrays",
        "Use Arrays.sort and binarySearch correctly",
        "Write varargs methods safely",
        "Copy arrays without aliasing bugs",
    ],
    ["Day 05 — strings"],
    [
        (
            "Array creation and access",
            "Fixed length after creation. Index from 0. Out of bounds → `ArrayIndexOutOfBoundsException`.",
        ),
        (
            "Multidimensional arrays",
            "Arrays of arrays; rows can have different lengths (ragged).",
        ),
        (
            "`Arrays` utility",
            "`sort`, `binarySearch` (must be sorted), `equals`, `copyOf`, `fill`, `asList` (fixed-size).",
        ),
        (
            "Varargs",
            "`type...` is syntactic sugar for an array. Place last in parameter list. Avoid ambiguity with overloads.",
        ),
    ],
    [
        task(
            "array-stats",
            "Array Stats",
            "Warm-up",
            "Compute min, max, average for an int array.",
            "ArrayStats",
            [
                (
                    "public static int min(int[] a)",
                    "return minimum; empty or null throws IllegalArgumentException / NPE respectively",
                    "min",
                ),
                (
                    "public static int max(int[] a)",
                    "return maximum; empty/null same rules",
                    "max",
                ),
                (
                    "public static double average(int[] a)",
                    "return average as double; empty/null same rules",
                    "average",
                ),
            ],
        ),
        task(
            "matrix-sum",
            "Matrix Sum",
            "Core",
            "Sum all elements of a 2D int array (ragged OK).",
            "MatrixSum",
            [
                (
                    "public static long sum(int[][] matrix)",
                    "sum all; null matrix or null row throws NPE",
                    "sums matrix",
                )
            ],
        ),
        task(
            "sort-and-search",
            "Sort and Search",
            "Stretch",
            "Sort a copy and binary-search without mutating the original.",
            "SortSearch",
            [
                (
                    "public static int indexOfSortedCopy(int[] original, int key)",
                    "sort a copy, binarySearch, return index or -1 if not found; null original throws NPE",
                    "sort copy and search",
                )
            ],
        ),
        task(
            "varargs-max",
            "Varargs Max",
            "Challenge",
            "Return the maximum of varargs ints.",
            "VarargsMax",
            [
                (
                    "public static int max(int first, int... rest)",
                    "return max of first and rest; rest may be empty",
                    "varargs max",
                )
            ],
        ),
    ],
)

day(
    7,
    "Methods, Access Modifiers, Static Members, Pass-by-Value, Overloading",
    "Core Java",
    [
        "Design methods with clear signatures and access levels",
        "Use static vs instance members correctly",
        "Explain Java pass-by-value for primitives and references",
        "Overload methods without ambiguity",
    ],
    ["Day 06 — arrays"],
    [
        (
            "Method anatomy",
            "Modifiers, return type, name, parameters, throws clause, body. Varargs last.",
        ),
        (
            "Access modifiers",
            "`private`, package-private (default), `protected`, `public` — know who can call what across packages.",
        ),
        (
            "Static members",
            "Belong to the class. No `this`. Static init blocks run once. Static imports for constants cautiously.",
        ),
        (
            "Pass-by-value",
            "Reassigning a parameter does not affect the caller; mutating a referenced object does.",
        ),
        (
            "Overloading",
            "Same name, different parameter lists. Return type alone is not enough. Watch autoboxing ambiguities.",
        ),
    ],
    [
        task(
            "temperature-converter",
            "Temperature Converter",
            "Warm-up",
            "Static methods converting C↔F.",
            "TemperatureConverter",
            [
                (
                    "public static double celsiusToFahrenheit(double c)",
                    "return c * 9/5 + 32",
                    "C to F",
                ),
                (
                    "public static double fahrenheitToCelsius(double f)",
                    "return (f - 32) * 5/9",
                    "F to C",
                ),
            ],
        ),
        task(
            "pass-by-value-lab",
            "Pass-by-Value Lab",
            "Core",
            "Show that reassignment vs mutation differ.",
            "PassByValueLab",
            [
                (
                    "public static void reassign(int[] holder, int[] other)",
                    "reassign local parameter holder to other (caller array unchanged)",
                    "reassign has no caller effect",
                ),
                (
                    "public static void mutateFirst(int[] arr, int value)",
                    "set arr[0]=value if length>0; NPE if null",
                    "mutation visible",
                ),
            ],
        ),
        task(
            "overload-resolver",
            "Overload Resolver",
            "Stretch",
            "Provide overloaded format methods for int, double, and String.",
            "Formatter",
            [
                (
                    "public static String format(int value)",
                    "return 'INT:' + value",
                    "format int",
                ),
                (
                    "public static String format(double value)",
                    "return 'DBL:' + value",
                    "format double",
                ),
                (
                    "public static String format(String value)",
                    "return 'STR:' + value; NPE if null",
                    "format string",
                ),
            ],
        ),
        task(
            "access-boundary",
            "Access Boundary",
            "Challenge",
            "Expose only a public API while keeping helper private.",
            "PasswordMasker",
            [
                (
                    "public static String mask(String password)",
                    "return same length of '*' ; null/blank throws IllegalArgumentException; use a private helper to validate",
                    "masks password via private helper",
                )
            ],
        ),
    ],
)

day(
    8,
    "Constructors, Initialization Order, final, Immutable Classes, Records",
    "Core Java",
    [
        "Write constructors and constructor overloads",
        "Predict initialization order",
        "Apply final to fields, locals, and parameters",
        "Build immutable types and Java records",
    ],
    ["Day 07 — methods"],
    [
        (
            "Constructors",
            "No return type. Default constructor appears if none declared. `this(...)` constructor chaining.",
        ),
        (
            "Initialization order",
            "Static fields/blocks → instance fields/blocks → constructor body. Know the sequence for interviews.",
        ),
        (
            "`final`",
            "Final variables assigned once. Final fields for immutability. Final classes/methods block extension/override.",
        ),
        (
            "Immutable classes and records",
            "Private final fields, no setters, defensive copies. Records give canonical constructor, accessors, equals/hashCode/toString.",
        ),
    ],
    [
        task(
            "point-constructors",
            "Point Constructors",
            "Warm-up",
            "2D point with overloaded constructors.",
            "Point",
            [
                (
                    "public Point()",
                    "origin (0,0)",
                    "default origin",
                ),
                (
                    "public Point(int x, int y)",
                    "store x,y",
                    "stores coordinates",
                ),
                (
                    "public int x()",
                    "return x",
                    "x accessor",
                ),
                (
                    "public int y()",
                    "return y",
                    "y accessor",
                ),
            ],
        ),
        task(
            "final-budget",
            "Final Budget",
            "Core",
            "Immutable money amount using final fields.",
            "Money",
            [
                (
                    "public Money(long cents)",
                    "reject negative; store cents final",
                    "constructs money",
                ),
                (
                    "public long cents()",
                    "return cents",
                    "accessor",
                ),
                (
                    "public Money plus(Money other)",
                    "return new Money sum; NPE if other null",
                    "immutable plus",
                ),
            ],
        ),
        task(
            "immutable-list-holder",
            "Immutable List Holder",
            "Stretch",
            "Hold a defensive copy of a list.",
            "ImmutableNames",
            [
                (
                    "public ImmutableNames(java.util.List<String> names)",
                    "defensive copy; reject null list or null elements",
                    "defensive copy",
                ),
                (
                    "public java.util.List<String> names()",
                    "return unmodifiable view",
                    "unmodifiable view",
                ),
            ],
        ),
        task(
            "user-record",
            "User Record",
            "Challenge",
            "Define a record with compact canonical constructor validation.",
            "UserId",
            [
                (
                    "public UserId(String value)",
                    "record component; reject null/blank; store stripped value",
                    "validates record",
                )
            ],
        ),
    ],
)

day(
    9,
    "Inheritance, Overriding, super, and Object Methods",
    "Core Java",
    [
        "Extend classes and call super constructors",
        "Override methods with correct contracts",
        "Implement equals, hashCode, and toString",
        "Know @Override and covariant returns",
    ],
    ["Day 08 — constructors and records"],
    [
        (
            "Inheritance basics",
            "`extends` one class. Constructors chain to `super(...)`. Protected members visible to subclasses.",
        ),
        (
            "Overriding",
            "Same signature, compatible return, non-weaker access. `@Override` catches typos. `final` methods cannot be overridden.",
        ),
        (
            "Object methods",
            "`equals`/`hashCode` contract. Prefer Objects.equals/hash. `toString` for debugging.",
        ),
    ],
    [
        task(
            "animal-speak",
            "Animal Speak",
            "Warm-up",
            "Base Animal and Dog override speak.",
            "Animal",
            [
                (
                    "public String speak()",
                    "return '...' for Animal; Dog overrides to 'woof'",
                    "polymorphic speak",
                )
            ],
        ),
        task(
            "employee-hierarchy",
            "Employee Hierarchy",
            "Core",
            "Employee and Manager with salary override.",
            "Employee",
            [
                (
                    "public double pay()",
                    "Employee returns base; Manager returns base + bonus",
                    "pay hierarchy",
                )
            ],
        ),
        task(
            "equals-hashcode-book",
            "Equals HashCode Book",
            "Stretch",
            "Book equality by ISBN.",
            "Book",
            [
                (
                    "public boolean equals(Object o)",
                    "equal if same ISBN",
                    "equals by isbn",
                ),
                (
                    "public int hashCode()",
                    "hash of ISBN",
                    "hashCode",
                ),
            ],
        ),
        task(
            "toString-contract",
            "ToString Contract",
            "Challenge",
            "Readable toString including type and key fields.",
            "Account",
            [
                (
                    "public String toString()",
                    "include id and balance in a stable format specified by tests",
                    "toString format",
                )
            ],
        ),
    ],
)

day(
    10,
    "Abstract Classes, Interfaces, Polymorphism, Sealed Types, SOLID (Light)",
    "Core Java",
    [
        "Design abstract classes and interfaces",
        "Use default/static/private interface methods",
        "Apply polymorphism and safe casting",
        "Use sealed classes lightly; apply SRP/OCP/DIP intuition",
    ],
    ["Day 09 — inheritance"],
    [
        (
            "Abstract classes",
            "Cannot instantiate. May have state and constructors. Subclasses must implement abstract methods unless abstract.",
        ),
        (
            "Interfaces",
            "Contracts. Default methods enable evolution. Multiple interfaces OK. Conflict resolution rules.",
        ),
        (
            "Polymorphism and casting",
            "Reference type vs runtime type. `instanceof` pattern matching (Java 16+). ClassCastException risk.",
        ),
        (
            "Sealed classes and SOLID (light)",
            "`sealed`/`permits` for closed hierarchies. SOLID: SRP, OCP, LSP, ISP, DIP — map to DI in Spring later.",
        ),
    ],
    [
        task(
            "shape-area",
            "Shape Area",
            "Warm-up",
            "Abstract Shape with Circle/Rectangle.",
            "Shape",
            [
                (
                    "public abstract double area()",
                    "Circle pi*r*r; Rectangle w*h",
                    "shape areas",
                )
            ],
        ),
        task(
            "payment-interface",
            "Payment Interface",
            "Core",
            "PaymentMethod interface with Card and Wallet implementations.",
            "PaymentMethod",
            [
                (
                    "public boolean pay(int amountCents)",
                    "implementations succeed when funds/limit allow",
                    "pay implementations",
                )
            ],
        ),
        task(
            "instanceof-pattern",
            "Instanceof Pattern",
            "Stretch",
            "Format objects using instanceof pattern matching.",
            "Describe",
            [
                (
                    "public static String describe(Object o)",
                    "pattern-match String/Integer/null/other as specified by tests",
                    "instanceof patterns",
                )
            ],
        ),
        task(
            "sealed-result",
            "Sealed Result",
            "Challenge",
            "Sealed Result hierarchy Success/Failure.",
            "Result",
            [
                (
                    "public static Result ok(String value)",
                    "return Success",
                    "ok",
                ),
                (
                    "public static Result fail(String error)",
                    "return Failure",
                    "fail",
                ),
            ],
        ),
    ],
)

day(
    11,
    "Exceptions: Checked vs Unchecked, try-with-resources, Custom Exceptions",
    "Core Java",
    [
        "Choose checked vs unchecked appropriately",
        "Use try/catch/finally and multi-catch",
        "Use try-with-resources for AutoCloseable",
        "Create custom exception types with causes",
    ],
    ["Day 10 — interfaces"],
    [
        (
            "Exception hierarchy",
            "Throwable → Error / Exception. RuntimeException unchecked. Checked must declare or handle.",
        ),
        (
            "try / catch / finally / multi-catch",
            "Finally always runs (except JVM kill). Multi-catch with `|`. Prefer precise catches.",
        ),
        (
            "try-with-resources",
            "AutoCloseable resources closed automatically. Suppressed exceptions attached to primary.",
        ),
        (
            "Custom exceptions",
            "Extend Exception or RuntimeException. Include message and cause. Domain exceptions improve APIs.",
        ),
    ],
    [
        task(
            "parse-int-safe",
            "Parse Int Safe",
            "Warm-up",
            "Parse int returning Optional-like sentinel via exception handling.",
            "ParseIntSafe",
            [
                (
                    "public static int parseOrDefault(String s, int defaultValue)",
                    "Integer.parseInt or return default on NumberFormatException; NPE if s null",
                    "parse or default",
                )
            ],
        ),
        task(
            "multi-catch-lab",
            "Multi-Catch Lab",
            "Core",
            "Classify exceptions into categories.",
            "ExceptionClassifier",
            [
                (
                    "public static String classify(Exception e)",
                    "map NPE/IAE/other RuntimeException/checked Exception to labels per tests",
                    "classifies exceptions",
                )
            ],
        ),
        task(
            "try-with-resources-counter",
            "Try-With-Resources Counter",
            "Stretch",
            "Implement AutoCloseable that counts closes.",
            "CountingResource",
            [
                (
                    "public void close()",
                    "increment closeCount; implement AutoCloseable",
                    "close counting",
                ),
                (
                    "public int getCloseCount()",
                    "return closes",
                    "close count",
                ),
            ],
        ),
        task(
            "custom-validation-error",
            "Custom Validation Error",
            "Challenge",
            "ValidationException unchecked with field name.",
            "ValidationException",
            [
                (
                    "public ValidationException(String field, String message)",
                    "store field+message; getter for field",
                    "custom exception",
                ),
                (
                    "public static void requireEmail(String email)",
                    "throw ValidationException if null/blank or missing '@'",
                    "require email",
                ),
            ],
        ),
    ],
)

day(
    12,
    "Wrappers, Autoboxing, Enums, and Nested Classes",
    "Core Java",
    [
        "Use wrappers and understand autoboxing pitfalls (NPE, cache)",
        "Design enums with fields and methods",
        "Write static nested, inner, local, and anonymous classes",
        "Know Integer cache for -128..127",
    ],
    ["Day 11 — exceptions"],
    [
        (
            "Wrappers and autoboxing",
            "`Integer`, `Boolean`, etc. Autobox/unbox. Unboxing null → NPE. Prefer primitives in hot paths.",
        ),
        (
            "Integer cache",
            "`Integer.valueOf` caches -128..127 by default — `==` may accidentally work; still use `equals`.",
        ),
        (
            "Enums",
            "Type-safe constants. Can have fields, methods, abstract methods per constant.",
        ),
        (
            "Nested classes",
            "Static nested, inner (has outer this), local, anonymous. Prefer static nested when no outer instance needed.",
        ),
    ],
    [
        task(
            "autobox-safe-sum",
            "Autobox Safe Sum",
            "Warm-up",
            "Sum Integer list treating null elements as 0.",
            "SafeSum",
            [
                (
                    "public static int sum(java.util.List<Integer> values)",
                    "sum with null elements as 0; null list throws NPE",
                    "safe sum",
                )
            ],
        ),
        task(
            "order-status-enum",
            "Order Status Enum",
            "Core",
            "Enum with transition rules.",
            "OrderStatus",
            [
                (
                    "public boolean canTransitionTo(OrderStatus next)",
                    "NEW→PAID/CANCELLED; PAID→SHIPPED/CANCELLED; SHIPPED→DELIVERED; others false",
                    "enum transitions",
                )
            ],
        ),
        task(
            "nested-counter",
            "Nested Counter",
            "Stretch",
            "Outer class with static nested Builder-like counter factory.",
            "CounterFactory",
            [
                (
                    "public static Counter newCounter(int start)",
                    "return nested Counter starting at start",
                    "nested counter",
                )
            ],
        ),
        task(
            "anonymous-comparator",
            "Anonymous Comparator",
            "Challenge",
            "Sort strings by length then alpha using anonymous Comparator (no lambdas yet required — but lambdas OK).",
            "LengthThenAlpha",
            [
                (
                    "public static java.util.Comparator<String> comparator()",
                    "length asc then natural order",
                    "comparator",
                )
            ],
        ),
    ],
)


def pad(n: int) -> str:
    return f"{n:02d}"


def pom_xml(day_num: int, task_num: int, artifact: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.javaprep.day{pad(day_num)}</groupId>
  <artifactId>{artifact}</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <name>Day {pad(day_num)} — {artifact}</name>
  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <maven.compiler.release>21</maven.compiler.release>
    <junit.version>5.11.4</junit.version>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>${{junit.version}}</version>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.assertj</groupId>
      <artifactId>assertj-core</artifactId>
      <version>3.27.3</version>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.13.0</version>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.5.2</version>
      </plugin>
    </plugins>
  </build>
</project>
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def generate_theory(d: dict) -> str:
    xx = pad(d["num"])
    parts = [
        f"# Day {xx} — {d['title']}",
        "",
        f"**Phase:** {d['phase']}  ",
        f"**Day:** {xx}  ",
        f"**Verify tasks with:** `mvn test`",
        "",
        "## Overview",
        "",
        f"This day focuses on **{d['title']}**. Read each section, try the self-test questions, then complete the practical tasks in order.",
        "",
        "## Day roadmap",
        "",
    ]
    for i, (heading, _) in enumerate(d["theory"], 1):
        parts.append(f"{i}. {heading}")
    parts.append("")
    for heading, body in d["theory"]:
        parts.append(f"## {heading}")
        parts.append("")
        parts.append(body)
        parts.append("")
        parts.append("### Quick checks (self-test)")
        parts.append("")
        parts.append(f"1. In your own words, what is the main idea of **{heading}**?")
        parts.append("2. What bug appears if you misuse this concept?")
        parts.append("")
    parts.append("## Common mistakes & debugging")
    parts.append("")
    parts.append("- Reading theory without running `mvn test` on the warm-up task first.")
    parts.append("- Mixing up compile-time types with runtime behavior.")
    parts.append("- Ignoring exception messages from failing tests.")
    parts.append("")
    parts.append("## Interview angles")
    parts.append("")
    for q in d["interview"] or [
        f"Explain the key idea behind {d['title']}.",
        "What production bug have you seen (or can imagine) related to today's topic?",
    ]:
        parts.append(f"- {q}")
    parts.append("")
    parts.append("## Further reading")
    parts.append("")
    parts.append("- Oracle Java Tutorials (matching topic)")
    parts.append("- Java Language Specification sections referenced in interviews")
    if d["num"] <= 12:
        parts.append("- OCA Java SE 8 Programmer I Study Guide — overlapping chapters (update mentally to Java 21 where APIs differ)")
    parts.append("")
    parts.append("## Glossary")
    parts.append("")
    parts.append("| Term | Meaning |")
    parts.append("|------|---------|")
    parts.append(f"| Day {xx} focus | {d['title']} |")
    parts.append("| `mvn test` | Compile + run JUnit 5 tests |")
    parts.append("")
    parts.append("## Answers (self-test)")
    parts.append("")
    parts.append("Compare your answers against the theory sections above. Re-read any section you could not explain out loud in 60 seconds.")
    parts.append("")
    return "\n".join(parts)


def generate_day_readme(d: dict) -> str:
    xx = pad(d["num"])
    lines = [
        f"# Day {xx} — {d['title']}",
        "",
        "## Learning objectives",
        "",
    ]
    for o in d["objectives"]:
        lines.append(f"- {o}")
    lines += ["", "## Prerequisites", ""]
    for p in d["prereqs"]:
        lines.append(f"- {p}")
    lines += [
        "",
        "## How to use this folder",
        "",
        f"1. Read [`DAY-{xx}-THEORY-AND-REFERENCE.md`](DAY-{xx}-THEORY-AND-REFERENCE.md).",
        "2. Complete `practical-tasks/` in order (task-01 → task-04).",
        "3. In each task folder run `mvn test` (expected **RED** until you implement the TODOs).",
        "",
        "## Task list",
        "",
        "| Order | Folder | Type | Verify with |",
        "|------:|--------|------|-------------|",
    ]
    for i, t in enumerate(d["tasks"], 1):
        lines.append(
            f"| {i} | `task-{pad(i)}-{t['slug']}` | Java / JUnit | `mvn test` |"
        )
    lines.append("")
    return "\n".join(lines)


def java_type_for_class(class_name: str, methods: list, day_num: int, task_num: int, extra: str = "") -> str:
    xx, yy = pad(day_num), pad(task_num)
    pkg = f"com.javaprep.day{xx}.task{yy}"
    body = []
    # Special-case a few class-shaped tasks with multiple constructors — keep simple static/instance stubs
    is_likely_instance = any(
        m[0].startswith("public ") and "static" not in m[0].split("(")[0]
        for m in methods
    )
    # Always generate a simple class with stub methods
    for sig, todo, _ in methods:
        clean_sig = sig.strip()
        if clean_sig.endswith("{"):
            clean_sig = clean_sig[:-1].strip()
        # constructor?
        if clean_sig.startswith("public " + class_name) or clean_sig.startswith(f"public {class_name}"):
            body.append(f"    // TODO(Day{xx}-task{yy}): {todo}")
            body.append(f"    {clean_sig} {{")
            body.append(f"        throw new UnsupportedOperationException(\"TODO(Day{xx}-task{yy}): implement {class_name} constructor\");")
            body.append("    }")
            body.append("")
            continue
        # abstract method in interface/abstract — still stub in concrete helper class for tests
        ret = "Object"
        name = "method"
        if "(" in clean_sig:
            before = clean_sig.split("(")[0].strip().split()
            name = before[-1]
            if len(before) >= 2:
                ret = before[-2]
        body.append(f"    // TODO(Day{xx}-task{yy}): {todo}")
        body.append(f"    {clean_sig} {{")
        body.append(f"        throw new UnsupportedOperationException(\"TODO(Day{xx}-task{yy}): implement {name}\");")
        body.append("    }")
        body.append("")
    return f"""package {pkg};

/**
 * Day {xx} Task {yy} — implement the TODOs. Run {{@code mvn test}}.
 */
public class {class_name} {{
{chr(10).join(body)}
}}
"""


def java_test(class_name: str, methods: list, day_num: int, task_num: int) -> str:
    """Fallback test generator for tasks WITHOUT a curated spec in scripts/curated/.

    Tests are RED while the stub throws UnsupportedOperationException and never *assert* that exception:
    each probe fails if the call throws UnsupportedOperationException (the TODO stub). Real behavioral
    assertions for Day 01-12 live in scripts/curated/dayXX/taskYY/ and are copied over by generate_day().
    """
    xx, yy = pad(day_num), pad(task_num)
    pkg = f"com.javaprep.day{xx}.task{yy}"
    tests = []
    for i, (sig, todo, desc) in enumerate(methods, 1):
        head = sig.split("(")[0].strip().split()
        mname = head[-1] if head else "method"
        args_part = sig[sig.find("(") + 1 : sig.rfind(")")] if "(" in sig else ""
        if "static" in head:
            call = f"{class_name}.{mname}({stub_args(args_part)})"
            tests.append(
                f"""
    @Test
    @DisplayName("{desc.replace(chr(34), chr(39))}")
    void {mname}_{i}_isImplemented() {{
        Throwable thrown = catchThrowable(() -> {call});
        assertThat(thrown)
                .as("{class_name}.{mname} must be implemented (still the TODO stub)")
                .isNotInstanceOf(UnsupportedOperationException.class);
        // TODO: add real return-value / edge-case assertions for: {todo.replace(chr(34), chr(39))}
    }}"""
            )
        else:
            tests.append(
                f"""
    @Test
    @DisplayName("{desc.replace(chr(34), chr(39))}")
    void {mname}_{i}_needsBehavioralTest() {{
        fail("No curated behavioral test for {class_name}: {mname}. Add one under scripts/curated/day{xx}/task{yy}.");
    }}"""
            )
    return f"""package {pkg};

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.catchThrowable;
import static org.assertj.core.api.Assertions.fail;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * Generated fallback: RED while stubs throw UnsupportedOperationException. Never asserts that exception.
 */
class {class_name}Test {{
{"".join(tests)}
}}
"""


def stub_args(args_part: str) -> str:
    if not args_part.strip():
        return ""
    parts = []
    # naive split on comma not inside <>
    depth = 0
    current = []
    for ch in args_part:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        elif ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    if current:
        parts.append("".join(current).strip())
    vals = []
    for p in parts:
        if not p:
            continue
        tokens = p.replace("...", " ").split()
        typ = tokens[0] if tokens else "Object"
        if typ.startswith("String"):
            vals.append('"x"')
        elif typ in ("int", "long", "short", "byte"):
            vals.append("1")
        elif typ in ("double", "float"):
            vals.append("1.0")
        elif typ == "boolean":
            vals.append("true")
        elif typ == "char":
            vals.append("'a'")
        elif "String[]" in p or typ.endswith("[]"):
            vals.append("new int[]{1,2,3}" if "int" in p else "new String[]{\"a\"}")
        elif "List" in typ:
            vals.append("java.util.List.of()")
        elif "Map" in typ:
            vals.append("java.util.Map.of()")
        elif "Object" in typ:
            vals.append('"x"')
        else:
            vals.append("null")
    return ", ".join(vals)


def task_instructions(d: dict, t: dict, task_num: int) -> str:
    xx, yy = pad(d["num"]), pad(task_num)
    methods_rows = "\n".join(
        f"| `{t['class_name']}` / `{m[0].split('(')[0].strip().split()[-1]}` | `TODO(Day{xx}-task{yy})` | {m[1]} |"
        for m in t["methods"]
    )
    return f"""# Task {task_num} — {t['title']}

**Day:** {xx} · **Task ID:** Day{xx}-task{yy} · **Type:** Plain Java · **Difficulty:** {t['difficulty']}

## Summary

{t['summary']}

## Learning goals

- Practice today's theory with a focused, testable API
- Drive implementation with failing JUnit tests (`mvn test`)
- Replace `UnsupportedOperationException` stubs with correct behavior

## Provided files

| Path | Purpose |
|------|---------|
| `pom.xml` | Maven project (Java 21, JUnit 5, AssertJ) |
| `src/main/java/.../{t['class_name']}.java` | Stubs with TODOs |
| `src/test/java/.../{t['class_name']}Test.java` | Failing tests |

## Prerequisites

- Day {xx} theory read
- JDK 21 + Maven available on PATH

## What you will implement

1. Implement every method marked `TODO(Day{xx}-task{yy})` in `{t['class_name']}`.
2. Satisfy edge cases listed below and in tests.
3. Make `mvn test` green.

## Constraints

- Java 21; no Spring on this task unless the day is Spring-focused
- Do not change test method names unless a test is clearly wrong (prefer fixing your code)
- No Lombok
- Do not return dummy values that accidentally pass — implement real logic

## Step-by-step guidance

1. Run `mvn test` and confirm failures mention `TODO(Day{xx}-task{yy})`.
2. Implement methods one at a time.
3. Re-run `mvn test` until green.
4. Commit: `Day {xx}: complete task-{yy}-{t['slug']}`.

## How to run and verify

### Prerequisites check

`java -version` (21) · `mvn -v` (3.9+)

### Run all tests (expected RED at start)

```bash
mvn test
```

### Run one test class

```bash
mvn -Dtest={t['class_name']}Test test
```

### Manual checks

- [ ] No `TODO(Day{xx}-task{yy})` left in executable paths (comments OK only if behavior is done)
- [ ] Edge cases covered

## `TODO` map

| Location | TODO tag | "Done" means |
|----------|----------|--------------|
{methods_rows}

## Test map

| Requirement # | Test method(s) |
|--------------:|----------------|
| 1+ | `{t['class_name']}Test` methods |

## Edge cases to handle

- Null / illegal arguments as described in each method TODO
- Empty collections/arrays where relevant

## Submission checklist (Git)

- [ ] `mvn test` is green
- [ ] Only intentional files changed (no `target/`)
- [ ] No secrets committed
- [ ] Commit message: `Day {xx}: {t['title']}`

## Hints (optional)

<details><summary>Hint 1</summary>
Read the theory section that matches this task before coding.
</details>
"""


def evaluation_criteria(d: dict, t: dict, task_num: int) -> str:
    xx, yy = pad(d["num"]), pad(task_num)
    return f"""# Evaluation Criteria — Day {xx} — Task {yy} — {t['title']}

## Scope

Automated JUnit verification plus light code-quality review for Day {xx} Task {yy}.

## Weighting (100 points)

| Category | Points |
|----------|-------:|
| Correctness (tests + edge cases) | 70 |
| API / exception contracts | 15 |
| Code clarity (naming, simplicity) | 10 |
| Git / hygiene (no target/, no secrets) | 5 |

## Pass / fail gates (automatic fail if violated)

- Code does not compile
- `mvn test` fails
- Secrets or `target/` committed
- Lombok or forbidden APIs used when constraints forbid them

## Detailed rubric

### Correctness

- All required behaviors implemented
- Edge cases match TODOs

### Edge cases

- Null / illegal inputs handled as specified

### Security / privacy (if applicable)

- N/A unless task involves secrets or SQL

### UX / accessibility (if applicable)

- N/A (backend / library task)

## Evidence the grader should collect

- `mvn test` console output
- Diff of `{t['class_name']}.java`

## AI grading prompt (paste into your grader)

```
You are grading Day {xx} Task {yy} ({t['title']}) for a graduate Java backend course.
Use only observable evidence. Run or trust mvn test results.
Score /100 using the rubric weights. List blocking issues first.
Leftover TODO comments are OK if behavior is implemented and tests pass.
```
"""


def apply_curated(day_num: int, task_num: int, task_dir: Path) -> None:
    """Overlay hand-written, behavior-asserting sources (main stubs + tests) from scripts/curated/.

    Layout: scripts/curated/dayXX/taskYY/src/{main,test}/java/... . When present, the generic generated
    main/test .java files for that task are replaced so APIs are well-shaped and tests assert real behavior.
    """
    src = ROOT / "scripts" / "curated" / f"day{pad(day_num)}" / f"task{pad(task_num)}" / "src"
    if not src.is_dir():
        return
    for kind in ("main", "test"):
        for old in (task_dir / "src" / kind / "java").rglob("*.java"):
            old.unlink()
    for f in src.rglob("*.java"):
        write(task_dir / "src" / f.relative_to(src), f.read_text())


def generate_day(d: dict) -> None:
    xx = pad(d["num"])
    day_dir = ROOT / f"Day {xx}"
    write(day_dir / "README.md", generate_day_readme(d))
    write(day_dir / f"DAY-{xx}-THEORY-AND-REFERENCE.md", generate_theory(d))
    for i, t in enumerate(d["tasks"], 1):
        yy = pad(i)
        task_dir = day_dir / "practical-tasks" / f"task-{yy}-{t['slug']}"
        write(task_dir / "pom.xml", pom_xml(d["num"], i, f"task-{yy}-{t['slug']}"))
        write(task_dir / "TASK_INSTRUCTIONS.md", task_instructions(d, t, i))
        write(task_dir / "EVALUATION_CRITERIA.md", evaluation_criteria(d, t, i))
        pkg_path = f"com/javaprep/day{xx}/task{yy}"
        write(
            task_dir / "src/main/java" / pkg_path / f"{t['class_name']}.java",
            java_type_for_class(t["class_name"], t["methods"], d["num"], i),
        )
        write(
            task_dir / "src/test/java" / pkg_path / f"{t['class_name']}Test.java",
            java_test(t["class_name"], t["methods"], d["num"], i),
        )
        apply_curated(d["num"], i, task_dir)


def main() -> None:
    # Only days defined in this file (01-12). Later batches append more day() calls or separate modules.
    for d in DAYS:
        generate_day(d)
        print(f"Generated Day {pad(d['num'])} — {d['title']}")
    print(f"Total days generated: {len(DAYS)}")


if __name__ == "__main__":
    main()
