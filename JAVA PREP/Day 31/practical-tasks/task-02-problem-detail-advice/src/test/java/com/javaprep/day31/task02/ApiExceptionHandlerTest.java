package com.javaprep.day31.task02;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(DemoController.class)
@Import(ApiExceptionHandler.class)
class ApiExceptionHandlerTest {

    @Autowired
    MockMvc mvc;

    @Test
    void notFoundBecomesProblemDetail() throws Exception {
        mvc.perform(get("/api/demo/missing/7")).andExpect(status().isNotFound())
                .andExpect(content().contentTypeCompatibleWith(MediaType.APPLICATION_PROBLEM_JSON))
                .andExpect(jsonPath("$.title").value("Not Found")).andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.detail").value("Item 7 not found"));
    }

    @Test
    void illegalStateBecomesConflict() throws Exception {
        mvc.perform(get("/api/demo/conflict")).andExpect(status().isConflict())
                .andExpect(jsonPath("$.title").value("Conflict")).andExpect(jsonPath("$.detail").value("Already processed"));
    }

    @Test
    void validationFailureListsFieldErrors() throws Exception {
        mvc.perform(post("/api/demo/validate").contentType(MediaType.APPLICATION_JSON).content("{\"title\":\"\"}"))
                .andExpect(status().isBadRequest()).andExpect(jsonPath("$.title").value("Validation failed"))
                .andExpect(jsonPath("$.errors.title").exists());
    }

    @Test
    void happyPathUntouched() throws Exception {
        mvc.perform(post("/api/demo/validate").contentType(MediaType.APPLICATION_JSON).content("{\"title\":\"ok\"}"))
                .andExpect(status().isOk()).andExpect(content().string("ok"));
    }
}
