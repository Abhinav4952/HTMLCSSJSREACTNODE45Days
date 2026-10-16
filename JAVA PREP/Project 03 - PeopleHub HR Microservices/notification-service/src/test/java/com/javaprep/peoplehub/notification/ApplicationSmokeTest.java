package com.javaprep.peoplehub.notification;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Smoke test: the application context starts against an in-memory H2 database (PostgreSQL mode),
 * so `mvn test` needs NO local PostgreSQL. The real database is only used when you run the application.
 */
@SpringBootTest(properties = {
        "spring.datasource.url=jdbc:h2:mem:peoplehub_notification;MODE=PostgreSQL;DB_CLOSE_DELAY=-1",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=none"
})
@AutoConfigureMockMvc
class ApplicationSmokeTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void welcomeEndpointIsUp() throws Exception {
        mvc.perform(get("/")).andExpect(status().isOk()).andExpect(jsonPath("$.status").value("UP"));
    }
}
