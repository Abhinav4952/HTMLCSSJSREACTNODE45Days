package com.javaprep.day38.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.AuthenticationCredentialsNotFoundException;
import org.springframework.security.test.context.support.WithMockUser;

@SpringBootTest
class MethodSecurityTest {

    @Autowired ReportService service;

    @Test
    @WithMockUser(roles = "USER")
    void userCannotDeleteAll() {
        assertThatThrownBy(service::deleteAll).isInstanceOf(AccessDeniedException.class);
    }

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminCanDeleteAll() {
        assertThat(service.deleteAll()).isEqualTo("deleted");
    }

    @Test
    @WithMockUser(roles = "USER")
    void userCanView() {
        assertThat(service.view()).isEqualTo("report");
    }

    @Test
    @WithMockUser(roles = "GUEST")
    void guestCannotView() {
        assertThatThrownBy(service::view).isInstanceOf(AccessDeniedException.class);
    }

    @Test
    @WithMockUser(username = "ann", roles = "USER")
    void ownerReadsOwnReportOnly() {
        assertThat(service.readFor("ann")).isEqualTo("report-of-ann");
        assertThatThrownBy(() -> service.readFor("bob")).isInstanceOf(AccessDeniedException.class);
    }

    @Test
    @WithMockUser(username = "root", roles = "ADMIN")
    void adminReadsAnyReport() {
        assertThat(service.readFor("bob")).isEqualTo("report-of-bob");
    }

    @Test
    void anonymousCallsAreRejected() {
        assertThatThrownBy(service::view).isInstanceOfAny(AccessDeniedException.class, AuthenticationCredentialsNotFoundException.class);
    }
}
