package com.javaprep.day35.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.math.BigDecimal;
import java.util.NoSuchElementException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class TransferServiceTest {

    @Autowired
    TransferService service;
    @Autowired
    BankAccountRepository repository;

    long a, b;

    @BeforeEach
    void setUp() {
        repository.deleteAll();
        a = repository.save(new BankAccount("Ann", "100.00")).getId();
        b = repository.save(new BankAccount("Bob", "20.00")).getId();
    }

    @Test
    void successfulTransferMovesMoney() {
        service.transfer(a, b, new BigDecimal("30.00"));
        assertThat(service.balanceOf(a)).isEqualByComparingTo("70");
        assertThat(service.balanceOf(b)).isEqualByComparingTo("50");
    }

    @Test
    void insufficientFundsChangesNothing() {
        assertThatThrownBy(() -> service.transfer(a, b, new BigDecimal("500"))).isInstanceOf(InsufficientFundsException.class);
        assertThat(service.balanceOf(a)).isEqualByComparingTo("100");
        assertThat(service.balanceOf(b)).isEqualByComparingTo("20");
    }

    @Test
    void failureAfterDebitRollsEverythingBack() {
        assertThatThrownBy(() -> service.transfer(a, 99999L, new BigDecimal("30"))).isInstanceOf(NoSuchElementException.class);
        assertThat(service.balanceOf(a)).isEqualByComparingTo("100");
    }

    @Test
    void checkedExceptionRollsBackBecauseOfRollbackFor() {
        assertThatThrownBy(() -> service.transferWithAudit(a, b, new BigDecimal("10")))
                .isInstanceOf(AuditUnavailableException.class);
        assertThat(service.balanceOf(a)).isEqualByComparingTo("100");
        assertThat(service.balanceOf(b)).isEqualByComparingTo("20");
    }

    @Test
    void unknownAccountBalanceThrows() {
        assertThatThrownBy(() -> service.balanceOf(424242L)).isInstanceOf(NoSuchElementException.class);
    }
}
