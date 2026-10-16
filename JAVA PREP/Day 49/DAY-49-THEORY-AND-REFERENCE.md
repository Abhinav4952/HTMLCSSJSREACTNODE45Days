# Day 49 — Production Readiness: Profiles, Secrets, JAR, CI, Checkstyle, Git

**Phase:** Capstone  
**Primary theme:** What it takes to ship: externalized configuration, executable JARs, CI pipelines, style gates and disciplined Git workflow  
**Estimated study time:** 2-3 h theory + 4-6 h tasks  
**Related tasks:** `task-01-production-config-check`, `task-02-github-actions-workflow`, `task-03-style-linter`, `task-04-git-conventions-release-checklist`  
**Instruction alignment:** Maps to Day 49 in the 50-day topic map (`course-generation-instructions/04`).  
**Java / Spring versions:** Java 21, Spring Boot 3.4.1 (course target: Spring Boot 4 when available)

> **Note:** Course target is Spring Boot 4 when available; labs pin 3.4.x for reproducible builds. Production APIs shown here are largely identical in Boot 4; differences (starter splitting, Jackson 3) are called out where they matter.

## Overview

What it takes to ship: externalized configuration, executable JARs, CI pipelines, style gates and disciplined Git workflow. This day gives you the mental model first, then makes you prove it with tests. In real backend work these topics decide whether your service is correct, secure, and operable; in interviews they are the topics where shallow answers are exposed quickly.

## Day roadmap

1. Profiles, externalized configuration, and secrets
2. Packaging and running an executable JAR
3. CI with GitHub Actions and code quality with Checkstyle
4. Git branching, pull requests, and release hygiene
5. Interview corner, common mistakes, glossary

## Subtopics

### Profiles, externalized configuration, and secrets

#### What it is

Production behavior comes from configuration, not code. Spring Boot layers sources: defaults < `application.yml` < `application-{profile}.yml` < OS environment variables < command-line args. Secrets (DB password, JWT key) must come from the environment or a secret manager, never from the repository.

#### Why it exists / why it matters

The same JAR runs in dev, test and prod. Committed secrets are leaked secrets (Git history is forever); misconfigured prod (dev profile, weak secrets, `ddl-auto=create`) causes incidents.

#### Pros and cons

**Pros**

- One artifact for all environments
- Secrets rotate without rebuilds
- Fail-fast validation at startup

**Cons / trade-offs**

- More moving parts to document
- Environment drift between machines

#### What happens without it / when misused

A committed `application.yml` with real credentials is a breach; `ddl-auto=update` in prod silently mutates schemas; `management.endpoints.web.exposure.include=*` exposes internals.

#### Syntax and rules

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  jpa.hibernate.ddl-auto: validate
```
Run: `SPRING_PROFILES_ACTIVE=prod DB_URL=... java -jar app.jar`. Local only: `application-local.yml` (git-ignored). See `samples/application-prod.yml`.

#### Examples

**Example 1 — Fail fast**

```java
if (!problems.isEmpty()) throw new IllegalStateException("Bad configuration: " + problems);
```

**Example 2 — Env var mapping**

```text
app.jwt.secret  <-  APP_JWT_SECRET (relaxed binding)
```

#### Quick checks

1. Where do production secrets live?
2. Why `ddl-auto=validate` in prod?

### Packaging and running an executable JAR

#### What it is

`spring-boot-maven-plugin` repackages the app into a **fat (executable) JAR** containing dependencies and an embedded server: `mvn -DskipTests package` then `java -jar target/app-1.0.0.jar`. Useful flags: `-Xmx`, `-Dspring.profiles.active=prod`, `--server.port=9090`; graceful shutdown with `server.shutdown=graceful`.

#### Why it exists / why it matters

A single self-contained artifact is simple to deploy, version and roll back. Operations need health endpoints, logs on stdout, and predictable shutdown.

#### Pros and cons

**Pros**

- No external app server
- Reproducible builds
- Easy containerless deployment (systemd, VM)

**Cons / trade-offs**

- Big artifacts
- Dependencies are updated only by rebuilding

#### What happens without it / when misused

Running with the IDE classpath instead of the JAR hides packaging bugs (missing resources); logging to a local file on ephemeral hosts loses logs.

#### Syntax and rules

```bash
mvn -B clean verify
java -jar target/payflow-1.0.0.jar --spring.profiles.active=prod
curl -s localhost:8080/actuator/health
```
Stop with SIGTERM (graceful shutdown completes in-flight requests).

#### Examples

**Example 1 — Memory and profile**

```bash
JAVA_OPTS="-Xms256m -Xmx512m"
java $JAVA_OPTS -jar app.jar --spring.profiles.active=prod
```

#### Quick checks

1. What does repackage do?
2. How do you stop it cleanly?

### CI with GitHub Actions and code quality with Checkstyle

#### What it is

A **workflow** (`.github/workflows/*.yml`) runs jobs on events (`push`, `pull_request`). A Java job: checkout -> setup-java (Temurin 21, Maven cache) -> `mvn -B verify`. **Checkstyle** enforces style rules via `maven-checkstyle-plugin` bound to `validate`/`verify`.

#### Why it exists / why it matters

Automation makes quality non-negotiable: every pull request builds, tests and lints before review, so humans review design not whitespace.

#### Pros and cons

**Pros**

- Fast feedback on every PR
- Consistent style
- Reproducible clean-room build

**Cons / trade-offs**

- CI minutes cost; flaky tests erode trust
- Strict rules need team agreement

#### What happens without it / when misused

Without CI, 'works on my machine' merges break main. Without a style gate, reviews become style debates.

#### Syntax and rules

See `samples/github-actions-ci.yml` and `samples/checkstyle.xml`.
```xml
<plugin>
  <artifactId>maven-checkstyle-plugin</artifactId>
  <configuration><configLocation>checkstyle.xml</configLocation><failOnViolation>true</failOnViolation></configuration>
  <executions><execution><phase>validate</phase><goals><goal>check</goal></goals></execution></executions>
</plugin>
```

#### Examples

**Example 1 — Minimal workflow**

```yaml
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21', cache: maven }
      - run: mvn -B verify
```

#### Quick checks

1. Why cache Maven dependencies?
2. Where do CI secrets go?

### Git branching, pull requests, and release hygiene

#### What it is

Common models: **trunk-based** (short-lived branches off `main`, small PRs, feature flags) and **GitFlow** (`develop`, `release/*`, `hotfix/*`). Good PRs are small, linked to a ticket, have a clear description and pass CI. Use **Conventional Commits** and **semantic versioning** for readable history and releases.

#### Why it exists / why it matters

Predictable branching and history make code review, bisecting and releases safe.

#### Pros and cons

**Pros**

- Easier reviews and reverts
- Automatable release notes
- Clear versioning contract

**Cons / trade-offs**

- Process overhead
- Long-lived branches cause painful merges

#### What happens without it / when misused

Giant PRs get rubber-stamped; force-pushing shared branches destroys teammates' work; committing secrets requires a history rewrite and key rotation.

#### Syntax and rules

Branch: `feature/PAY-123-add-idempotency-key`. Commit: `feat(payments): add idempotency key`. Release: tag `v1.4.0` from `release/1.4.0`. Release checklist: tests green, migration reviewed, config documented, changelog, tag, rollback plan.

#### Examples

**Example 1 — Semver**

```text
MAJOR (breaking) . MINOR (feature) . PATCH (fix)  e.g. 1.4.9 -> 1.5.0 for a new feature
```

#### Quick checks

1. Rebase or merge?
2. What do you do after committing a secret?

## Interview corner

**Q1. What is a twelve-factor config?**

Config in environment variables, strictly separated from code.

**Q2. How do you roll back a bad release?**

Redeploy the previous immutable artifact (and compatible schema).

**Q3. Why avoid long-lived branches?**

They diverge and cause integration pain; prefer short-lived branches and small PRs.

**Q4. What does `mvn -B verify` do?**

Runs compile, test and package checks in batch (non-interactive) mode.

**Q5. What belongs in CI?**

Build, tests, static analysis, dependency checks; deploy on tagged releases.

## Common mistakes & debugging

- Committing secrets or `application-local.yml`.
- Using `ddl-auto=update` in prod.
- Running prod with the dev profile.
- Not caching dependencies in CI.
- Force-pushing shared branches.

## Further reading

- Spring Boot Reference: Externalized Configuration, Packaging
- GitHub Actions documentation: Building and testing Java with Maven
- Checkstyle documentation
- Conventional Commits 1.0
- Semantic Versioning 2.0

## Glossary

| Term | Meaning |
|------|---------|
| Profile | Named configuration group |
| Fat JAR | Executable JAR with dependencies |
| Workflow | GitHub Actions automation file |
| Checkstyle | Style checking tool |
| Trunk-based | Integrate small changes to main frequently |
| Semver | Major.Minor.Patch versioning |

## Answers

### Profiles, externalized configuration, and secrets

1. Environment variables injected by the platform or a secret manager (Vault, cloud secrets).
2. Schema changes must be explicit migrations; Hibernate should only verify.

### Packaging and running an executable JAR

1. Creates a nested-JAR executable archive with a launcher and the app's dependencies.
2. Send SIGTERM; with graceful shutdown in-flight requests complete.

### CI with GitHub Actions and code quality with Checkstyle

1. To avoid re-downloading them on every run.
2. GitHub repository/environment secrets, referenced as `${{ secrets.NAME }}`.

### Git branching, pull requests, and release hygiene

1. Rebase keeps history linear on private branches; merge/squash for shared integration per team policy; never rebase shared history.
2. Rotate it immediately; removing it from Git history alone is not enough.
