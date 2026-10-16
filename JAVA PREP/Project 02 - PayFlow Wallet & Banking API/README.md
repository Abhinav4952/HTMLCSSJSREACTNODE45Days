# Project 02 - PayFlow Wallet & Banking API

A wallet/banking backend: customers hold accounts, deposit and withdraw money and transfer between accounts safely. The focus is
**correctness under concurrency and retries**: transactions, optimistic locking (`@Version`), an append-only ledger and
idempotency keys.

| | |
|---|---|
| Stack | Java 21, Spring Boot 3.4.x (course target: Boot 4), Spring Data JPA, PostgreSQL 17, Maven |
| Package | `com.javaprep.payflow` |
| Port | `8080` |
| Database | `payflow` on `localhost:5432` (JDBC URL `jdbc:postgresql://localhost:5432/payflow`) |

Documents: [`PROJECT_INSTRUCTIONS.md`](PROJECT_INSTRUCTIONS.md) · [`DATA_MODEL.md`](DATA_MODEL.md) · [`GRADING_CRITERIA.md`](GRADING_CRITERIA.md) · [`database/DATABASE_SETUP.md`](database/DATABASE_SETUP.md)

## Prerequisites

JDK 21, Maven 3.9+, PostgreSQL 17 with `psql`; Days 25-27 (transactions), 35-40 (JPA/Security), 46 (idempotency/outbox), 47-48 (capstone).

## Quick start

```bash
cd "Project 02 - PayFlow Wallet & Banking API"

psql -d postgres -f database/00_create_database.sql
psql -U course_user -h localhost -d payflow -f database/01_schema.sql
psql -U course_user -h localhost -d payflow -f database/02_seed_data.sql
psql -U course_user -h localhost -d payflow -f database/03_procedures.sql

cp backend/src/main/resources/application-local.yml.example backend/src/main/resources/application-local.yml
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=local
curl http://localhost:8080/
mvn test        # H2, no PostgreSQL required
```

## CRITICAL: database connection (`application-local.yml`)

`backend/src/main/resources/application.yml` contains placeholders only:

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
```

### Option A (recommended): `application-local.yml`

1. Copy the template
   - macOS/Linux: `cp backend/src/main/resources/application-local.yml.example backend/src/main/resources/application-local.yml`
   - Windows: `Copy-Item backend\src\main\resources\application-local.yml.example backend\src\main\resources\application-local.yml`
2. Fill in your values:
   ```yaml
   spring:
     datasource:
       url: jdbc:postgresql://localhost:5432/payflow
       username: course_user
       password: change_me
   ```
3. Run with the `local` profile: `mvn spring-boot:run -Dspring-boot.run.profiles=local` (IntelliJ: *Active profiles* = `local`).
4. The file is **git-ignored** - confirm with `git status` and **never commit it**.

### Option B: environment variables

```bash
export DB_URL=jdbc:postgresql://localhost:5432/payflow DB_USERNAME=course_user DB_PASSWORD=change_me   # macOS/Linux
```
```powershell
$env:DB_URL="jdbc:postgresql://localhost:5432/payflow"; $env:DB_USERNAME="course_user"; $env:DB_PASSWORD="change_me"   # Windows
```

| Error | Meaning |
|-------|---------|
| `Could not resolve placeholder 'DB_URL'` | No `local` profile and no environment variables |
| `Connection refused` | PostgreSQL not running |
| `password authentication failed` | Wrong password |
| `Schema-validation: missing table` | SQL scripts not applied to this database |

## Seed accounts

Plain-text passwords below are for **local development only**; the SQL stores the BCrypt hashes (cost 10).

| Email | Role | Plain password | BCrypt hash stored in SQL |
|-------|------|----------------|---------------------------|
| `admin@payflow.com` | ADMIN | `Admin@123` | `$2a$10$6Ai9fZGYXWcJcFj2FxED0eBQ5dBwrOgfgQg/1dRO.Cq6F4VT/ku2C` |
| `alice@payflow.com` | CUSTOMER (accounts 1 and 3) | `Alice@123` | `$2a$10$E1CeAbXchPDULuJ31jx1.OUSr7ffnPs0arczbvZc8ZbGU7qCUZkOG` |
| `bob@payflow.com` | CUSTOMER (accounts 2 and 4 - frozen) | `Bob@123` | `$2a$10$OfLP3.Q9SjzEDOi5GU4wFeSE.0KkVV.WyJutnnTcKa8UCOFjiEimC` |

Seed balances: account 1 = 1300.00, account 2 = 500.00, account 3 = 2000.00, account 4 = 0.00 (FROZEN), all USD.

## Layout

```
Project 02 - PayFlow Wallet & Banking API/
  README.md  PROJECT_INSTRUCTIONS.md  DATA_MODEL.md  GRADING_CRITERIA.md
  database/  00_create_database.sql  01_schema.sql  02_seed_data.sql  03_procedures.sql (fn_monthly_statement)  99_reset.sql  DATABASE_SETUP.md
  backend/   Spring Boot skeleton (see PROJECT_INSTRUCTIONS.md for the package plan)
```
