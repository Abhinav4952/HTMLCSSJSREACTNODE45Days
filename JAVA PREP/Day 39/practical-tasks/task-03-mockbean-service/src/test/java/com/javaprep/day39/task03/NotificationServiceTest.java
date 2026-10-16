package com.javaprep.day39.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.BDDMockito.given;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;

import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

@SpringBootTest(classes = NotificationService.class)
class NotificationServiceTest {

    @Autowired NotificationService service;
    @MockitoBean EmailGateway gateway;
    @MockitoBean UserLookup users;

    @Test
    void sendsToLookedUpEmail() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(gateway.send("a@x.io", "hi")).willReturn(true);
        assertThat(service.notifyUser(1, "hi")).isTrue();
        ArgumentCaptor<String> to = ArgumentCaptor.forClass(String.class);
        verify(gateway).send(to.capture(), org.mockito.ArgumentMatchers.eq("hi"));
        assertThat(to.getValue()).isEqualTo("a@x.io");
    }

    @Test
    void blankMessageTouchesNothing() {
        assertThatThrownBy(() -> service.notifyUser(1, " ")).isInstanceOf(IllegalArgumentException.class);
        verifyNoInteractions(gateway, users);
    }

    @Test
    void unknownUserNeverCallsGateway() {
        given(users.findEmail(2)).willReturn(Optional.empty());
        assertThatThrownBy(() -> service.notifyUser(2, "hi")).isInstanceOf(NoSuchElementException.class);
        verify(gateway, never()).send(anyString(), anyString());
    }

    @Test
    void gatewayFailureBecomesFalse() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(gateway.send(anyString(), anyString())).willThrow(new GatewayException("down"));
        assertThat(service.notifyUser(1, "hi")).isFalse();
    }

    @Test
    void rejectedByProviderIsFalse() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(gateway.send(anyString(), anyString())).willReturn(false);
        assertThat(service.notifyUser(1, "hi")).isFalse();
    }

    @Test
    void broadcastCountsOnlySuccessesAndKeepsGoing() {
        given(users.findEmail(1)).willReturn(Optional.of("a@x.io"));
        given(users.findEmail(2)).willReturn(Optional.empty());
        given(users.findEmail(3)).willReturn(Optional.of("c@x.io"));
        given(users.findEmail(4)).willReturn(Optional.of("d@x.io"));
        given(gateway.send("a@x.io", "news")).willReturn(true);
        given(gateway.send("c@x.io", "news")).willThrow(new GatewayException("boom"));
        given(gateway.send("d@x.io", "news")).willReturn(true);
        assertThat(service.broadcast(List.of(1L, 2L, 3L, 4L), "news")).isEqualTo(2);
        verify(gateway, times(3)).send(anyString(), org.mockito.ArgumentMatchers.eq("news"));
    }
}
