# Project 01 - StayEasy Hotel Booking API

A REST backend for a hotel booking platform: guests search hotels and rooms by city, dates and capacity and book rooms;
managers maintain their hotels; admins oversee everything. You design and implement the service on top of the provided
**Spring Boot skeleton** and **PostgreSQL schema**.

| | |
|---|---|
| Stack | Java 21, Spring Boot 3.4.x (course target: Boot 4), Spring Data JPA, PostgreSQL 17, Maven |
| Package | `com.javaprep.stayeasy` |
| Port | `8080` |
| Database | `stayeasy` on `localhost:5432` (JDBC URL `jdbc:postgresql://localhost:5432/stayeasy`) |

Documents in this folder: [`PROJECT_INSTRUCTIONS.md`](PROJECT_INSTRUCTIONS.md) (milestones, API contract, stories, security) ·
[`DATA_MODEL.md`](DATA_MODEL.md) (ER diagram, availability rules) · [`GRADING_CRITERIA.md`](GRADING_CRITERIA.md) ·
[`database/DATABASE_SETUP.md`](database/DATABASE_SETUP.md).

## Prerequisites

- JDK 21 and Maven 3.9+ (`setup/JAVA_AND_MAVEN_SETUP.md`)
- PostgreSQL 17 with `psql` (`setup/POSTGRESQL_SETUP.md`)
- Days 1-50 completed, especially JPA (25-35), REST (31-33), Security (37-38), testing (40, 48)

## Quick start

```bash
cd "Project 01 - StayEasy Hotel Booking API"

# 1. database (details + Windows steps: database/DATABASE_SETUP.md)
psql -d postgres -f database/00_create_database.sql
psql -U course_user -h localhost -d stayeasy -f database/01_schema.sql
psql -U course_user -h localhost -d stayeasy -f database/02_seed_data.sql

# 2. connection settings (see the CRITICAL section below)
cp backend/src/main/resources/application-local.yml.example backend/src/main/resources/application-local.yml

# 3. run
cd backend
mvn spring-boot:run -Dspring-boot.run.profiles=local
curl http://localhost:8080/            # {"application":"StayEasy Hotel Booking API","status":"UP",...}
curl http://localhost:8080/actuator/health

# 4. tests (no PostgreSQL needed: they use in-memory H2)
mvn test
```

## CRITICAL: database connection (`application-local.yml`)

The application **will not start** until it knows how to reach PostgreSQL. `backend/src/main/resources/application.yml`
deliberately contains **no credentials**; it reads them from placeholders:

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
```

Choose ONE of the following ways to supply the values.

### Option A (recommended): `application-local.yml`

1. Copy the template:
   - macOS/Linux: `cp backend/src/main/resources/application-local.yml.example backend/src/main/resources/application-local.yml`
   - Windows PowerShell: `Copy-Item backend\src\main\resources\application-local.yml.example backend\src\main\resources\application-local.yml`
2. Edit it with your values:
   ```yaml
   spring:
     datasource:
       url: jdbc:postgresql://localhost:5432/stayeasy
       username: course_user
       password: change_me          # the password you set for course_user
   ```
3. Start with the `local` profile: `mvn spring-boot:run -Dspring-boot.run.profiles=local`
   (IntelliJ: Run configuration -> *Active profiles* = `local`).
4. `application-local.yml` is **git-ignored**. Run `git status` and confirm it is not listed. **Never commit it.**

### Option B: environment variables

```bash
# macOS / Linux
export DB_URL=jdbc:postgresql://localhost:5432/stayeasy DB_USERNAME=course_user DB_PASSWORD=change_me
mvn spring-boot:run
```
```powershell
# Windows PowerShell (current session)
$env:DB_URL="jdbc:postgresql://localhost:5432/stayeasy"; $env:DB_USERNAME="course_user"; $env:DB_PASSWORD="change_me"
mvn spring-boot:run
```

### Common connection errors

| Error | Meaning |
|-------|---------|
| `Could not resolve placeholder 'DB_URL'` | Neither profile `local` nor the environment variables are set |
| `Connection to localhost:5432 refused` | PostgreSQL is not running (macOS: `brew services start postgresql@17`) |
| `password authentication failed` | Wrong `DB_PASSWORD`/role password |
| `Schema-validation: missing table [...]` | `01_schema.sql` was not run against this database |
| `Schema-validation: wrong column type` | Your entity does not match the SQL schema (the schema is the source of truth) |

## Seed accounts

All seeded passwords are listed here **in plain text for local development only**. The database stores only the BCrypt
hashes (cost 10) that are present in `database/02_seed_data.sql`.

| Email | Role | Plain password | BCrypt hash stored in SQL |
|-------|------|----------------|---------------------------|
| `admin@stayeasy.com` | ADMIN | `Admin@123` | `$2a$10$6Ai9fZGYXWcJcFj2FxED0eBQ5dBwrOgfgQg/1dRO.Cq6F4VT/ku2C` |
| `manager@stayeasy.com` | MANAGER (Seaside Grand, City Central Inn) | `Manager@123` | `$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m` |
| `manager2@stayeasy.com` | MANAGER (Hillview Lodge) | `Manager@123` | `$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m` |
| `guest@stayeasy.com` | GUEST | `Guest@123` | `$2a$10$/lC0I8o7r/LGYFuyJ2z8/edADXBrSE3CwVyeaXeggQxEba501CfNS` |
| `guest2@stayeasy.com` | GUEST | `Guest@123` | `$2a$10$/lC0I8o7r/LGYFuyJ2z8/edADXBrSE3CwVyeaXeggQxEba501CfNS` |

(Each hash was produced with `htpasswd -bnBC 10 "" <password>` and is verified by Spring's `BCryptPasswordEncoder`.)

## Project layout

```
Project 01 - StayEasy Hotel Booking API/
  README.md  PROJECT_INSTRUCTIONS.md  DATA_MODEL.md  GRADING_CRITERIA.md
  database/   00_create_database.sql  01_schema.sql  02_seed_data.sql  03_procedures.sql  99_reset.sql  DATABASE_SETUP.md
  backend/    pom.xml  src/main/java/com/javaprep/stayeasy/...  src/main/resources/application*.yml  src/test/...
```

## Git workflow

Work on a branch such as `student/<id>/project-01`, commit per milestone (`feat(booking): reject overlapping stays`),
open a pull request per milestone, never commit `application-local.yml`, `.env` or `target/`.
