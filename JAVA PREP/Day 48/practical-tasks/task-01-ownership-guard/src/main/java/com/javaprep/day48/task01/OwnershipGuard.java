package com.javaprep.day48.task01;

import java.util.Optional;

/** Object-level authorization: who may touch a resource, and what do we reveal when they may not? */
public class OwnershipGuard {

    public enum DenialPolicy {
        /** Existence is hidden: non-owners get the same answer as for a missing resource (404). */
        HIDE_AS_404,
        /** Honest answer: the resource exists but you may not touch it (403). */
        FORBID_403
    }

    private final DenialPolicy policy;

    public OwnershipGuard(DenialPolicy policy) {
        this.policy = policy;
    }

    /**
     * empty -> NotFoundException; owner or admin -> the resource;
     * other callers -> NotFoundException (HIDE_AS_404) or ForbiddenException (FORBID_403).
     */
    public Resource require(Optional<Resource> found, long callerId, boolean admin) {
        // TODO(Day48-task01): implement the decision table above
        throw new UnsupportedOperationException("TODO(Day48-task01): implement require");
    }
}
