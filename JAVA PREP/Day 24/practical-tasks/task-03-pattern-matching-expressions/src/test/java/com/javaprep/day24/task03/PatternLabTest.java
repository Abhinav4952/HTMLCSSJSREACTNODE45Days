package com.javaprep.day24.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.javaprep.day24.task03.Expr.Add;
import com.javaprep.day24.task03.Expr.Mul;
import com.javaprep.day24.task03.Expr.Neg;
import com.javaprep.day24.task03.Expr.Num;
import com.javaprep.day24.task03.Expr.Var;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

class PatternLabTest {

    private static Num n(int v) {
        return new Num(v);
    }

    private static Var v(String name) {
        return new Var(name);
    }

    // ------------------------------------------------------------------ r1 eval
    @Test
    void r1_evaluatesNestedExpressions() {
        Expr e = new Add(n(2), new Mul(v("x"), n(3)));        // 2 + x * 3
        assertThat(PatternLab.eval(e, Map.of("x", 4))).isEqualTo(14);
        assertThat(PatternLab.eval(new Neg(e), Map.of("x", 4))).isEqualTo(-14);
        assertThat(PatternLab.eval(new Neg(new Neg(n(5))), Map.of())).isEqualTo(5);
        assertThat(PatternLab.eval(n(-9), Map.of())).isEqualTo(-9);
    }

    @Test
    void r1_usesTheEnvironmentForEveryVariable() {
        Expr e = new Add(v("a"), new Mul(v("b"), v("a")));
        assertThat(PatternLab.eval(e, Map.of("a", 2, "b", 5))).isEqualTo(12);
        assertThat(PatternLab.eval(e, Map.of("a", 1, "b", 1))).isEqualTo(2);
    }

    @Test
    void r1_unboundVariableIsReported() {
        assertThatThrownBy(() -> PatternLab.eval(new Add(n(1), v("y")), Map.of("x", 1)))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessage("unbound variable: y");
    }

    // ------------------------------------------------------------------ r2 show
    @Test
    void r2_rendersInfixWithParentheses() {
        assertThat(PatternLab.show(n(3))).isEqualTo("3");
        assertThat(PatternLab.show(v("x"))).isEqualTo("x");
        assertThat(PatternLab.show(new Add(n(1), n(2)))).isEqualTo("(1 + 2)");
        assertThat(PatternLab.show(new Mul(new Add(n(1), v("x")), n(3)))).isEqualTo("((1 + x) * 3)");
    }

    @Test
    void r2_negativeNumbersAndNegation() {
        assertThat(PatternLab.show(n(-3))).isEqualTo("(-3)");
        assertThat(PatternLab.show(new Neg(v("x")))).isEqualTo("-x");
        assertThat(PatternLab.show(new Neg(new Add(v("x"), n(-1))))).isEqualTo("-(x + (-1))");
        assertThat(PatternLab.show(new Neg(new Neg(n(2))))).isEqualTo("--2");
    }

    // ------------------------------------------------------------------ r3 simplify
    @Test
    void r3_constantFolding() {
        assertThat(PatternLab.simplify(new Add(n(2), n(3)))).isEqualTo(n(5));
        assertThat(PatternLab.simplify(new Mul(n(4), n(5)))).isEqualTo(n(20));
        assertThat(PatternLab.simplify(new Add(new Mul(n(2), n(3)), new Neg(n(1))))).isEqualTo(n(5));
    }

    @Test
    void r3_identities() {
        assertThat(PatternLab.simplify(new Add(n(0), v("x")))).isEqualTo(v("x"));
        assertThat(PatternLab.simplify(new Add(v("x"), n(0)))).isEqualTo(v("x"));
        assertThat(PatternLab.simplify(new Mul(n(1), v("y")))).isEqualTo(v("y"));
        assertThat(PatternLab.simplify(new Mul(v("y"), n(1)))).isEqualTo(v("y"));
        assertThat(PatternLab.simplify(new Mul(n(0), v("x")))).isEqualTo(n(0));
        assertThat(PatternLab.simplify(new Mul(v("x"), n(0)))).isEqualTo(n(0));
    }

    @Test
    void r3_negation() {
        assertThat(PatternLab.simplify(new Neg(n(5)))).isEqualTo(n(-5));
        assertThat(PatternLab.simplify(new Neg(new Neg(v("x"))))).isEqualTo(v("x"));
        assertThat(PatternLab.simplify(new Neg(new Neg(new Neg(v("x")))))).isEqualTo(new Neg(v("x")));
        assertThat(PatternLab.simplify(new Neg(new Add(n(1), n(-1))))).isEqualTo(n(0));
    }

    @Test
    void r3_rulesCascadeBottomUp() {
        // (1 * x) + (0 * y)  ->  x + 0  ->  x
        Expr e = new Add(new Mul(n(1), v("x")), new Mul(n(0), v("y")));
        assertThat(PatternLab.simplify(e)).isEqualTo(v("x"));
        // 2 * ((3 + -3) + x)  ->  2 * x
        Expr f = new Mul(n(2), new Add(new Add(n(3), n(-3)), v("x")));
        assertThat(PatternLab.simplify(f)).isEqualTo(new Mul(n(2), v("x")));
    }

    @Test
    void r3_unsimplifiableTreesAreRebuiltEqual() {
        Expr e = new Add(v("a"), new Mul(v("b"), v("c")));
        assertThat(PatternLab.simplify(e)).isEqualTo(e);
        assertThat(PatternLab.simplify(v("z"))).isEqualTo(v("z"));
    }

    @Test
    void r3_simplifyPreservesTheValue() {
        Expr e = new Add(new Mul(n(1), new Add(v("x"), n(0))), new Neg(new Neg(new Mul(v("y"), n(3)))));
        Map<String, Integer> env = Map.of("x", 7, "y", -2);
        assertThat(PatternLab.eval(PatternLab.simplify(e), env)).isEqualTo(PatternLab.eval(e, env));
        assertThat(PatternLab.simplify(e)).isEqualTo(new Add(v("x"), new Mul(v("y"), n(3))));
    }

    // ------------------------------------------------------------------ r4 variables
    @Test
    void r4_collectsSortedVariableNames() {
        Expr e = new Add(new Mul(v("zeta"), v("alpha")), new Neg(new Add(v("beta"), new Add(n(1), v("alpha")))));
        assertThat(PatternLab.variables(e)).containsExactly("alpha", "beta", "zeta");
        assertThat(PatternLab.variables(new Add(n(1), n(2)))).isEmpty();
    }

    // ------------------------------------------------------------------ r5 describe
    @Test
    void r5_describesNullAndNumbers() {
        assertThat(PatternLab.describe(null)).isEqualTo("null");
        assertThat(PatternLab.describe(-5)).isEqualTo("negative int -5");
        assertThat(PatternLab.describe(0)).isEqualTo("int 0");
        assertThat(PatternLab.describe(42)).isEqualTo("int 42");
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "\t\n"})
    void r5_blankStrings(String s) {
        assertThat(PatternLab.describe(s)).isEqualTo("blank string");
    }

    @Test
    void r5_stringsArraysAndLists() {
        assertThat(PatternLab.describe("hello")).isEqualTo("string of length 5");
        assertThat(PatternLab.describe(new int[] {1, 2, 3})).isEqualTo("int array of 3");
        assertThat(PatternLab.describe(new int[0])).isEqualTo("int array of 0");
        assertThat(PatternLab.describe(List.of())).isEqualTo("empty list");
        assertThat(PatternLab.describe(new ArrayList<>())).isEqualTo("empty list");
        assertThat(PatternLab.describe(List.of(1, 2))).isEqualTo("list of 2");
    }

    @Test
    void r5_expressionsAndOtherTypes() {
        assertThat(PatternLab.describe(new Add(n(1), v("x")))).isEqualTo("expression (1 + x)");
        assertThat(PatternLab.describe(3.5)).isEqualTo("other: Double");
        assertThat(PatternLab.describe(new StringBuilder("x"))).isEqualTo("other: StringBuilder");
        assertThat(PatternLab.describe(new long[] {1})).isEqualTo("other: long[]");
    }
}
