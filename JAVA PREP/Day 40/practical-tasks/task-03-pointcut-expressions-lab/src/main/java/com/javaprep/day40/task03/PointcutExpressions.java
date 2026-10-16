package com.javaprep.day40.task03;

/**
 * AspectJ pointcut expressions (as Strings) for the sample classes in com.javaprep.day40.task03.sample:
 *   UserService:      find(long), save(String) [@Audited], count()
 *   OrderService:     place(String, int), cancel(long)
 *   web.UserController: get(long), save(String)
 */
public final class PointcutExpressions {

    private PointcutExpressions() {
    }

    /** every method of every class whose simple name ends with "Service" in package com.javaprep.day40.task03.sample (not sub-packages) */
    public static String allInServices() {
        // TODO(Day40-task03): execution(...) with a *Service type pattern
        throw new UnsupportedOperationException("TODO(Day40-task03): execution(...) with a *Service type pattern");
    }

    /** every method named save that takes exactly one String parameter, in any class of any package */
    public static String saveWithString() {
        // TODO(Day40-task03): execution with any declaring type
        throw new UnsupportedOperationException("TODO(Day40-task03): execution with any declaring type");
    }

    /** every method with exactly two parameters of any type */
    public static String twoArguments() {
        // TODO(Day40-task03): execution with (*, *)
        throw new UnsupportedOperationException("TODO(Day40-task03): execution with (*, *)");
    }

    /** every method of classes in com.javaprep.day40.task03.sample.web and its sub-packages (use within) */
    public static String webLayer() {
        // TODO(Day40-task03): within(...) with a .. pattern
        throw new UnsupportedOperationException("TODO(Day40-task03): within(...) with a .. pattern");
    }

    /** every method carrying the @Audited annotation */
    public static String audited() {
        // TODO(Day40-task03): @annotation(...)
        throw new UnsupportedOperationException("TODO(Day40-task03): @annotation(...)");
    }

    /** everything in com.javaprep.day40.task03.sample (all sub-packages) EXCEPT the web layer: combine execution(...) && !within(...) */
    public static String serviceLayerOnly() {
        // TODO(Day40-task03): boolean combination
        throw new UnsupportedOperationException("TODO(Day40-task03): boolean combination");
    }
}
