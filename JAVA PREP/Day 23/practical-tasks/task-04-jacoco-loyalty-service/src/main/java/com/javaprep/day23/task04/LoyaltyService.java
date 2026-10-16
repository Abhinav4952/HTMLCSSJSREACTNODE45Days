package com.javaprep.day23.task04;

import java.time.Clock;
import java.time.LocalDate;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.Optional;

/** Loyalty points business rules. */
public final class LoyaltyService {

    static final int INACTIVITY_DAYS = 365;

    private final CustomerRepository repository;
    private final Clock clock;

    public LoyaltyService(CustomerRepository repository, Clock clock) {
        this.repository = repository;
        this.clock = clock;
    }

    public static Customer.Tier tierFor(int points) {
        // TODO(Day23-task04): >= 1000 GOLD, >= 500 SILVER, otherwise BRONZE
        throw new UnsupportedOperationException("TODO(Day23-task04): tierFor");
    }

    public Customer earn(String customerId, long spendCents) {
        // TODO(Day23-task04): spend <= 0 -> IAE; load customer or NoSuchElementException('unknown customer: id'); earned = spend/100 * tier multiplier; save and return a copy with new points, tierFor(newPoints) and lastActivity = LocalDate.now(clock)
        throw new UnsupportedOperationException("TODO(Day23-task04): earn");
    }

    public Customer redeem(String customerId, int points) {
        // TODO(Day23-task04): points <= 0 -> IAE; load customer; inactive > 365 days -> IllegalStateException('points expired'); points > balance -> IllegalStateException('insufficient points'); save and return the reduced customer with recomputed tier and lastActivity today
        throw new UnsupportedOperationException("TODO(Day23-task04): redeem");
    }

    public int expireInactive(List<String> customerIds) {
        // TODO(Day23-task04): for every id: skip unknown customers, skip customers with 0 points or activity within 365 days; otherwise save points=0/BRONZE (lastActivity unchanged) and count it
        throw new UnsupportedOperationException("TODO(Day23-task04): expireInactive");
    }

    private Customer load(String customerId) {
        return repository.findById(customerId)
                .orElseThrow(() -> new NoSuchElementException("unknown customer: " + customerId));
    }

    private boolean isInactive(Customer customer) {
        return customer.lastActivity().isBefore(LocalDate.now(clock).minusDays(INACTIVITY_DAYS));
    }
}
