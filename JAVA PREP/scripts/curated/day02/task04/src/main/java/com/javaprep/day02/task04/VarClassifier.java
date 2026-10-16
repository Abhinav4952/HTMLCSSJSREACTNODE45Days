package com.javaprep.day02.task04;

public class VarClassifier {

    /**
     * Classifies a simplified local-variable declaration snippet.
     * <ul>
     *   <li>{@code "VALID"}: {@code var name = <initializer>;} where the initializer is not null, an
     *       array initializer {@code {..}}, a lambda ({@code ->}) or a method reference ({@code ::}).</li>
     *   <li>{@code "NEEDS_EXPLICIT"}: a {@code var} declaration that cannot infer a type: no initializer,
     *       {@code = null}, array initializer, lambda, or method reference.</li>
     *   <li>{@code "INVALID"}: anything that is not a well-formed {@code var} declaration
     *       (null/blank, no variable name, not starting with {@code var}).</li>
     * </ul>
     */
    // TODO(Day02-task04): implement per Javadoc
    public static String classify(String declaration) {
        throw new UnsupportedOperationException("TODO(Day02-task04): implement classify");
    }
}
