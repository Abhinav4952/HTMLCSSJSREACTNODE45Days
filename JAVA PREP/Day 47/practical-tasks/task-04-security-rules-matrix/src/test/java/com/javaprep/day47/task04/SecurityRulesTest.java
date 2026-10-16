package com.javaprep.day47.task04;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ProbeController.class)
@Import(SecurityConfig.class)
class SecurityRulesTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void publicEndpointsAreOpen() throws Exception {
        mvc.perform(get("/public/ping")).andExpect(status().isOk());
        mvc.perform(post("/api/auth/login")).andExpect(status().isOk());
    }

    @Test
    void anonymousGets401OnProtectedEndpoints() throws Exception {
        mvc.perform(get("/api/projects")).andExpect(status().isUnauthorized());
        mvc.perform(get("/api/admin/stats")).andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "USER")
    void userCanUseProtectedButNotAdminEndpoints() throws Exception {
        mvc.perform(get("/api/projects")).andExpect(status().isOk());
        mvc.perform(get("/api/admin/stats")).andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminCanUseAdminEndpoints() throws Exception {
        mvc.perform(get("/api/admin/stats")).andExpect(status().isOk());
    }

    @Test
    @WithMockUser(roles = "USER")
    void postWorksWithoutCsrfToken() throws Exception {
        mvc.perform(post("/api/projects")).andExpect(status().isOk());
    }
}
