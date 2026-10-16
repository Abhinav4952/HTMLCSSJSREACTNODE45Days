package com.javaprep.day23.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;

import java.time.Clock;
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class LoyaltyServiceTest {

    private static final Clock CLOCK = Clock.fixed(Instant.parse("2026-03-01T10:00:00Z"), ZoneOffset.UTC);
    private static final LocalDate TODAY = LocalDate.of(2026, 3, 1);

    @Mock
    CustomerRepository repository;
    @Captor
    ArgumentCaptor<Customer> saved;

    LoyaltyService service;

    @BeforeEach
    void setUp() {
        service = new LoyaltyService(repository, CLOCK);
    }

    private static Customer customer(String id, int points, LocalDate last, Customer.Tier tier) {
        return new Customer(id, points, last, tier);
    }

    // ---------------------------------------------------------------- tierFor
    @ParameterizedTest
    @CsvSource({"0,BRONZE", "1,BRONZE", "499,BRONZE", "500,SILVER", "999,SILVER", "1000,GOLD", "50000,GOLD"})
    void r1_tierThresholds(int points, Customer.Tier expected) {
        assertThat(LoyaltyService.tierFor(points)).isEqualTo(expected);
    }

    // ---------------------------------------------------------------- earn
    @Test
    void r2_earnUsesTheTierMultiplierAndUpdatesActivity() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 100, TODAY.minusDays(10), Customer.Tier.BRONZE)));

        Customer result = service.earn("c1", 12_345);   // 123 * 1

        assertThat(result.points()).isEqualTo(223);
        assertThat(result.tier()).isEqualTo(Customer.Tier.BRONZE);
        assertThat(result.lastActivity()).isEqualTo(TODAY);
        verify(repository).save(saved.capture());
        assertThat(saved.getValue()).isEqualTo(result);
    }

    @Test
    void r2_goldEarnsTripleAndSilverDouble() {
        when(repository.findById("gold")).thenReturn(Optional.of(customer("gold", 1_000, TODAY, Customer.Tier.GOLD)));
        when(repository.findById("silver")).thenReturn(Optional.of(customer("silver", 500, TODAY, Customer.Tier.SILVER)));

        assertThat(service.earn("gold", 5_000).points()).isEqualTo(1_150);     // 50 * 3
        assertThat(service.earn("silver", 5_099).points()).isEqualTo(600);     // 50 * 2 (cents below 100 ignored)
    }

    @Test
    void r2_earnPromotesAcrossTierBoundaries() {
        when(repository.findById("a")).thenReturn(Optional.of(customer("a", 499, TODAY, Customer.Tier.BRONZE)));
        when(repository.findById("b")).thenReturn(Optional.of(customer("b", 998, TODAY, Customer.Tier.SILVER)));
        when(repository.findById("c")).thenReturn(Optional.of(customer("c", 0, TODAY, Customer.Tier.BRONZE)));

        assertThat(service.earn("a", 100).tier()).isEqualTo(Customer.Tier.SILVER);   // 500
        assertThat(service.earn("b", 100).tier()).isEqualTo(Customer.Tier.GOLD);     // 998 + 2 = 1000
        assertThat(service.earn("c", 99).points()).as("less than one whole currency unit").isZero();
    }

    @Test
    void r2_earnRejectsInvalidInput() {
        assertThatThrownBy(() -> service.earn("c1", 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.earn("c1", -5)).isInstanceOf(IllegalArgumentException.class);
        when(repository.findById("ghost")).thenReturn(Optional.empty());
        assertThatThrownBy(() -> service.earn("ghost", 100))
                .isInstanceOf(NoSuchElementException.class)
                .hasMessage("unknown customer: ghost");
        verify(repository, never()).save(any());
    }

    // ---------------------------------------------------------------- redeem
    @Test
    void r3_redeemDeductsAndRecomputesTier() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 1_200, TODAY.minusDays(30), Customer.Tier.GOLD)));

        Customer result = service.redeem("c1", 300);

        assertThat(result.points()).isEqualTo(900);
        assertThat(result.tier()).isEqualTo(Customer.Tier.SILVER);
        assertThat(result.lastActivity()).isEqualTo(TODAY);
        verify(repository).save(saved.capture());
        assertThat(saved.getValue()).isEqualTo(result);
    }

    @Test
    void r3_redeemAllPointsIsAllowed() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 50, TODAY, Customer.Tier.BRONZE)));
        assertThat(service.redeem("c1", 50).points()).isZero();
    }

    @Test
    void r3_redeemMoreThanBalanceFails() {
        when(repository.findById("c1")).thenReturn(Optional.of(customer("c1", 50, TODAY, Customer.Tier.BRONZE)));
        assertThatThrownBy(() -> service.redeem("c1", 51))
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("insufficient points");
        verify(repository, never()).save(any());
    }

    @Test
    void r3_exactly365DaysInactiveIsStillValidButOneMoreDayExpires() {
        when(repository.findById("edge")).thenReturn(Optional.of(customer("edge", 100, TODAY.minusDays(365), Customer.Tier.BRONZE)));
        when(repository.findById("old")).thenReturn(Optional.of(customer("old", 100, TODAY.minusDays(366), Customer.Tier.BRONZE)));

        assertThat(service.redeem("edge", 10).points()).isEqualTo(90);
        assertThatThrownBy(() -> service.redeem("old", 10))
                .isInstanceOf(IllegalStateException.class)
                .hasMessage("points expired");
        verify(repository, times(1)).save(any());
    }

    @Test
    void r3_redeemRejectsInvalidInput() {
        assertThatThrownBy(() -> service.redeem("c1", 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.redeem("c1", -1)).isInstanceOf(IllegalArgumentException.class);
        when(repository.findById("ghost")).thenReturn(Optional.empty());
        assertThatThrownBy(() -> service.redeem("ghost", 5)).isInstanceOf(NoSuchElementException.class);
    }

    // ---------------------------------------------------------------- expireInactive
    @Test
    void r4_expireInactiveResetsOnlyStaleCustomersWithPoints() {
        LocalDate stale = TODAY.minusDays(400);
        when(repository.findById("stale-1")).thenReturn(Optional.of(customer("stale-1", 700, stale, Customer.Tier.SILVER)));
        when(repository.findById("stale-0")).thenReturn(Optional.of(customer("stale-0", 0, stale, Customer.Tier.BRONZE)));
        when(repository.findById("fresh")).thenReturn(Optional.of(customer("fresh", 900, TODAY.minusDays(365), Customer.Tier.SILVER)));
        when(repository.findById("missing")).thenReturn(Optional.empty());

        int expired = service.expireInactive(List.of("stale-1", "stale-0", "fresh", "missing"));

        assertThat(expired).isEqualTo(1);
        verify(repository).save(saved.capture());
        assertThat(saved.getValue()).isEqualTo(customer("stale-1", 0, stale, Customer.Tier.BRONZE));
        verify(repository, times(4)).findById(any());
        verifyNoMoreInteractions(repository);
    }

    @Test
    void r4_expireInactiveWithNoIdsDoesNothing() {
        assertThat(service.expireInactive(List.of())).isZero();
        verifyNoMoreInteractions(repository);
    }
}
