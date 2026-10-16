package com.javaprep.day41.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.actuate.health.Status;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class QueueHealthTest {

    @Autowired
    MockMvc mvc;
    @Autowired
    QueueStats stats;

    @BeforeEach
    void reset() {
        stats.setDepth(0);
    }

    @Test
    void unitLevelStatusMapping() {
        QueueHealthIndicator hi = new QueueHealthIndicator(stats);
        stats.setDepth(79);
        assertThat(hi.health().getStatus()).isEqualTo(Status.UP);
        stats.setDepth(80);
        assertThat(hi.health().getStatus()).isEqualTo(Status.OUT_OF_SERVICE);
        stats.setDepth(99);
        assertThat(hi.health().getStatus()).isEqualTo(Status.OUT_OF_SERVICE);
        stats.setDepth(100);
        assertThat(hi.health().getStatus()).isEqualTo(Status.DOWN);
    }

    @Test
    void detailsAreAlwaysPresent() {
        stats.setDepth(12);
        assertThat(new QueueHealthIndicator(stats).health().getDetails()).containsEntry("depth", 12).containsEntry("capacity", 100);
    }

    @Test
    void healthyQueueGivesHttp200AndComponentUp() throws Exception {
        stats.setDepth(10);
        mvc.perform(get("/actuator/health")).andExpect(status().isOk()).andExpect(jsonPath("$.status").value("UP"))
                .andExpect(jsonPath("$.components.queue.status").value("UP"))
                .andExpect(jsonPath("$.components.queue.details.depth").value(10));
    }

    @Test
    void drainingQueueGivesHttp503() throws Exception {
        stats.setDepth(90);
        mvc.perform(get("/actuator/health")).andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.status").value("OUT_OF_SERVICE")).andExpect(jsonPath("$.components.queue.status").value("OUT_OF_SERVICE"));
    }

    @Test
    void fullQueueMakesTheApplicationDown() throws Exception {
        stats.setDepth(150);
        mvc.perform(get("/actuator/health")).andExpect(status().isServiceUnavailable()).andExpect(jsonPath("$.status").value("DOWN"));
    }
}
