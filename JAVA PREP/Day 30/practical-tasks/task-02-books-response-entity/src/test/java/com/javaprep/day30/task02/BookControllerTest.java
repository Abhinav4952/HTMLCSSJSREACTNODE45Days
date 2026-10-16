package com.javaprep.day30.task02;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(BookController.class)
@Import(BookService.class)
@org.springframework.test.annotation.DirtiesContext(classMode = org.springframework.test.annotation.DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class BookControllerTest {

    @Autowired
    MockMvc mvc;

    private void create(String json) throws Exception {
        mvc.perform(post("/api/books").contentType(MediaType.APPLICATION_JSON).content(json)).andExpect(status().isCreated());
    }

    @Test
    void emptyListInitially() throws Exception {
        mvc.perform(get("/api/books")).andExpect(status().isOk()).andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void createReturns201WithLocation() throws Exception {
        mvc.perform(post("/api/books").contentType(MediaType.APPLICATION_JSON).content("{\"title\":\"Dune\",\"author\":\"Herbert\"}"))
                .andExpect(status().isCreated())
                .andExpect(header().string("Location", "/api/books/1"))
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.title").value("Dune"));
    }

    @Test
    void getExistingAndMissing() throws Exception {
        create("{\"title\":\"A\",\"author\":\"B\"}");
        mvc.perform(get("/api/books/1")).andExpect(status().isOk()).andExpect(jsonPath("$.author").value("B"));
        mvc.perform(get("/api/books/99")).andExpect(status().isNotFound());
    }

    @Test
    void listContainsCreatedBooks() throws Exception {
        create("{\"title\":\"A\",\"author\":\"B\"}");
        create("{\"title\":\"C\",\"author\":\"D\"}");
        mvc.perform(get("/api/books")).andExpect(jsonPath("$", hasSize(2))).andExpect(jsonPath("$[1].title").value("C"));
    }

    @Test
    void deleteIs204ThenMissingIs404() throws Exception {
        create("{\"title\":\"A\",\"author\":\"B\"}");
        mvc.perform(delete("/api/books/1")).andExpect(status().isNoContent());
        mvc.perform(delete("/api/books/1")).andExpect(status().isNotFound());
    }

    @Test
    void malformedJsonIs400() throws Exception {
        mvc.perform(post("/api/books").contentType(MediaType.APPLICATION_JSON).content("{oops")).andExpect(status().isBadRequest());
    }
}
