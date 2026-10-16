package com.javaprep.day38.task03;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(ApiController.class)
@Import({SecurityConfig.class, JwtConfig.class})
class Status401Vs403Test {

    @Autowired MockMvc mvc;
    @Autowired JwtUtil jwt;

    private String bearer(String user, String... roles) {
        return "Bearer " + jwt.generate(user, List.of(roles));
    }

    @Test
    void publicIsOpen() throws Exception {
        mvc.perform(get("/public/ping")).andExpect(status().isOk()).andExpect(content().string("pong"));
    }

    @Test
    void noTokenIs401Json() throws Exception {
        mvc.perform(get("/api/hello")).andExpect(status().isUnauthorized())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.error").value("unauthorized"));
    }

    @Test
    void garbageTokenIs401() throws Exception {
        mvc.perform(get("/api/hello").header("Authorization", "Bearer nope")).andExpect(status().isUnauthorized());
    }

    @Test
    void userCanReadApiButNotAdmin() throws Exception {
        mvc.perform(get("/api/hello").header("Authorization", bearer("ann", "USER"))).andExpect(status().isOk());
        mvc.perform(get("/admin/stats").header("Authorization", bearer("ann", "USER"))).andExpect(status().isForbidden())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_JSON))
                .andExpect(jsonPath("$.error").value("forbidden"));
    }

    @Test
    void adminCanReadAdmin() throws Exception {
        mvc.perform(get("/admin/stats").header("Authorization", bearer("root", "ADMIN"))).andExpect(status().isOk());
    }
}
