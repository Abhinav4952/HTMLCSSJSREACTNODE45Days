package com.javaprep.day49.task04;

import java.util.regex.Pattern;

/** Team Git conventions as executable rules (branch names, commit messages, release versions). */
public final class GitConventions {

    private GitConventions() {
    }

    /**
     * Valid branch names:
     * <ul>
     *   <li>"main" or "develop"</li>
     *   <li>"feature/", "bugfix/", "hotfix/" or "chore/" + ticket (UPPERCASE letters, dash, digits) + dash + kebab-case slug,
     *       e.g. feature/PAY-123-add-idempotency-key (slug: lower-case letters/digits separated by single dashes)</li>
     *   <li>"release/" + major.minor.patch, e.g. release/1.4.0</li>
     * </ul>
     */
    public static boolean isValidBranchName(String name) {
        // TODO(Day49-task04): implement with one or more regular expressions
        throw new UnsupportedOperationException("TODO(Day49-task04): implement isValidBranchName");
    }

    /**
     * Conventional Commits: first line "type(scope)!: subject" where type is one of feat, fix, docs, refactor, test,
     * chore, build, ci; (scope) optional lower-case kebab; "!" optional; subject 1..72 chars, not blank.
     * Only the FIRST line is validated. null/blank -> false.
     */
    public static boolean isValidCommitMessage(String message) {
        // TODO(Day49-task04): validate the first line
        throw new UnsupportedOperationException("TODO(Day49-task04): implement isValidCommitMessage");
    }

    /**
     * Semantic version bump. bump is "major", "minor" or "patch" (case-insensitive).
     * major: X+1.0.0, minor: X.Y+1.0, patch: X.Y.Z+1. Invalid version/bump -> IllegalArgumentException.
     */
    public static String nextVersion(String current, String bump) {
        // TODO(Day49-task04): parse MAJOR.MINOR.PATCH and apply the bump
        throw new UnsupportedOperationException("TODO(Day49-task04): implement nextVersion");
    }
}
