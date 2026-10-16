package com.javaprep.day39.task04;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;

import org.springframework.test.web.servlet.request.RequestPostProcessor;

/**
 * Reusable helpers that keep security noise out of test bodies.
 * Every method returns a RequestPostProcessor usable as `mvc.perform(get("/x").with(...))`.
 */
public final class SecurityTestSupport {

    private SecurityTestSupport() {
    }

    /** Authenticated principal `name` with the single role USER. */
    public static RequestPostProcessor asUser(String name) {
        // TODO(Day39-task04): build with SecurityMockMvcRequestPostProcessors.user(name).roles("USER")
        throw new UnsupportedOperationException("TODO(Day39-task04): build with SecurityMockMvcRequestPostProcessors.user(name).roles('USER')");
    }

    /** Authenticated principal "admin" with roles ADMIN and USER. */
    public static RequestPostProcessor asAdmin() {
        // TODO(Day39-task04): user("admin") with roles ADMIN and USER
        throw new UnsupportedOperationException("TODO(Day39-task04): user('admin') with roles ADMIN and USER");
    }

    /** Same as asUser(name) but ALSO carrying a valid CSRF token (for POST/PUT/DELETE). */
    public static RequestPostProcessor asUserWithCsrf(String name) {
        // TODO(Day39-task04): combine asUser(name) and csrf()
        throw new UnsupportedOperationException("TODO(Day39-task04): combine asUser(name) and csrf()");
    }

    /** HTTP Basic credentials header. */
    public static RequestPostProcessor basic(String username, String password) {
        // TODO(Day39-task04): delegate to httpBasic
        throw new UnsupportedOperationException("TODO(Day39-task04): delegate to httpBasic");
    }
}
