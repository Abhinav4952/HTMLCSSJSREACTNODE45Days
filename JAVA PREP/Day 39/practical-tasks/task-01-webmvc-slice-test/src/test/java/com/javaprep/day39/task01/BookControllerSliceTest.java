package com.javaprep.day39.task01;

import static org.hamcrest.Matchers.hasSize;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.test.web.servlet.MockMvc;

/** Web slice: only MVC infrastructure + BookController are loaded; the service is a Mockito mock. */
@WebMvcTest(BookController.class)
class BookControllerSliceTest {

    @Autowired MockMvc mvc;
    @MockitoBean BookService service;

    @Test
    void returnsBookJson() throws Exception {
        given(service.find(1)).willReturn(Optional.of(new Book(1, "Dune", "Herbert")));
        mvc.perform(get("/books/1")).andExpect(status().isOk())
                .andExpect(jsonPath("$.title").value("Dune")).andExpect(jsonPath("$.author").value("Herbert"));
    }

    @Test
    void unknownBookIs404() throws Exception {
        given(service.find(9)).willReturn(Optional.empty());
        mvc.perform(get("/books/9")).andExpect(status().isNotFound());
    }

    @Test
    void listsAll() throws Exception {
        given(service.findAll()).willReturn(List.of(new Book(1, "A", "x"), new Book(2, "B", "y")));
        mvc.perform(get("/books")).andExpect(status().isOk()).andExpect(jsonPath("$", hasSize(2)));
        verify(service, never()).byAuthor(org.mockito.ArgumentMatchers.anyString());
    }

    @Test
    void filtersByAuthor() throws Exception {
        given(service.byAuthor("x")).willReturn(List.of(new Book(1, "A", "x")));
        mvc.perform(get("/books").param("author", "x")).andExpect(jsonPath("$", hasSize(1)));
        verify(service).byAuthor("x");
        verify(service, never()).findAll();
    }

    @Test
    void badIdTypeIs400() throws Exception {
        mvc.perform(get("/books/abc")).andExpect(status().isBadRequest());
    }
}
