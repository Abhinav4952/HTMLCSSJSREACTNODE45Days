"""Project 01 - StayEasy Hotel Booking API."""
from pathlib import Path

from skeleton import sub, write, write_service

NAME = "Project 01 - StayEasy Hotel Booking API"
DB = "stayeasy"

PW = {
    "admin": ("admin@stayeasy.com", "Admin@123", "$2a$10$6Ai9fZGYXWcJcFj2FxED0eBQ5dBwrOgfgQg/1dRO.Cq6F4VT/ku2C"),
    "manager": ("manager@stayeasy.com", "Manager@123", "$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m"),
    "guest": ("guest@stayeasy.com", "Guest@123", "$2a$10$/lC0I8o7r/LGYFuyJ2z8/edADXBrSE3CwVyeaXeggQxEba501CfNS"),
}

CREATE_DB = """-- 00_create_database.sql
-- Run as a PostgreSQL superuser (usually `postgres`), connected to the default `postgres` database:
--   psql -U postgres -f database/00_create_database.sql
-- Safe to run more than once.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'course_user') THEN
        CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
    END IF;
END
$$;

-- CREATE DATABASE cannot run inside a DO block; \\gexec runs the generated statement only when needed (psql feature).
SELECT 'CREATE DATABASE stayeasy OWNER course_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'stayeasy')\\gexec

GRANT ALL PRIVILEGES ON DATABASE stayeasy TO course_user;
"""

SCHEMA = """-- 01_schema.sql  (PostgreSQL 17)
-- Run connected to the stayeasy database:
--   psql -U course_user -d stayeasy -f database/01_schema.sql
-- The schema is OWNED by these scripts. The Spring Boot app runs with spring.jpa.hibernate.ddl-auto=validate.

-- btree_gist lets the exclusion constraint below combine "room_id =" with a date-range overlap (&&).
-- It is a "trusted" extension in PostgreSQL 13+, so the database owner can create it.
CREATE EXTENSION IF NOT EXISTS btree_gist;

CREATE TABLE users (
    id            BIGSERIAL PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL,                 -- BCrypt hash, never the plain password
    full_name     VARCHAR(120) NOT NULL,
    role          VARCHAR(10)  NOT NULL CHECK (role IN ('GUEST', 'MANAGER', 'ADMIN')),
    enabled       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT now()
);

CREATE TABLE hotels (
    id          BIGSERIAL PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    city        VARCHAR(100) NOT NULL,
    country     VARCHAR(100) NOT NULL,
    address     VARCHAR(255) NOT NULL,
    star_rating SMALLINT     NOT NULL CHECK (star_rating BETWEEN 1 AND 5),
    description TEXT,
    manager_id  BIGINT       NOT NULL REFERENCES users (id),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT uq_hotel_name_city UNIQUE (name, city)
);

CREATE TABLE rooms (
    id              BIGSERIAL PRIMARY KEY,
    hotel_id        BIGINT         NOT NULL REFERENCES hotels (id) ON DELETE CASCADE,
    room_number     VARCHAR(10)    NOT NULL,
    room_type       VARCHAR(10)    NOT NULL CHECK (room_type IN ('SINGLE', 'DOUBLE', 'SUITE')),
    capacity        SMALLINT       NOT NULL CHECK (capacity > 0),
    price_per_night NUMERIC(10, 2) NOT NULL CHECK (price_per_night > 0),
    active          BOOLEAN        NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_room_number_per_hotel UNIQUE (hotel_id, room_number)
);

CREATE TABLE bookings (
    id          BIGSERIAL PRIMARY KEY,
    room_id     BIGINT         NOT NULL REFERENCES rooms (id),
    guest_id    BIGINT         NOT NULL REFERENCES users (id),
    check_in    DATE           NOT NULL,
    check_out   DATE           NOT NULL,
    guests      SMALLINT       NOT NULL CHECK (guests > 0),
    total_price NUMERIC(12, 2) NOT NULL CHECK (total_price >= 0),
    status      VARCHAR(10)    NOT NULL CHECK (status IN ('PENDING', 'CONFIRMED', 'CANCELLED', 'COMPLETED')),
    created_at  TIMESTAMPTZ    NOT NULL DEFAULT now(),
    CONSTRAINT chk_stay_dates CHECK (check_out > check_in),
    -- The database itself refuses double bookings: no two ACTIVE bookings of the same room may overlap.
    -- Date ranges are half-open [check_in, check_out): a guest may check in on the day another one checks out.
    CONSTRAINT excl_no_overlapping_bookings
        EXCLUDE USING gist (room_id WITH =, daterange(check_in, check_out, '[)') WITH &&)
        WHERE (status IN ('PENDING', 'CONFIRMED'))
);

CREATE INDEX idx_hotels_city        ON hotels (city);
CREATE INDEX idx_hotels_manager     ON hotels (manager_id);
CREATE INDEX idx_rooms_hotel        ON rooms (hotel_id);
CREATE INDEX idx_bookings_guest     ON bookings (guest_id);
CREATE INDEX idx_bookings_room_dates ON bookings (room_id, check_in, check_out);
"""

SEED = """-- 02_seed_data.sql
-- Demo data. Run after 01_schema.sql:  psql -U course_user -d stayeasy -f database/02_seed_data.sql
--
-- Seed accounts (plain-text passwords are documented in README.md; the database stores only the BCrypt hashes):
--   admin@stayeasy.com    / Admin@123
--   manager@stayeasy.com  / Manager@123
--   manager2@stayeasy.com / Manager@123
--   guest@stayeasy.com    / Guest@123
--   guest2@stayeasy.com   / Guest@123

INSERT INTO users (id, email, password_hash, full_name, role) VALUES
 (1, 'admin@stayeasy.com',    '@@ADMIN@@', 'Ada Admin',      'ADMIN'),
 (2, 'manager@stayeasy.com',  '@@MANAGER@@', 'Mia Manager',    'MANAGER'),
 (3, 'manager2@stayeasy.com', '@@MANAGER@@', 'Marco Manager',  'MANAGER'),
 (4, 'guest@stayeasy.com',    '@@GUEST@@', 'Gina Guest',     'GUEST'),
 (5, 'guest2@stayeasy.com',   '@@GUEST@@', 'Gus Guest',      'GUEST');

INSERT INTO hotels (id, name, city, country, address, star_rating, description, manager_id) VALUES
 (1, 'Seaside Grand',   'Goa',       'India', '12 Beach Road',        5, 'Beachfront resort with pool and spa.', 2),
 (2, 'City Central Inn', 'Bengaluru', 'India', '45 MG Road',           3, 'Business hotel next to the metro.',   2),
 (3, 'Hillview Lodge',  'Manali',    'India', '8 Mall Road',          4, 'Mountain lodge with valley views.',   3);

INSERT INTO rooms (id, hotel_id, room_number, room_type, capacity, price_per_night) VALUES
 (1, 1, '101', 'SINGLE', 1, 4500.00),
 (2, 1, '102', 'DOUBLE', 2, 6500.00),
 (3, 1, '201', 'SUITE',  4, 12000.00),
 (4, 2, '101', 'SINGLE', 1, 2200.00),
 (5, 2, '102', 'DOUBLE', 2, 3200.00),
 (6, 2, '103', 'DOUBLE', 3, 3600.00),
 (7, 3, '1',   'DOUBLE', 2, 5200.00),
 (8, 3, '2',   'SUITE',  5, 9800.00);

-- Bookings relative to today so the demo data never goes stale. Room 2 has two back-to-back stays
-- (check-out day of the first = check-in day of the second, which is allowed).
INSERT INTO bookings (room_id, guest_id, check_in, check_out, guests, total_price, status) VALUES
 (2, 4, CURRENT_DATE + 5,  CURRENT_DATE + 8,  2, 19500.00, 'CONFIRMED'),
 (2, 5, CURRENT_DATE + 8,  CURRENT_DATE + 10, 2, 13000.00, 'CONFIRMED'),
 (3, 4, CURRENT_DATE + 20, CURRENT_DATE + 23, 3, 36000.00, 'PENDING'),
 (5, 5, CURRENT_DATE - 10, CURRENT_DATE - 7,  2,  9600.00, 'COMPLETED'),
 (7, 4, CURRENT_DATE + 2,  CURRENT_DATE + 4,  2, 10400.00, 'CANCELLED');

-- Keep the BIGSERIAL sequences ahead of the explicit ids inserted above.
SELECT setval(pg_get_serial_sequence('users', 'id'),  (SELECT MAX(id) FROM users));
SELECT setval(pg_get_serial_sequence('hotels', 'id'), (SELECT MAX(id) FROM hotels));
SELECT setval(pg_get_serial_sequence('rooms', 'id'),  (SELECT MAX(id) FROM rooms));
"""

PROC = """-- 03_procedures.sql  (PLACEHOLDER)
-- Reserved for optional database-side logic. The main implementation lives in Java (service layer); use this file only
-- if your team decides that a rule is better enforced or reported inside PostgreSQL (e.g. occupancy reports).
-- Run after 01_schema.sql:  psql -U course_user -d stayeasy -f database/03_procedures.sql

-- Example helper you may call from a native query: is the room free for [p_check_in, p_check_out) ?
CREATE OR REPLACE FUNCTION fn_is_room_available(p_room_id BIGINT, p_check_in DATE, p_check_out DATE)
RETURNS BOOLEAN
LANGUAGE sql
STABLE
AS $$
    SELECT NOT EXISTS (
        SELECT 1
        FROM bookings b
        WHERE b.room_id = p_room_id
          AND b.status IN ('PENDING', 'CONFIRMED')
          AND daterange(b.check_in, b.check_out, '[)') && daterange(p_check_in, p_check_out, '[)')
    );
$$;

-- TODO (optional stretch): fn_occupancy_report(p_hotel_id BIGINT, p_from DATE, p_to DATE) returning booked nights per room.
"""

RESET = """-- 99_reset.sql
-- DESTRUCTIVE: drops every StayEasy object so you can start over.
--   psql -U course_user -d stayeasy -f database/99_reset.sql
-- Then re-run 01_schema.sql, 02_seed_data.sql and (optionally) 03_procedures.sql.

DROP FUNCTION IF EXISTS fn_is_room_available(BIGINT, DATE, DATE);
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS rooms    CASCADE;
DROP TABLE IF EXISTS hotels   CASCADE;
DROP TABLE IF EXISTS users    CASCADE;
"""

DB_SETUP = """# StayEasy - Database Setup (PostgreSQL 17)

You need PostgreSQL installed and `psql` on your PATH. If not, follow [`../../setup/POSTGRESQL_SETUP.md`](../../setup/POSTGRESQL_SETUP.md) first.

Default connection used everywhere in this project: host `localhost`, port `5432`, database `stayeasy`, user `course_user`, password `change_me` (**change the password for anything but your own laptop**).

JDBC URL format: `jdbc:postgresql://localhost:5432/stayeasy`

## Scripts

| Script | Purpose | Run as |
|--------|---------|--------|
| `00_create_database.sql` | Creates role `course_user` and database `stayeasy` (idempotent) | superuser (`postgres`) |
| `01_schema.sql` | Tables, constraints, indexes (incl. the no-overlap exclusion constraint) | `course_user` |
| `02_seed_data.sql` | Demo users, hotels, rooms, bookings | `course_user` |
| `03_procedures.sql` | Optional helper function (placeholder for your own SQL) | `course_user` |
| `99_reset.sql` | Drops everything (destructive) | `course_user` |

## macOS (Homebrew PostgreSQL)

```bash
# 1. start the server if needed
brew services start postgresql@17

# 2. from the project folder
cd "Project 01 - StayEasy Hotel Booking API"

# 3. create role + database (Homebrew's superuser is usually YOUR macOS username, not "postgres")
psql -d postgres -f database/00_create_database.sql

# 4. schema + seed data
psql -U course_user -h localhost -d stayeasy -f database/01_schema.sql
psql -U course_user -h localhost -d stayeasy -f database/02_seed_data.sql
psql -U course_user -h localhost -d stayeasy -f database/03_procedures.sql

# 5. verify
psql -U course_user -h localhost -d stayeasy -c "SELECT email, role FROM users ORDER BY id;"
```

If `psql` is not found: `echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`.

## Windows (PowerShell)

```powershell
# 1. make sure the PostgreSQL service is running (Services app -> postgresql-x64-17) and psql is on PATH:
#    C:\\Program Files\\PostgreSQL\\17\\bin

cd "Project 01 - StayEasy Hotel Booking API"

# 2. create role + database (enter the password you chose for "postgres" during installation)
psql -U postgres -h localhost -d postgres -f database\\00_create_database.sql

# 3. schema + seed data (password: change_me)
psql -U course_user -h localhost -d stayeasy -f database\\01_schema.sql
psql -U course_user -h localhost -d stayeasy -f database\\02_seed_data.sql
psql -U course_user -h localhost -d stayeasy -f database\\03_procedures.sql

# 4. verify
psql -U course_user -h localhost -d stayeasy -c "SELECT email, role FROM users ORDER BY id;"
```

## Starting over

```bash
psql -U course_user -h localhost -d stayeasy -f database/99_reset.sql
psql -U course_user -h localhost -d stayeasy -f database/01_schema.sql
psql -U course_user -h localhost -d stayeasy -f database/02_seed_data.sql
```

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `psql: command not found` | Add the PostgreSQL `bin` folder to PATH (see above) |
| `FATAL: password authentication failed for user "course_user"` | Wrong password; reset with `ALTER ROLE course_user PASSWORD 'change_me';` as superuser |
| `ERROR: permission denied to create extension "btree_gist"` | Run `CREATE EXTENSION btree_gist;` once as superuser inside the `stayeasy` database (`psql -U postgres -d stayeasy`) |
| `database "stayeasy" does not exist` | Run `00_create_database.sql` first |
| `\\gexec` error in step 00 | You ran it with a tool other than `psql` (e.g. a GUI); create the database manually: `CREATE DATABASE stayeasy OWNER course_user;` |
| Spring Boot: `Schema-validation: missing table` | The SQL scripts were not applied to the database named in `DB_URL` |
"""

DATA_MODEL = """# StayEasy - Data Model

## Entity-relationship diagram

```mermaid
erDiagram
    USERS ||--o{ HOTELS : "manages (manager_id)"
    USERS ||--o{ BOOKINGS : "books (guest_id)"
    HOTELS ||--|{ ROOMS : "has"
    ROOMS ||--o{ BOOKINGS : "is reserved by"

    USERS {
        bigint id PK
        varchar email UK
        varchar password_hash
        varchar full_name
        varchar role "GUEST | MANAGER | ADMIN"
        boolean enabled
        timestamptz created_at
    }
    HOTELS {
        bigint id PK
        varchar name
        varchar city
        varchar country
        varchar address
        smallint star_rating "1..5"
        text description
        bigint manager_id FK
        timestamptz created_at
    }
    ROOMS {
        bigint id PK
        bigint hotel_id FK
        varchar room_number "unique per hotel"
        varchar room_type "SINGLE | DOUBLE | SUITE"
        smallint capacity
        numeric price_per_night
        boolean active
    }
    BOOKINGS {
        bigint id PK
        bigint room_id FK
        bigint guest_id FK
        date check_in
        date check_out "exclusive end, > check_in"
        smallint guests
        numeric total_price
        varchar status "PENDING | CONFIRMED | CANCELLED | COMPLETED"
        timestamptz created_at
    }
```

## Roles

| Role | May do |
|------|--------|
| `GUEST` | Register/login, search hotels and rooms, create/cancel **own** bookings, view own bookings |
| `MANAGER` | Everything a guest may + create/update hotels and rooms **they manage**, view bookings of their hotels |
| `ADMIN` | Everything, including managing users and any hotel/booking |

## Availability and the date-overlap rule

Stays are **half-open date ranges** `[check_in, check_out)`: the night of `check_out` is *not* occupied. Two stays of the same room overlap when

```
existing.check_in < requested.check_out  AND  requested.check_in < existing.check_out
```

Only bookings in status `PENDING` or `CONFIRMED` block a room. `CANCELLED` and `COMPLETED` do not.

```mermaid
gantt
    title Room 102 - allowed back-to-back stays (check-out day = next check-in day)
    dateFormat  YYYY-MM-DD
    section Room 102
    Guest A (nights 5-7)  :a1, 2025-03-05, 3d
    Guest B (nights 8-9)  :a2, 2025-03-08, 2d
```

### Query used by the search endpoint (rooms of a hotel that are free)

```sql
SELECT r.*
FROM rooms r
WHERE r.hotel_id = :hotelId
  AND r.active
  AND r.capacity >= :guests
  AND NOT EXISTS (
      SELECT 1 FROM bookings b
      WHERE b.room_id = r.id
        AND b.status IN ('PENDING', 'CONFIRMED')
        AND b.check_in < :checkOut
        AND :checkIn < b.check_out);
```

### Two layers of protection

1. **Service layer**: check availability and compute `total_price = nights * price_per_night` inside one `@Transactional` method; answer **409 Conflict** when the room is taken.
2. **Database**: the exclusion constraint `excl_no_overlapping_bookings` rejects a conflicting insert even when two requests race. Map the resulting `DataIntegrityViolationException` to the same 409.

## Status life cycle

```mermaid
stateDiagram-v2
    [*] --> PENDING : guest creates booking
    PENDING --> CONFIRMED : manager confirms
    PENDING --> CANCELLED : guest or manager cancels
    CONFIRMED --> CANCELLED : cancelled before check-in
    CONFIRMED --> COMPLETED : stay finished
    CANCELLED --> [*]
    COMPLETED --> [*]
```
"""

README = """# Project 01 - StayEasy Hotel Booking API

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
   - Windows PowerShell: `Copy-Item backend\\src\\main\\resources\\application-local.yml.example backend\\src\\main\\resources\\application-local.yml`
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
| `admin@stayeasy.com` | ADMIN | `Admin@123` | `@@ADMIN@@` |
| `manager@stayeasy.com` | MANAGER (Seaside Grand, City Central Inn) | `Manager@123` | `@@MANAGER@@` |
| `manager2@stayeasy.com` | MANAGER (Hillview Lodge) | `Manager@123` | `@@MANAGER@@` |
| `guest@stayeasy.com` | GUEST | `Guest@123` | `@@GUEST@@` |
| `guest2@stayeasy.com` | GUEST | `Guest@123` | `@@GUEST@@` |

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
"""

INSTR = """# StayEasy - Project Instructions

## 1. Goal

Build a secure, well-tested REST API for hotel search and booking. The database schema (`database/01_schema.sql`) is
**given and authoritative**: map your JPA entities to it (`ddl-auto=validate`). Everything else is yours to design.

## 2. Rules

- Java 21, Spring Boot (skeleton in `backend/`), PostgreSQL, Maven. No Lombok. No Docker.
- Layered design: controller -> service -> repository; DTOs at the API boundary (never expose entities).
- Passwords: BCrypt. Authentication: JWT bearer tokens (Day 47) **or** HTTP Basic if your instructor allows it.
- Money: `BigDecimal`. Dates: `LocalDate`. Time stamps: UTC.
- All errors use `ProblemDetail` (see `GlobalExceptionHandler`).
- Secrets only via environment/`application-local.yml` (never committed).

## 3. Milestones

Each milestone ends with a green `mvn test`, a pull request and a short demo (curl or Postman) of the new endpoints.

### Milestone A - Foundations and authentication
- Run the database scripts; start the app against PostgreSQL (`/actuator/health` shows `UP`).
- Map `User` to `users`; `POST /api/auth/register` (role forced to `GUEST`), `POST /api/auth/login` returning a JWT.
- Security rules (section 7). Tests: registration validation, duplicate email (409), login success/failure (401).

### Milestone B - Hotels and rooms
- Entities `Hotel`, `Room` with relationships; CRUD for managers/admins; public read endpoints.
- A manager may only modify hotels where `manager_id` equals their user id (policy for strangers: **404**).
- Tests: ownership matrix, validation (rating 1..5, price > 0), unique room number per hotel (409).

### Milestone C - Search and availability
- `GET /api/hotels?city=&minStars=&page=&size=&sort=` (paged, whitelisted sort fields).
- `GET /api/hotels/{id}/rooms/available?checkIn=&checkOut=&guests=` using the date-overlap rule from `DATA_MODEL.md`.
- Tests with seed-like data: back-to-back stays are available, overlapping ones are not, cancelled bookings do not block.

### Milestone D - Bookings
- `POST /api/bookings` (guest): validates dates (`checkOut > checkIn`, check-in not in the past), capacity, availability;
  computes `total_price`; status `PENDING`. Overlap -> **409**.
- `GET /api/bookings/my`, `DELETE /api/bookings/{id}` (cancel own booking before check-in), manager endpoints to confirm/cancel
  bookings of their hotels.
- Concurrency: two simultaneous requests for the same room/dates must produce exactly one booking (database constraint + 409 mapping).

### Milestone E - Hardening and delivery
- Global error contract, pagination everywhere, input validation, no information leaks.
- Test pyramid: unit tests (price/overlap logic), slice tests (`@DataJpaTest`, `@WebMvcTest`), a few `@SpringBootTest` flows.
- Production notes: `prod` profile, env-based secrets, executable JAR, GitHub Actions workflow (Day 49 samples).
- README addendum: how to run, how to obtain a token, example curl calls.

## 4. API contract

All bodies are JSON. `Authorization: Bearer <token>` unless the endpoint is public.

| Method | Path | Role | Description | Success | Errors |
|--------|------|------|-------------|---------|--------|
| POST | `/api/auth/register` | public | Create GUEST account `{email, password(>=8), fullName}` | 201 `UserResponse` | 400, 409 |
| POST | `/api/auth/login` | public | `{email, password}` -> `{token, expiresAt}` | 200 | 400, 401 |
| GET | `/api/hotels` | public | Paged search (`city`, `minStars`, `page`, `size`, `sort`) | 200 `Page` | 400 |
| GET | `/api/hotels/{id}` | public | Hotel details with rooms | 200 | 404 |
| POST | `/api/hotels` | MANAGER, ADMIN | Create hotel (manager = caller; admin may set manager) | 201 | 400, 403, 409 |
| PUT | `/api/hotels/{id}` | owner MANAGER, ADMIN | Update hotel | 200 | 400, 404 |
| POST | `/api/hotels/{id}/rooms` | owner MANAGER, ADMIN | Add room | 201 | 400, 404, 409 |
| PUT | `/api/rooms/{id}` | owner MANAGER, ADMIN | Update room (price, active) | 200 | 400, 404 |
| GET | `/api/hotels/{id}/rooms/available` | public | `checkIn`, `checkOut`, `guests` | 200 list | 400, 404 |
| POST | `/api/bookings` | GUEST | `{roomId, checkIn, checkOut, guests}` | 201 `BookingResponse` | 400, 404, 409 |
| GET | `/api/bookings/my` | GUEST | Own bookings (paged) | 200 | 401 |
| DELETE | `/api/bookings/{id}` | owner GUEST, ADMIN | Cancel before check-in | 204 | 404, 409 |
| GET | `/api/manager/bookings` | MANAGER | Bookings of hotels I manage | 200 | 403 |
| PATCH | `/api/manager/bookings/{id}/confirm` | owner MANAGER, ADMIN | PENDING -> CONFIRMED | 200 | 404, 409 |
| GET | `/api/admin/users` | ADMIN | Paged users | 200 | 403 |

Error body (RFC 9457): `{"status":409,"title":"Conflict","detail":"Room 2 is not available for the selected dates"}`;
validation errors add `"errors": {"field": "message"}`.

## 5. User stories (acceptance criteria)

1. **As a guest** I can register and log in so that I can book rooms. *Duplicate email -> 409; weak password -> 400.*
2. **As a guest** I can search hotels by city and star rating with paging. *Unknown sort field -> 400.*
3. **As a guest** I can see only rooms that are free and large enough for my dates and party. *Back-to-back stays are free.*
4. **As a guest** I can book a free room and see the total price. *Price = nights x nightly rate; overlap -> 409.*
5. **As a guest** I can cancel my booking until the check-in date. *Someone else's booking -> 404.*
6. **As a manager** I can add hotels and rooms and change prices for my hotels only.
7. **As a manager** I can confirm or cancel bookings for my hotels and list them.
8. **As an admin** I can list users and manage any hotel or booking.
9. **As an operator** I can check `/actuator/health` and run the app with only environment variables.

## 6. Business rules

- `checkOut > checkIn`; `checkIn >= today`; maximum stay 30 nights.
- `guests <= room.capacity`; inactive rooms cannot be booked.
- Price is calculated server-side, never trusted from the client.
- Cancelling is allowed for `PENDING`/`CONFIRMED` bookings with `checkIn > today`.
- Deleting a hotel with bookings is not allowed (409).

## 7. Security requirements

| Area | Requirement |
|------|-------------|
| Passwords | BCrypt only; never log or return hashes |
| Authentication | Stateless JWT (HS256, secret from `JWT_SECRET` env, min 32 chars, short expiry, `alg` enforced) |
| Authorization | URL rules: `/api/auth/**` and `GET /api/hotels/**` public; `/api/admin/**` ADMIN; manager endpoints MANAGER/ADMIN; everything else authenticated |
| Object level | Guests touch only their bookings; managers only their hotels (policy: 404 for strangers) |
| Input | Bean Validation on every DTO; whitelist sort fields; clamp page size (<= 50) |
| Errors | No stack traces/SQL in responses; generic 500 message |
| Secrets | `application-local.yml`, `.env` git-ignored; no credentials in code or README (except the documented seed passwords) |
| Transport | Document that production runs behind HTTPS |

## 8. Suggested package layout

```
com.javaprep.stayeasy
  config/      security + jwt configuration
  auth/        controller, service, dto
  hotel/       entity, repository, service, controller, dto
  room/        ...
  booking/     ...
  web/         GlobalExceptionHandler, WelcomeController
```

## 9. Deliverables

Source code, tests, updated README (run instructions + sample requests), a short `DESIGN_NOTES.md` (decisions, trade-offs, what you would improve), pull requests per milestone.
"""

GRADING = """# StayEasy - Grading Criteria (100 points)

| Category | Points | What graders look for |
|----------|-------:|-----------------------|
| Milestone A - Auth and foundations | 12 | App starts against PostgreSQL via `application-local.yml`/env; register + login; BCrypt; JWT |
| Milestone B - Hotels and rooms | 14 | Correct entity mapping (`validate` passes), CRUD, ownership rules |
| Milestone C - Search and availability | 16 | Paged search, correct overlap query, back-to-back and cancelled cases |
| Milestone D - Bookings | 20 | Validation, price calculation, 409 on overlap, DB-level protection, cancel rules, transactions |
| Security | 10 | Rules matrix, object-level checks, no secrets committed, safe errors |
| Testing | 12 | Unit + slice + integration tests, meaningful assertions, `mvn test` green without PostgreSQL |
| Code quality and design | 8 | Layering, DTOs, naming, no duplicated logic, no Lombok |
| Documentation and Git | 8 | README accuracy, sample calls, PR/commit hygiene |

## Automatic deductions

- `application-local.yml`, `.env`, credentials or `target/` committed: **-10**
- `mvn test` fails on a clean checkout: **-15**
- Entities exposed directly in API responses: **-5**
- Price accepted from the client: **-5**
- SQL built by string concatenation: **-10**

## Score bands

| Score | Meaning |
|------:|---------|
| 90-100 | Production-minded: all milestones, concurrency-safe bookings, strong tests |
| 75-89 | Complete and correct with minor gaps |
| 60-74 | Core booking works; weak tests or security gaps |
| < 60 | Missing milestones or unsafe behavior |

## AI grading prompt

```
You are grading Project 01 (StayEasy Hotel Booking API) for a graduate Java backend course. Use only observable evidence:
the repository diff, `mvn test` output and the README. Score out of 100 with the weights in GRADING_CRITERIA.md.
List blocking issues first (secrets committed, failing tests, SQL concatenation). Check: overlap logic is half-open
[check_in, check_out); cancelled bookings do not block; price is server-side; strangers get 404; sort fields are whitelisted.
```
"""


def build(root: Path) -> None:
    base = root / NAME
    kw = dict(ADMIN=PW["admin"][2], MANAGER=PW["manager"][2], GUEST=PW["guest"][2])
    write(base / "README.md", sub(README, **kw))
    write(base / "PROJECT_INSTRUCTIONS.md", INSTR)
    write(base / "DATA_MODEL.md", DATA_MODEL)
    write(base / "GRADING_CRITERIA.md", GRADING)
    db = base / "database"
    write(db / "00_create_database.sql", CREATE_DB)
    write(db / "01_schema.sql", SCHEMA)
    write(db / "02_seed_data.sql", sub(SEED, **kw))
    write(db / "03_procedures.sql", PROC)
    write(db / "99_reset.sql", RESET)
    write(db / "DATABASE_SETUP.md", DB_SETUP)
    write_service(base / "backend", pkg="stayeasy", cls="StayEasy", artifact="stayeasy-backend", title="StayEasy Hotel Booking API",
                  desc="StayEasy hotel booking REST API (course project 01)", appname="stayeasy", db=DB, port=8080)
