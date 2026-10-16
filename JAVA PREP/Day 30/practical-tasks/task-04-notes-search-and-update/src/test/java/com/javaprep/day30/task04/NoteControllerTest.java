package com.javaprep.day30.task04;

import static org.hamcrest.Matchers.hasSize;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(NoteController.class)
@Import(NoteService.class)
@org.springframework.test.annotation.DirtiesContext(classMode = org.springframework.test.annotation.DirtiesContext.ClassMode.AFTER_EACH_TEST_METHOD)
class NoteControllerTest {

    @Autowired
    MockMvc mvc;
    @Autowired
    NoteService service;

    @BeforeEach
    void seed() {
        service.add("Buy milk");
        service.add("Call Mom");
        service.add("Milk the cow");
    }

    @Test
    void listsAllWithTotalHeader() throws Exception {
        mvc.perform(get("/api/notes")).andExpect(status().isOk()).andExpect(jsonPath("$", hasSize(3)))
                .andExpect(header().string("X-Total-Count", "3"));
    }

    @Test
    void filtersCaseInsensitively() throws Exception {
        mvc.perform(get("/api/notes").param("contains", "MILK")).andExpect(jsonPath("$", hasSize(2)))
                .andExpect(header().string("X-Total-Count", "2"));
    }

    @Test
    void limitCutsPageButNotTotal() throws Exception {
        mvc.perform(get("/api/notes").param("limit", "1")).andExpect(jsonPath("$", hasSize(1)))
                .andExpect(header().string("X-Total-Count", "3"));
        mvc.perform(get("/api/notes").param("limit", "0")).andExpect(jsonPath("$", hasSize(0)));
    }

    @Test
    void updateReturnsNewNote() throws Exception {
        mvc.perform(put("/api/notes/2").contentType(MediaType.APPLICATION_JSON).content("{\"text\":\"Call Dad\"}"))
                .andExpect(status().isOk()).andExpect(jsonPath("$.text").value("Call Dad")).andExpect(jsonPath("$.id").value(2));
    }

    @Test
    void updateUnknownIs404() throws Exception {
        mvc.perform(put("/api/notes/42").contentType(MediaType.APPLICATION_JSON).content("{\"text\":\"x\"}")).andExpect(status().isNotFound());
    }

    @Test
    void blankTextIs400EvenForUnknownId() throws Exception {
        mvc.perform(put("/api/notes/42").contentType(MediaType.APPLICATION_JSON).content("{\"text\":\"  \"}"))
                .andExpect(status().isBadRequest()).andExpect(jsonPath("$.error").value("text must not be blank"));
        mvc.perform(put("/api/notes/1").contentType(MediaType.APPLICATION_JSON).content("{}")).andExpect(status().isBadRequest());
    }
}
