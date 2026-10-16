package com.javaprep.day24.task03;

import com.javaprep.day24.task03.Expr.Add;
import com.javaprep.day24.task03.Expr.Mul;
import com.javaprep.day24.task03.Expr.Neg;
import com.javaprep.day24.task03.Expr.Num;
import com.javaprep.day24.task03.Expr.Var;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/** Pattern matching exercises. */
public final class PatternLab {

    private PatternLab() {
    }

    public static int eval(Expr expr, Map<String, Integer> env) {
        // TODO(Day24-task03): exhaustive switch (no default) with record patterns: Num -> value; Var -> env lookup or IllegalArgumentException('unbound variable: <name>'); Add -> sum; Mul -> product; Neg -> negation
        throw new UnsupportedOperationException("TODO(Day24-task03): eval");
    }

    public static String show(Expr expr) {
        // TODO(Day24-task03): Num with a guard (negative -> '(-3)'), Num -> digits, Var -> name, Add -> '(l + r)', Mul -> '(l * r)', Neg -> '-' + show(inner)
        throw new UnsupportedOperationException("TODO(Day24-task03): show");
    }

    public static Expr simplify(Expr expr) {
        // TODO(Day24-task03): bottom-up: simplify the children first, then apply: Add/Mul of two Num folds; 0+x=x, x+0=x, 1*x=x, x*1=x, 0*x=0, x*0=0; Neg(Num n)=Num(-n); Neg(Neg x)=x; otherwise rebuild the node
        throw new UnsupportedOperationException("TODO(Day24-task03): simplify");
    }

    public static Set<String> variables(Expr expr) {
        // TODO(Day24-task03): collect Var names recursively into a TreeSet (sorted)
        throw new UnsupportedOperationException("TODO(Day24-task03): variables");
    }

    public static String describe(Object value) {
        // TODO(Day24-task03): switch with patterns in this order: null, negative Integer (guard), Integer, blank String (guard), String, int[], empty List (guard), List, Expr (use show), default 'other: ' + simple class name
        throw new UnsupportedOperationException("TODO(Day24-task03): describe");
    }

    private static boolean isNum(Expr expr, int expected) {
        return expr instanceof Num(int value) && value == expected;
    }

    private static void collect(Expr expr, Set<String> names) {
        switch (expr) {
            case Var(String name) -> names.add(name);
            case Num n -> { }
            case Add(Expr left, Expr right) -> {
                collect(left, names);
                collect(right, names);
            }
            case Mul(Expr left, Expr right) -> {
                collect(left, names);
                collect(right, names);
            }
            case Neg(Expr inner) -> collect(inner, names);
        }
    }
}
