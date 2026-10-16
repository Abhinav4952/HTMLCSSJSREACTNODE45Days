package com.javaprep.day41.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.MDC;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

class RequestIdFilterTest {

    MockMvc mvc;

    @BeforeEach
    void setUp() {
        mvc = MockMvcBuilders.standaloneSetup(new EchoController()).addFilters(new RequestIdFilter()).build();
    }

    @Test
    void incomingIdIsUsedAndEchoed() throws Exception {
        mvc.perform(get("/echo").header("X-Request-Id", "abc-123")).andExpect(status().isOk())
                .andExpect(content().string("abc-123")).andExpect(header().string("X-Request-Id", "abc-123"));
    }

    @Test
    void missingIdIsGenerated() throws Exception {
        String id = mvc.perform(get("/echo")).andReturn().getResponse().getHeader("X-Request-Id");
        assertThat(id).isNotNull();
        assertThat(UUID.fromString(id)).isNotNull();
    }

    @Test
    void unsafeIdIsReplaced() throws Exception {
        String evil = "x\nFAKE LOG LINE";
        String id = mvc.perform(get("/echo").header("X-Request-Id", evil)).andReturn().getResponse().getHeader("X-Request-Id");
        assertThat(id).doesNotContain("FAKE").hasSize(36);
        String tooLong = "a".repeat(65);
        assertThat(mvc.perform(get("/echo").header("X-Request-Id", tooLong)).andReturn().getResponse().getHeader("X-Request-Id")).hasSize(36);
    }

    @Test
    void mdcIsClearedAfterTheRequest() throws Exception {
        mvc.perform(get("/echo").header("X-Request-Id", "keep-clean"));
        assertThat(MDC.get("requestId")).isNull();
    }

    @Test
    void patternReferencesTheMdcKey() {
        assertThat(RequestIdFilter.logPattern()).contains("%X{requestId}").contains("%msg%n");
    }
}
