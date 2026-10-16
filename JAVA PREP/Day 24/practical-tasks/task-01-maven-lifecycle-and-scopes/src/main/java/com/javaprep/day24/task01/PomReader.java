package com.javaprep.day24.task01;

import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;

/** Reads dependencies from a POM and applies scope rules. */
public final class PomReader {

    /** Which classpath is being computed. */
    public enum ClasspathKind { COMPILE, RUNTIME, TEST }

    /** A direct dependency as declared in the POM. */
    public record Dependency(String groupId, String artifactId, String version, String scope) {
        public String coordinates() {
            return groupId + ":" + artifactId + ":" + version;
        }
    }

    private static final Pattern PLACEHOLDER = Pattern.compile("\\$\\{([^}]+)}");

    private PomReader() {
    }

    public static List<Dependency> dependencies(String pomXml) {
        // TODO(Day24-task01): parse with a DocumentBuilderFactory that disallows DOCTYPE (feature http://apache.org/xml/features/disallow-doctype-decl) and wrap parser errors in IllegalArgumentException; collect <properties> children plus project.version; read ONLY project/dependencies/dependency (direct children) with groupId, artifactId, version (resolve ${...} via properties, unresolved stays as is, missing -> null) and scope (default compile)
        throw new UnsupportedOperationException("TODO(Day24-task01): dependencies");
    }

    public static boolean onClasspath(String scope, ClasspathKind kind) {
        // TODO(Day24-task01): compile: all three kinds; provided and system: COMPILE and TEST; runtime: RUNTIME and TEST; test: TEST only; null/unknown scope -> IllegalArgumentException
        throw new UnsupportedOperationException("TODO(Day24-task01): onClasspath");
    }

    public static List<String> classpath(List<Dependency> dependencies, ClasspathKind kind) {
        // TODO(Day24-task01): keep the dependencies for which onClasspath(scope, kind) is true and return their coordinates() in declaration order
        throw new UnsupportedOperationException("TODO(Day24-task01): classpath");
    }

    // ---- helpers (provided) -------------------------------------------------------------

    private static Document parse(String xml) {
        if (xml == null || xml.isBlank()) {
            throw new IllegalArgumentException("empty pom");
        }
        try {
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
            factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
            factory.setXIncludeAware(false);
            factory.setExpandEntityReferences(false);
            DocumentBuilder builder = factory.newDocumentBuilder();
            builder.setErrorHandler(new org.xml.sax.helpers.DefaultHandler());   // no console noise; fatal errors still throw
            return builder.parse(new InputSource(new StringReader(xml)));
        } catch (ParserConfigurationException | SAXException | IOException e) {
            throw new IllegalArgumentException("cannot parse pom: " + e.getMessage(), e);
        }
    }

    private static Element child(Element parent, String name) {
        for (Node n = parent.getFirstChild(); n != null; n = n.getNextSibling()) {
            if (n instanceof Element e && e.getTagName().equals(name)) {
                return e;
            }
        }
        return null;
    }

    private static String childText(Element parent, String name) {
        Element e = child(parent, name);
        return e == null ? null : e.getTextContent().trim();
    }

    private static String resolve(String value, Map<String, String> properties) {
        Matcher m = PLACEHOLDER.matcher(value);
        StringBuilder sb = new StringBuilder();
        while (m.find()) {
            String replacement = properties.getOrDefault(m.group(1), m.group());
            m.appendReplacement(sb, Matcher.quoteReplacement(replacement));
        }
        m.appendTail(sb);
        return sb.toString();
    }
}
