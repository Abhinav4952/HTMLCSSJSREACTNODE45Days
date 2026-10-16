package com.javaprep.day38.task02;

import static org.assertj.core.api.Assertions.assertThat;

import java.time.Duration;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.springframework.mock.web.MockFilterChain;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.mock.web.MockHttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;

class JwtAuthFilterTest {

    static final String SECRET = "0123456789-0123456789-0123456789-ab";
    final JwtUtil jwt = new JwtUtil(SECRET, Duration.ofMinutes(5));
    final JwtAuthFilter filter = new JwtAuthFilter(jwt);

    @AfterEach
    void clear() {
        SecurityContextHolder.clearContext();
    }

    private MockFilterChain run(String authorization) throws Exception {
        MockHttpServletRequest req = new MockHttpServletRequest();
        if (authorization != null) {
            req.addHeader("Authorization", authorization);
        }
        MockFilterChain chain = new MockFilterChain();
        filter.doFilter(req, new MockHttpServletResponse(), chain);
        return chain;
    }

    @Test
    void validTokenAuthenticates() throws Exception {
        MockFilterChain chain = run("Bearer " + jwt.generate("ann", List.of("USER", "ADMIN")));
        Authentication a = SecurityContextHolder.getContext().getAuthentication();
        assertThat(a).isNotNull();
        assertThat(a.getName()).isEqualTo("ann");
        assertThat(a.getAuthorities()).extracting(GrantedAuthority::getAuthority).containsExactlyInAnyOrder("ROLE_USER", "ROLE_ADMIN");
        assertThat(chain.getRequest()).as("chain continued").isNotNull();
    }

    @Test
    void missingHeaderLeavesContextEmpty() throws Exception {
        MockFilterChain chain = run(null);
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        assertThat(chain.getRequest()).isNotNull();
    }

    @Test
    void invalidTokenDoesNotAuthenticateButContinues() throws Exception {
        MockFilterChain chain = run("Bearer abc.def.ghi");
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        assertThat(chain.getRequest()).isNotNull();
    }

    @Test
    void otherSchemesAreIgnored() throws Exception {
        MockFilterChain chain = run("Basic YW5uOnB3");
        assertThat(SecurityContextHolder.getContext().getAuthentication()).isNull();
        assertThat(chain.getRequest()).isNotNull();
    }
}
