package com.javaprep.day49.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import org.junit.jupiter.api.Test;

class GitConventionsTest {

    @Test
    void validBranchNames() {
        assertThat(GitConventions.isValidBranchName("main")).isTrue();
        assertThat(GitConventions.isValidBranchName("develop")).isTrue();
        assertThat(GitConventions.isValidBranchName("feature/PAY-123-add-idempotency-key")).isTrue();
        assertThat(GitConventions.isValidBranchName("hotfix/OPS-9-fix")).isTrue();
        assertThat(GitConventions.isValidBranchName("release/1.4.0")).isTrue();
    }

    @Test
    void invalidBranchNames() {
        assertThat(GitConventions.isValidBranchName(null)).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/add-stuff")).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/pay-1-x")).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/PAY-1-Bad_Slug")).isFalse();
        assertThat(GitConventions.isValidBranchName("feature/PAY-1-double--dash")).isFalse();
        assertThat(GitConventions.isValidBranchName("release/1.4")).isFalse();
        assertThat(GitConventions.isValidBranchName("my-branch")).isFalse();
    }

    @Test
    void validCommitMessages() {
        assertThat(GitConventions.isValidCommitMessage("feat: add login")).isTrue();
        assertThat(GitConventions.isValidCommitMessage("fix(auth): reject expired tokens")).isTrue();
        assertThat(GitConventions.isValidCommitMessage("refactor(user-service)!: drop v1 api\n\nBody text here")).isTrue();
    }

    @Test
    void invalidCommitMessages() {
        assertThat(GitConventions.isValidCommitMessage(null)).isFalse();
        assertThat(GitConventions.isValidCommitMessage("  ")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("added stuff")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("feat:no space")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("wip: something")).isFalse();
        assertThat(GitConventions.isValidCommitMessage("feat: " + "x".repeat(73))).isFalse();
        assertThat(GitConventions.isValidCommitMessage("feat(Auth): upper scope")).isFalse();
    }

    @Test
    void versionBumps() {
        assertThat(GitConventions.nextVersion("1.4.9", "patch")).isEqualTo("1.4.10");
        assertThat(GitConventions.nextVersion("1.4.9", "MINOR")).isEqualTo("1.5.0");
        assertThat(GitConventions.nextVersion("1.4.9", "major")).isEqualTo("2.0.0");
    }

    @Test
    void invalidVersionInputs() {
        assertThatThrownBy(() -> GitConventions.nextVersion("1.4", "patch")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GitConventions.nextVersion("a.b.c", "patch")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GitConventions.nextVersion("1.0.0", "huge")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GitConventions.nextVersion(null, "patch")).isInstanceOf(IllegalArgumentException.class);
    }
}
