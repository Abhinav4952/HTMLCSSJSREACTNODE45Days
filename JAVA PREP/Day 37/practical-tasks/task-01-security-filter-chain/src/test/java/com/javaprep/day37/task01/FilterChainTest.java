package com.javaprep.day37.task01;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class FilterChainTest {

    @Autowired
    MockMvc mvc;

    @Test
    void publicPathsAreOpen() throws Exception {
        mvc.perform(get("/public/hello")).andExpect(status().isOk()).andExpect(content().string("hello"));
    }

    @Test
    void anonymousGets401WithBasicChallenge() throws Exception {
        mvc.perform(get("/api/me")).andExpect(status().isUnauthorized())
                .andExpect(header().string("WWW-Authenticate", org.hamcrest.Matchers.startsWith("Basic")));
    }

    @Test
    void unknownPathsAreProtectedToo() throws Exception {
        mvc.perform(get("/something/else")).andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(username = "ann")
    void authenticatedUserSeesOwnName() throws Exception {
        mvc.perform(get("/api/me")).andExpect(status().isOk()).andExpect(content().string("ann"));
    }

    @Test
    @WithMockUser(roles = "USER")
    void plainUserCannotEnterAdminArea() throws Exception {
        mvc.perform(get("/admin/stats")).andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminCanEnterAdminArea() throws Exception {
        mvc.perform(get("/admin/stats")).andExpect(status().isOk());
    }

    @Test
    @WithMockUser
    void postWorksWithoutCsrfTokenForStatelessApi() throws Exception {
        mvc.perform(post("/api/echo").content("ping")).andExpect(status().isOk()).andExpect(content().string("ping"));
    }
}
