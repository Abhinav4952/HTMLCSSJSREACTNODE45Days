package com.javaprep.day49.task03;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;

class StyleLinterTest {

    private final StyleLinter linter = new StyleLinter();

    @Test
    void cleanSourceHasNoViolations() {
        assertThat(linter.lint("package a;\n\nclass A {\n}\n")).isEmpty();
    }

    @Test
    void emptySourceHasNoViolations() {
        assertThat(linter.lint("")).isEmpty();
    }

    @Test
    void tabsAndTrailingWhitespaceAreFound() {
        String src = "class A {\n\tint x;\n    int y; \n}\n";
        assertThat(linter.lint(src)).containsExactly("2:TAB", "3:TRAILING_WHITESPACE");
    }

    @Test
    void longLinesAreFound() {
        String src = "// " + "x".repeat(98) + "\n// " + "x".repeat(97) + "\n";
        assertThat(linter.lint(src)).containsExactly("1:LINE_TOO_LONG");
    }

    @Test
    void starImportsAndConsolePrintsAreFound() {
        String src = "import java.util.*;\nimport java.io.File;\nclass A { void m() { System.out.println(1); } }\n";
        assertThat(linter.lint(src)).containsExactly("1:STAR_IMPORT", "3:SYSTEM_OUT");
    }

    @Test
    void oneLineCanHaveSeveralRulesInOrder() {
        String src = "\tSystem.out.println(\"x\"); \n";
        assertThat(linter.lint(src)).containsExactly("1:TAB", "1:TRAILING_WHITESPACE", "1:SYSTEM_OUT");
    }

    @Test
    void missingFinalNewlineIsReportedLast() {
        assertThat(linter.lint("class A {\n\tint x;\n}")).containsExactly("2:TAB", "EOF:NO_FINAL_NEWLINE");
    }
}
