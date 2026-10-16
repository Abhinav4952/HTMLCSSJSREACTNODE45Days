package com.javaprep.day44.task03;

/** Like Gateway's RewritePath: regex replace on the path, e.g. "/old/(?<rest>.*)" -> "/new/${rest}". */
public class RewritePathFilter implements GatewayFilter {

    private final String regex;
    private final String replacement;

    public RewritePathFilter(String regex, String replacement) {
        this.regex = regex;
        this.replacement = replacement;
    }

    @Override
    public GatewayResponse filter(GatewayRequest request, Handler next) {
        // TODO(Day44-task03): apply String.replaceAll(regex, replacement) to the path and continue
        throw new UnsupportedOperationException("TODO(Day44-task03): implement RewritePathFilter");
    }
}
