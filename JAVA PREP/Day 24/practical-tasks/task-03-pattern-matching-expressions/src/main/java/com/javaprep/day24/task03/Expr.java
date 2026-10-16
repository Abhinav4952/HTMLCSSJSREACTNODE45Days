package com.javaprep.day24.task03;

/** Provided: a closed expression language. */
public sealed interface Expr permits Expr.Num, Expr.Var, Expr.Add, Expr.Mul, Expr.Neg {

    record Num(int value) implements Expr {
    }

    record Var(String name) implements Expr {
    }

    record Add(Expr left, Expr right) implements Expr {
    }

    record Mul(Expr left, Expr right) implements Expr {
    }

    record Neg(Expr inner) implements Expr {
    }
}
