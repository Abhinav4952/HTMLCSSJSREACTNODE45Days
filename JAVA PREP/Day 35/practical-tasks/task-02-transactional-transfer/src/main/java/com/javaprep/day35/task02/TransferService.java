package com.javaprep.day35.task02;

import java.math.BigDecimal;
import java.util.NoSuchElementException;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TransferService {

    private final BankAccountRepository repository;

    public TransferService(BankAccountRepository repository) {
        this.repository = repository;
    }

    private BankAccount find(long id) {
        return repository.findById(id).orElseThrow(() -> new NoSuchElementException("Account " + id + " not found"));
    }

    /**
     * Moves money atomically.
     * 1. load source; if balance < amount -> InsufficientFundsException (nothing changed)
     * 2. debit the source and saveAndFlush it
     * 3. load the target (unknown id -> NoSuchElementException) and credit it
     * If ANY step fails after step 2, the debit must be rolled back.
     */
    // TODO(Day35-task02): make this method run in a transaction
    public void transfer(long fromId, long toId, BigDecimal amount) {
        // TODO(Day35-task02): implement steps 1-3
        throw new UnsupportedOperationException("TODO(Day35-task02): implement steps 1-3");
    }

    /**
     * Same as transfer, then calls the audit system which is down: always throws AuditUnavailableException
     * AFTER the money moved. The whole transfer must be rolled back anyway.
     */
    // TODO(Day35-task02): transactional, rolling back for the CHECKED exception too (rollbackFor)
    public void transferWithAudit(long fromId, long toId, BigDecimal amount) throws AuditUnavailableException {
        // TODO(Day35-task02): call transfer logic (not through a proxy: inline the steps or call this.transfer) then throw AuditUnavailableException
        throw new UnsupportedOperationException("TODO(Day35-task02): call transfer logic (not through a proxy: inline the steps or call this.transfer) then throw AuditUnavailableException");
    }

    /** Read-only lookup. */
    // TODO(Day35-task02): read-only transaction
    public BigDecimal balanceOf(long id) {
        // TODO(Day35-task02): return the balance
        throw new UnsupportedOperationException("TODO(Day35-task02): return the balance");
    }
}
