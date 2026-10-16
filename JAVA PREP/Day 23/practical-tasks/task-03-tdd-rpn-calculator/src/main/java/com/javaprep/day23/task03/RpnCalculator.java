package com.javaprep.day23.task03;

/** Postfix calculator built on {@link BoundedStack}. */
public final class RpnCalculator {

    private final int maxDepth;

    public RpnCalculator(int maxDepth) {
        this.maxDepth = maxDepth;
    }

    public long evaluate(String expression) {
        // TODO(Day23-task03): null/blank -> IAE('empty expression'); split on whitespace; numbers (parse long) are pushed on a BoundedStack(maxDepth); + - * / pop right then left, apply (multiplyExact; '/' by zero -> ArithmeticException('division by zero')), push; too few operands -> IAE('not enough operands'); unknown token -> IAE('unknown token: x'); at the end exactly one value must remain else IAE('too many operands')
        throw new UnsupportedOperationException("TODO(Day23-task03): evaluate");
    }

    private static long parse(String token) {
        try {
            return Long.parseLong(token);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("unknown token: " + token);
        }
    }

    private static long apply(String operator, long left, long right) {
        return switch (operator) {
            case "+" -> Math.addExact(left, right);
            case "-" -> Math.subtractExact(left, right);
            case "*" -> Math.multiplyExact(left, right);
            case "/" -> {
                if (right == 0) {
                    throw new ArithmeticException("division by zero");
                }
                yield left / right;
            }
            default -> throw new IllegalArgumentException("unknown token: " + operator);
        };
    }
}
