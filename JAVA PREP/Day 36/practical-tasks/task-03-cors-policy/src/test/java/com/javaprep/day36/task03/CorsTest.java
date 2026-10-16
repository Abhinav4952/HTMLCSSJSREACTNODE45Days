package com.javaprep.day36.task03;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.options;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(DataController.class)
@Import(CorsConfig.class)
class CorsTest {

    static final String ALLOWED = "https://app.example.com";

    @Autowired
    MockMvc mvc;

    @Test
    void preflightFromAllowedOrigin() throws Exception {
        mvc.perform(options("/api/data").header("Origin", ALLOWED).header("Access-Control-Request-Method", "POST")
                        .header("Access-Control-Request-Headers", "content-type"))
                .andExpect(status().isOk())
                .andExpect(header().string("Access-Control-Allow-Origin", ALLOWED))
                .andExpect(header().string("Access-Control-Allow-Credentials", "true"))
                .andExpect(header().string("Access-Control-Max-Age", "3600"))
                .andExpect(header().string("Access-Control-Allow-Methods", containsString("POST")))
                .andExpect(header().string("Access-Control-Allow-Headers", containsString("content-type")));
    }

    @Test
    void deleteIsAllowedButPatchIsNot() throws Exception {
        mvc.perform(options("/api/data/5").header("Origin", ALLOWED).header("Access-Control-Request-Method", "DELETE"))
                .andExpect(status().isOk());
        mvc.perform(options("/api/data").header("Origin", ALLOWED).header("Access-Control-Request-Method", "PATCH"))
                .andExpect(status().isForbidden());
    }

    @Test
    void preflightFromOtherOriginIsForbidden() throws Exception {
        mvc.perform(options("/api/data").header("Origin", "https://evil.example").header("Access-Control-Request-Method", "GET"))
                .andExpect(status().isForbidden());
    }

    @Test
    void simpleRequestGetsAllowOriginHeader() throws Exception {
        mvc.perform(get("/api/data").header("Origin", ALLOWED)).andExpect(status().isOk())
                .andExpect(header().string("Access-Control-Allow-Origin", ALLOWED));
    }

    @Test
    void noOriginNoCorsHeaders() throws Exception {
        mvc.perform(get("/api/data")).andExpect(status().isOk()).andExpect(header().doesNotExist("Access-Control-Allow-Origin"));
    }

    @Test
    void pathsOutsideTheMappingGetNoCorsHeaders() throws Exception {
        mvc.perform(get("/other").header("Origin", ALLOWED)).andExpect(header().doesNotExist("Access-Control-Allow-Origin"));
    }

    @Test
    void crossOriginAnnotationOpensOnlyThePingEndpoint() throws Exception {
        mvc.perform(get("/public/ping").header("Origin", "https://anyone.example")).andExpect(status().isOk())
                .andExpect(header().string("Access-Control-Allow-Origin", "*"));
    }
}
