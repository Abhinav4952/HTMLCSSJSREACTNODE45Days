package com.javaprep.day30.task01;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(GreetingController.class)
class GreetingControllerTest {

    @Autowired
    MockMvc mvc;

    @Test
    void pathVariableGreeting() throws Exception {
        mvc.perform(get("/api/greetings/Ann")).andExpect(status().isOk()).andExpect(content().string("Hello, Ann!"));
    }

    @Test
    void queryDefaults() throws Exception {
        mvc.perform(get("/api/greetings")).andExpect(status().isOk()).andExpect(content().string("Hello, World!"));
    }

    @Test
    void repeatsGreeting() throws Exception {
        mvc.perform(get("/api/greetings").param("name", "Bo").param("times", "3"))
                .andExpect(content().string("Hello, Bo! Hello, Bo! Hello, Bo!"));
    }

    @Test
    void zeroTimesIsEmpty() throws Exception {
        mvc.perform(get("/api/greetings").param("times", "0")).andExpect(status().isOk()).andExpect(content().string(""));
    }

    @Test
    void badNumberIs400() throws Exception {
        mvc.perform(get("/api/greetings").param("times", "abc")).andExpect(status().isBadRequest());
    }
}
