package com.javaprep.day39.task04;

import static com.javaprep.day39.task04.SecurityTestSupport.asAdmin;
import static com.javaprep.day39.task04.SecurityTestSupport.asUser;
import static com.javaprep.day39.task04.SecurityTestSupport.asUserWithCsrf;
import static com.javaprep.day39.task04.SecurityTestSupport.basic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(NoteController.class)
@Import(AppSecurityConfig.class)
class SecurityTestSupportTest {

    @Autowired MockMvc mvc;

    @Test
    void anonymousIs401() throws Exception {
        mvc.perform(get("/me")).andExpect(status().isUnauthorized());
    }

    @Test
    void userHelperSetsPrincipal() throws Exception {
        mvc.perform(get("/me").with(asUser("zed"))).andExpect(status().isOk()).andExpect(content().string("zed"));
    }

    @Test
    void userIsNotAdmin() throws Exception {
        mvc.perform(get("/admin").with(asUser("zed"))).andExpect(status().isForbidden());
    }

    @Test
    void adminHelperOpensAdmin() throws Exception {
        mvc.perform(get("/admin").with(asAdmin())).andExpect(status().isOk());
    }

    @Test
    void postWithoutCsrfIsForbidden() throws Exception {
        mvc.perform(post("/notes").with(asUser("zed"))).andExpect(status().isForbidden());
    }

    @Test
    void postWithCsrfHelperWorks() throws Exception {
        mvc.perform(post("/notes").with(asUserWithCsrf("zed"))).andExpect(status().isCreated());
    }

    @Test
    void basicHelperAuthenticatesRealUser() throws Exception {
        mvc.perform(get("/me").with(basic("ann", "pw"))).andExpect(content().string("ann"));
        mvc.perform(get("/me").with(basic("ann", "wrong"))).andExpect(status().isUnauthorized());
    }
}
