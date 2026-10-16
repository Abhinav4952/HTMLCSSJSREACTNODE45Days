package com.javaprep.day37.task04;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class RoleRulesTest {

    @Autowired
    MockMvc mvc;

    @Test
    void publicIsOpen() throws Exception {
        mvc.perform(get("/public/ping")).andExpect(status().isOk());
    }

    @Test
    void anonymousIsRejected() throws Exception {
        mvc.perform(get("/api/reports")).andExpect(status().isUnauthorized());
    }

    @Test
    void wrongPasswordIsRejected() throws Exception {
        mvc.perform(get("/api/reports").with(httpBasic("bob", "wrong"))).andExpect(status().isUnauthorized());
        mvc.perform(get("/api/reports").with(httpBasic("ghost", "bobpw"))).andExpect(status().isUnauthorized());
    }

    @Test
    void userCanReadReports() throws Exception {
        mvc.perform(get("/api/reports").with(httpBasic("bob", "bobpw"))).andExpect(status().isOk()).andExpect(jsonPath("$[0]").value("q1"));
    }

    @Test
    void userCannotDelete() throws Exception {
        mvc.perform(delete("/api/reports/q1").with(httpBasic("bob", "bobpw"))).andExpect(status().isForbidden());
    }

    @Test
    void adminCanDelete() throws Exception {
        mvc.perform(delete("/api/reports/q1").with(httpBasic("alice", "alicepw"))).andExpect(status().isNoContent());
    }

    @Test
    void whoamiShowsAuthorities() throws Exception {
        mvc.perform(get("/api/whoami").with(httpBasic("alice", "alicepw"))).andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("alice")).andExpect(jsonPath("$.authorities[0]").value("ROLE_ADMIN"));
    }
}
