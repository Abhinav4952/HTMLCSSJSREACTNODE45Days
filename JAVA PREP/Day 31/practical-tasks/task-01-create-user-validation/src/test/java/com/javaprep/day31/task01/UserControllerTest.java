package com.javaprep.day31.task01;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;

@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    MockMvc mvc;

    private ResultActions submit(String name, String email, int age, String password) throws Exception {
        String json = "{\"name\":\"%s\",\"email\":\"%s\",\"age\":%d,\"password\":\"%s\"}".formatted(name, email, age, password);
        return mvc.perform(post("/api/users").contentType(MediaType.APPLICATION_JSON).content(json));
    }

    @Test
    void validRequestCreatesUserWithoutPassword() throws Exception {
        submit(" Ann ", "Ann@Example.com", 30, "longenough").andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").isNumber()).andExpect(jsonPath("$.name").value("Ann"))
                .andExpect(jsonPath("$.email").value("ann@example.com")).andExpect(jsonPath("$.password").doesNotExist());
    }

    @Test
    void blankNameRejected() throws Exception {
        submit("  ", "a@b.co", 30, "longenough").andExpect(status().isBadRequest());
    }

    @Test
    void badEmailRejected() throws Exception {
        submit("Ann", "not-an-email", 30, "longenough").andExpect(status().isBadRequest());
    }

    @Test
    void ageBoundsRejected() throws Exception {
        submit("Ann", "a@b.co", 17, "longenough").andExpect(status().isBadRequest());
        submit("Ann", "a@b.co", 121, "longenough").andExpect(status().isBadRequest());
        submit("Ann", "a@b.co", 18, "longenough").andExpect(status().isCreated());
    }

    @Test
    void shortPasswordRejected() throws Exception {
        submit("Ann", "a@b.co", 30, "short").andExpect(status().isBadRequest());
    }
}
