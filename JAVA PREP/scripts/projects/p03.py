"""Project 03 - PeopleHub HR Microservices (multi-module Maven)."""
from pathlib import Path

from skeleton import BOOT_VERSION, sub, write, write_service

NAME = "Project 03 - PeopleHub HR Microservices"

H_ADMIN = "$2a$10$AT4q/atqVTOFiepku8soV.IBYYPDcDXl4VMEbIZgbfgu9YciYpc3y"   # HrAdmin@123
H_MGR = "$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m"     # Manager@123
H_EMP = "$2a$10$GVpJM/q6STyj1bpCenjoQ.4jKsjz5F9V9.rz6OKM69PGNkXKHYJ46"     # Employee@123

SERVICES = [
    # folder, db, port, pkg, class, title
    ("employee-service", "peoplehub_employee", 8081, "peoplehub.employee", "Employee", "PeopleHub Employee Service"),
    ("leave-service", "peoplehub_leave", 8082, "peoplehub.leave", "Leave", "PeopleHub Leave Service"),
    ("notification-service", "peoplehub_notification", 8083, "peoplehub.notification", "Notification", "PeopleHub Notification Service"),
]

PARENT_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <!-- Course target is Spring Boot 4 when available; the projects pin 3.4.x for reproducible builds. -->
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>@@BOOT@@</version>
    <relativePath/>
  </parent>

  <groupId>com.javaprep.peoplehub</groupId>
  <artifactId>peoplehub-parent</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <packaging>pom</packaging>
  <name>PeopleHub HR Microservices (parent)</name>

  <modules>
    <module>employee-service</module>
    <module>leave-service</module>
    <module>notification-service</module>
    <module>api-gateway</module>
  </modules>

  <properties>
    <java.version>21</java.version>
    <maven.compiler.release>21</maven.compiler.release>
    <!-- Spring Cloud release train matching Spring Boot 3.4.x (only the gateway module uses it). -->
    <spring-cloud.version>2024.0.0</spring-cloud.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-dependencies</artifactId>
        <version>${spring-cloud.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-surefire-plugin</artifactId>
          <configuration>
            <argLine>-Dnet.bytebuddy.experimental=true</argLine>
          </configuration>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>
</project>
"""

SERVICE_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.javaprep.peoplehub</groupId>
    <artifactId>peoplehub-parent</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <relativePath>../pom.xml</relativePath>
  </parent>
  <artifactId>@@ARTIFACT@@</artifactId>
  <name>@@TITLE@@</name>
  <description>@@TITLE@@ (course project 03)</description>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
@@KAFKA@@    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>com.h2database</groupId>
      <artifactId>h2</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
"""

KAFKA_DEP = """    <dependency>
      <groupId>org.springframework.kafka</groupId>
      <artifactId>spring-kafka</artifactId>
    </dependency>
"""

EVENT_JAVA = """package com.javaprep.peoplehub.@@SHORT@@.events;

import java.time.LocalDate;

/**
 * Contract of the Kafka event "LeaveApproved" (topic leave.approved.v1, key = employeeId). See docs/LEAVE_APPROVED_EVENT.md.
 * Fields may be ADDED in later versions; consumers must ignore unknown fields (tolerant reader).
 */
public record LeaveApprovedEvent(
        int version,
        String eventId,
        long leaveRequestId,
        long employeeId,
        long approverId,
        String leaveType,
        LocalDate startDate,
        LocalDate endDate,
        int days,
        String approvedAt) {
}
"""

GATEWAY_POM = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>com.javaprep.peoplehub</groupId>
    <artifactId>peoplehub-parent</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <relativePath>../pom.xml</relativePath>
  </parent>
  <artifactId>api-gateway</artifactId>
  <name>PeopleHub API Gateway</name>
  <description>Spring Cloud Gateway (reactive) in front of the PeopleHub services</description>
  <dependencies>
    <dependency>
      <groupId>org.springframework.cloud</groupId>
      <artifactId>spring-cloud-starter-gateway</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
"""

GATEWAY_APP = """package com.javaprep.peoplehub.gateway;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class GatewayApplication {

    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }
}
"""

GATEWAY_FILTER = """package com.javaprep.peoplehub.gateway;

import java.util.UUID;
import org.springframework.cloud.gateway.filter.GatewayFilterChain;
import org.springframework.cloud.gateway.filter.GlobalFilter;
import org.springframework.core.Ordered;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

/** Adds an X-Request-Id to every request that does not carry one, so logs of all services can be correlated. */
@Component
public class RequestIdFilter implements GlobalFilter, Ordered {

    public static final String HEADER = "X-Request-Id";

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, GatewayFilterChain chain) {
        if (exchange.getRequest().getHeaders().containsKey(HEADER)) {
            return chain.filter(exchange);
        }
        ServerHttpRequest request = exchange.getRequest().mutate().header(HEADER, UUID.randomUUID().toString()).build();
        return chain.filter(exchange.mutate().request(request).build());
    }

    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE;
    }
}
"""

GATEWAY_YML = """server:
  port: 8080
spring:
  application:
    name: api-gateway
  cloud:
    gateway:
      routes:
        - id: employees
          uri: ${EMPLOYEE_SERVICE_URL:http://localhost:8081}
          predicates:
            - Path=/api/employees/**
        - id: leaves
          uri: ${LEAVE_SERVICE_URL:http://localhost:8082}
          predicates:
            - Path=/api/leaves/**
        - id: notifications
          uri: ${NOTIFICATION_SERVICE_URL:http://localhost:8083}
          predicates:
            - Path=/api/notifications/**
      # TODO (Milestone E): validate the JWT at the edge (global filter) and forward X-User-Id / X-User-Role to the services.
management:
  endpoints:
    web:
      exposure:
        include: health,info,gateway
"""

GATEWAY_TEST = """package com.javaprep.peoplehub.gateway;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.cloud.gateway.route.RouteLocator;

/** Smoke test: the gateway context starts and the three PeopleHub routes are registered. No services need to run. */
@SpringBootTest
class GatewaySmokeTest {

    @Autowired
    private RouteLocator routeLocator;

    @Test
    void routesAreConfigured() {
        var routes = routeLocator.getRoutes().collectList().block();
        assertThat(routes.stream().map(r -> r.getId()).toList()).contains("employees", "leaves", "notifications");
    }
}
"""

# -------------------------------------------------------------------------- SQL
def sql_create(db: str) -> str:
    return f"""-- 00_create_database.sql  ({db})
-- Run as a PostgreSQL superuser connected to the default `postgres` database:
--   psql -U postgres -f database/{db}/00_create_database.sql
-- Safe to run more than once. Each service owns its OWN database - there are no cross-database foreign keys.

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'course_user') THEN
        CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
    END IF;
END
$$;

SELECT 'CREATE DATABASE {db} OWNER course_user'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{db}')\\gexec

GRANT ALL PRIVILEGES ON DATABASE {db} TO course_user;
"""


EMP_SCHEMA = """-- 01_schema.sql (peoplehub_employee)
--   psql -U course_user -d peoplehub_employee -f database/employee-service/01_schema.sql
-- Owner of: departments, employees (and their login credentials / roles).

CREATE TABLE departments (
    id   BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE employees (
    id                BIGSERIAL PRIMARY KEY,
    email             VARCHAR(255) NOT NULL UNIQUE,
    password_hash     VARCHAR(100) NOT NULL,                    -- BCrypt
    full_name         VARCHAR(120) NOT NULL,
    role              VARCHAR(10)  NOT NULL CHECK (role IN ('HR_ADMIN', 'MANAGER', 'EMPLOYEE')),
    department_id     BIGINT       NOT NULL REFERENCES departments (id),
    manager_id        BIGINT       REFERENCES employees (id),   -- self reference: direct manager (NULL for the top)
    hire_date         DATE         NOT NULL,
    status            VARCHAR(10)  NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE', 'ON_LEAVE', 'TERMINATED')),
    annual_leave_days INT          NOT NULL DEFAULT 20 CHECK (annual_leave_days >= 0),
    created_at        TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT chk_not_own_manager CHECK (manager_id IS NULL OR manager_id <> id)
);

CREATE INDEX idx_employees_department ON employees (department_id);
CREATE INDEX idx_employees_manager    ON employees (manager_id);
"""

EMP_SEED = """-- 02_seed_data.sql (peoplehub_employee)
-- Logins (plain passwords are documented in README.md; only BCrypt hashes are stored):
--   hr@peoplehub.com / HrAdmin@123      manager@peoplehub.com / Manager@123
--   alice@peoplehub.com, bob@peoplehub.com, carol@peoplehub.com / Employee@123

INSERT INTO departments (id, name) VALUES (1, 'Human Resources'), (2, 'Engineering'), (3, 'Finance');

INSERT INTO employees (id, email, password_hash, full_name, role, department_id, manager_id, hire_date) VALUES
 (1, 'hr@peoplehub.com',      '@@ADMIN@@', 'Hana Reyes',   'HR_ADMIN', 1, NULL, DATE '2020-01-15'),
 (2, 'manager@peoplehub.com', '@@MGR@@',   'Milo Grant',   'MANAGER',  2, 1,    DATE '2021-03-01'),
 (3, 'alice@peoplehub.com',   '@@EMP@@',   'Alice Walker', 'EMPLOYEE', 2, 2,    DATE '2022-06-20'),
 (4, 'bob@peoplehub.com',     '@@EMP@@',   'Bob Turner',   'EMPLOYEE', 2, 2,    DATE '2023-02-10'),
 (5, 'carol@peoplehub.com',   '@@EMP@@',   'Carol Diaz',   'EMPLOYEE', 3, 1,    DATE '2023-09-05');

SELECT setval(pg_get_serial_sequence('departments', 'id'), (SELECT MAX(id) FROM departments));
SELECT setval(pg_get_serial_sequence('employees', 'id'),   (SELECT MAX(id) FROM employees));
"""

LEAVE_SCHEMA = """-- 01_schema.sql (peoplehub_leave)
--   psql -U course_user -d peoplehub_leave -f database/leave-service/01_schema.sql
-- Owner of: leave requests, yearly balances and the OUTBOX of domain events.
-- employee_id / approver_id are plain BIGINT values referencing employee-service ids: NO foreign key across databases.
-- Validate them through the employee-service API (RestClient) instead.

CREATE TABLE leave_requests (
    id          BIGSERIAL PRIMARY KEY,
    employee_id BIGINT      NOT NULL,
    approver_id BIGINT,
    leave_type  VARCHAR(10) NOT NULL CHECK (leave_type IN ('ANNUAL', 'SICK', 'UNPAID')),
    start_date  DATE        NOT NULL,
    end_date    DATE        NOT NULL,
    days        INT         NOT NULL CHECK (days > 0),
    status      VARCHAR(10) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED')),
    reason      VARCHAR(500),
    decided_at  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_leave_dates CHECK (end_date >= start_date),
    CONSTRAINT chk_decision CHECK ((status IN ('APPROVED', 'REJECTED') AND approver_id IS NOT NULL AND decided_at IS NOT NULL)
                                   OR status IN ('PENDING', 'CANCELLED'))
);

CREATE TABLE leave_balances (
    employee_id BIGINT NOT NULL,
    year        INT    NOT NULL,
    total_days  INT    NOT NULL CHECK (total_days >= 0),
    used_days   INT    NOT NULL DEFAULT 0 CHECK (used_days >= 0),
    PRIMARY KEY (employee_id, year),
    CONSTRAINT chk_used_within_total CHECK (used_days <= total_days)
);

-- Transactional outbox: written in the SAME transaction as the approval, relayed to Kafka by a poller (Day 46).
CREATE TABLE outbox_events (
    id             BIGSERIAL PRIMARY KEY,
    aggregate_type VARCHAR(50)  NOT NULL,
    aggregate_id   VARCHAR(50)  NOT NULL,
    event_type     VARCHAR(50)  NOT NULL,
    topic          VARCHAR(100) NOT NULL,
    event_key      VARCHAR(50)  NOT NULL,
    payload        JSONB        NOT NULL,
    published      BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT now(),
    published_at   TIMESTAMPTZ
);

CREATE INDEX idx_leave_employee          ON leave_requests (employee_id, start_date);
CREATE INDEX idx_leave_status            ON leave_requests (status);
CREATE INDEX idx_outbox_unpublished      ON outbox_events (id) WHERE published = FALSE;
"""

LEAVE_SEED = """-- 02_seed_data.sql (peoplehub_leave)
-- employee ids refer to peoplehub_employee (1 = HR, 2 = manager Milo, 3 = Alice, 4 = Bob, 5 = Carol).

INSERT INTO leave_balances (employee_id, year, total_days, used_days) VALUES
 (2, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 0),
 (3, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 5),
 (4, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 0),
 (5, EXTRACT(YEAR FROM CURRENT_DATE)::int, 20, 0);

INSERT INTO leave_requests (id, employee_id, approver_id, leave_type, start_date, end_date, days, status, reason, decided_at) VALUES
 (1, 3, 2,    'ANNUAL', CURRENT_DATE - 30, CURRENT_DATE - 26, 5, 'APPROVED',  'Family trip',   now() - INTERVAL '35 days'),
 (2, 4, NULL, 'ANNUAL', CURRENT_DATE + 14, CURRENT_DATE + 16, 3, 'PENDING',   'Long weekend',  NULL),
 (3, 5, NULL, 'SICK',   CURRENT_DATE + 1,  CURRENT_DATE + 1,  1, 'PENDING',   'Doctor visit',  NULL),
 (4, 3, 2,    'UNPAID', CURRENT_DATE + 40, CURRENT_DATE + 44, 5, 'REJECTED',  'Sabbatical',    now() - INTERVAL '2 days');

SELECT setval(pg_get_serial_sequence('leave_requests', 'id'), (SELECT MAX(id) FROM leave_requests));

-- The already-approved request 1 has a matching outbox row so you can test your poller immediately.
INSERT INTO outbox_events (aggregate_type, aggregate_id, event_type, topic, event_key, payload, published) VALUES
 ('LeaveRequest', '1', 'LeaveApproved', 'leave.approved.v1', '3',
  '{"version":1,"eventId":"seed-event-0001","leaveRequestId":1,"employeeId":3,"approverId":2,"leaveType":"ANNUAL","days":5}'::jsonb, FALSE);
"""

NOTIF_SCHEMA = """-- 01_schema.sql (peoplehub_notification)
--   psql -U course_user -d peoplehub_notification -f database/notification-service/01_schema.sql
-- Owner of: notifications and the idempotency table of the Kafka consumer.

CREATE TABLE notifications (
    id                    BIGSERIAL PRIMARY KEY,
    recipient_employee_id BIGINT       NOT NULL,                -- id in employee-service (no cross-database FK)
    type                  VARCHAR(30)  NOT NULL,                -- e.g. LEAVE_APPROVED
    message               VARCHAR(500) NOT NULL,
    status                VARCHAR(10)  NOT NULL DEFAULT 'NEW' CHECK (status IN ('NEW', 'SENT', 'READ')),
    source_event_id       VARCHAR(64),
    created_at            TIMESTAMPTZ  NOT NULL DEFAULT now()
);

-- Idempotent consumer: the primary key rejects a second delivery of the same event.
CREATE TABLE processed_events (
    event_id     VARCHAR(64) PRIMARY KEY,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_notifications_recipient ON notifications (recipient_employee_id, created_at DESC);
"""

NOTIF_SEED = """-- 02_seed_data.sql (peoplehub_notification)
INSERT INTO notifications (recipient_employee_id, type, message, status, source_event_id) VALUES
 (3, 'LEAVE_APPROVED', 'Your annual leave request #1 (5 days) was approved by Milo Grant.', 'READ', 'seed-event-0001');
INSERT INTO processed_events (event_id) VALUES ('seed-event-0001');
"""


def reset_sql(db: str, tables: list[str]) -> str:
    drops = "\n".join(f"DROP TABLE IF EXISTS {t} CASCADE;" for t in tables)
    return f"""-- 99_reset.sql ({db})  DESTRUCTIVE
--   psql -U course_user -d {db} -f database/<service>/99_reset.sql
-- Then re-run 01_schema.sql and 02_seed_data.sql.

{drops}
"""


DB_SETUP = """# PeopleHub - Database Setup (PostgreSQL 17)

Each microservice owns **its own database** (database-per-service). They live in the same local PostgreSQL server for convenience,
but services never read each other's tables.

| Service | Database | JDBC URL | Scripts |
|---------|----------|----------|---------|
| employee-service | `peoplehub_employee` | `jdbc:postgresql://localhost:5432/peoplehub_employee` | `database/employee-service/` |
| leave-service | `peoplehub_leave` | `jdbc:postgresql://localhost:5432/peoplehub_leave` | `database/leave-service/` |
| notification-service | `peoplehub_notification` | `jdbc:postgresql://localhost:5432/peoplehub_notification` | `database/notification-service/` |

Role for all three: user `course_user`, password `change_me` (change it for anything but your own laptop).
Prerequisite: PostgreSQL 17 + `psql` ([`../../setup/POSTGRESQL_SETUP.md`](../../setup/POSTGRESQL_SETUP.md)).

## macOS (bash/zsh)

```bash
cd "Project 03 - PeopleHub HR Microservices"
for svc in employee-service:peoplehub_employee leave-service:peoplehub_leave notification-service:peoplehub_notification; do
  dir=${svc%%:*}; db=${svc##*:}
  psql -d postgres -f "database/$dir/00_create_database.sql"
  psql -U course_user -h localhost -d "$db" -f "database/$dir/01_schema.sql"
  psql -U course_user -h localhost -d "$db" -f "database/$dir/02_seed_data.sql"
done
```

## Windows (PowerShell)

```powershell
cd "Project 03 - PeopleHub HR Microservices"
$services = @{ "employee-service"="peoplehub_employee"; "leave-service"="peoplehub_leave"; "notification-service"="peoplehub_notification" }
foreach ($dir in $services.Keys) {
  $db = $services[$dir]
  psql -U postgres -h localhost -d postgres -f "database\\$dir\\00_create_database.sql"
  psql -U course_user -h localhost -d $db -f "database\\$dir\\01_schema.sql"
  psql -U course_user -h localhost -d $db -f "database\\$dir\\02_seed_data.sql"
}
```
(`psql` prompts for the `postgres` password for step 00 and for `change_me` for the others; set `$env:PGPASSWORD` to avoid prompts.)

## Starting over (one service)

```bash
psql -U course_user -h localhost -d peoplehub_leave -f database/leave-service/99_reset.sql
psql -U course_user -h localhost -d peoplehub_leave -f database/leave-service/01_schema.sql
psql -U course_user -h localhost -d peoplehub_leave -f database/leave-service/02_seed_data.sql
```

## Verify

```bash
psql -U course_user -h localhost -d peoplehub_employee -c "SELECT id, email, role FROM employees ORDER BY id;"
psql -U course_user -h localhost -d peoplehub_leave    -c "SELECT id, employee_id, status FROM leave_requests ORDER BY id;"
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `database "peoplehub_leave" does not exist` | Run that service's `00_create_database.sql` |
| `password authentication failed` | `ALTER ROLE course_user PASSWORD 'change_me';` as superuser |
| `\\gexec` not understood | Use `psql` (not a GUI) or create the database manually: `CREATE DATABASE peoplehub_leave OWNER course_user;` |
| Service fails with `Schema-validation: missing table` | Scripts applied to another database than the service's `DB_URL` |
"""

EVENT_DOC = """# LeaveApproved event (Kafka)

| | |
|---|---|
| Topic | `leave.approved.v1` (3 partitions locally; DLT: `leave.approved.v1.DLT`) |
| Key | `employeeId` as a string (keeps all events of one employee ordered) |
| Producer | **leave-service** - writes an `outbox_events` row in the same transaction as the approval; a poller publishes it |
| Consumer | **notification-service** - consumer group `notification-service`; creates a notification, idempotent via `processed_events` |
| Delivery | at-least-once; consumers MUST tolerate duplicates |

## Payload (version 1)

```json
{
  "version": 1,
  "eventId": "7d2f6d4c-5c9e-4c53-9a37-6f6a1d1d2b11",
  "leaveRequestId": 42,
  "employeeId": 3,
  "approverId": 2,
  "leaveType": "ANNUAL",
  "startDate": "2025-07-14",
  "endDate": "2025-07-18",
  "days": 5,
  "approvedAt": "2025-07-01T09:30:00Z"
}
```

Rules: add fields only (tolerant reader); bump `version` for breaking changes and publish to a new topic (`leave.approved.v2`)
while v1 consumers migrate; `eventId` is a UUID generated once per approval (reused by outbox retries).

## Flow

```mermaid
sequenceDiagram
    participant M as Manager
    participant L as leave-service
    participant DB as peoplehub_leave
    participant K as Kafka
    participant N as notification-service
    M->>L: PATCH /api/leaves/42/approve
    L->>DB: UPDATE leave_requests, leave_balances, INSERT outbox_events (one transaction)
    L-->>M: 200 APPROVED
    L->>K: outbox poller publishes leave.approved.v1 (key=employeeId)
    K->>N: LeaveApproved
    N->>N: INSERT processed_events (duplicate? skip)
    N->>N: INSERT notifications
```

## Error handling

- Consumer retries 3 times (`FixedBackOff(1000, 2)`), then the record goes to `leave.approved.v1.DLT`.
- Malformed JSON (poison) must not block the partition: use `ErrorHandlingDeserializer` or parse manually and throw a non-retryable exception.
- Monitor the DLT; replay after fixing the cause.

## Local topic creation (see `setup/KAFKA_SETUP.md`)

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic leave.approved.v1 --partitions 3 --replication-factor 1
kafka-topics --bootstrap-server localhost:9092 --create --topic leave.approved.v1.DLT --partitions 3 --replication-factor 1
kafka-console-consumer --bootstrap-server localhost:9092 --topic leave.approved.v1 --from-beginning --property print.key=true
```
"""

DATA_MODEL = """# PeopleHub - Data Model (database per service)

```mermaid
erDiagram
    DEPARTMENTS ||--o{ EMPLOYEES : contains
    EMPLOYEES ||--o{ EMPLOYEES : "manages (manager_id)"

    DEPARTMENTS { bigint id PK
                  varchar name UK }
    EMPLOYEES { bigint id PK
                varchar email UK
                varchar password_hash
                varchar role "HR_ADMIN | MANAGER | EMPLOYEE"
                bigint department_id FK
                bigint manager_id FK
                date hire_date
                varchar status
                int annual_leave_days }
```
*Database `peoplehub_employee` (employee-service).*

```mermaid
erDiagram
    LEAVE_REQUESTS { bigint id PK
                     bigint employee_id "id in employee-service (no FK)"
                     bigint approver_id
                     varchar leave_type "ANNUAL | SICK | UNPAID"
                     date start_date
                     date end_date
                     int days
                     varchar status "PENDING | APPROVED | REJECTED | CANCELLED" }
    LEAVE_BALANCES { bigint employee_id PK
                     int year PK
                     int total_days
                     int used_days }
    OUTBOX_EVENTS { bigint id PK
                    varchar event_type
                    varchar topic
                    jsonb payload
                    boolean published }
```
*Database `peoplehub_leave` (leave-service). Approving a request updates `leave_requests`, `leave_balances` and inserts into `outbox_events` in ONE transaction.*

```mermaid
erDiagram
    NOTIFICATIONS { bigint id PK
                    bigint recipient_employee_id "id in employee-service (no FK)"
                    varchar type
                    varchar message
                    varchar status "NEW | SENT | READ"
                    varchar source_event_id }
    PROCESSED_EVENTS { varchar event_id PK
                       timestamptz processed_at }
```
*Database `peoplehub_notification` (notification-service).*

## Why no foreign keys between services?

Each service can be deployed, migrated and scaled independently. Cross-service references are plain ids that you validate via the owning
service's API (`RestClient` + Resilience4j from Day 43) or accept from a trusted token claim. The price is *eventual consistency*:
an employee may be terminated after a leave request was created - handle that with events or compensating actions.
"""

README = """# Project 03 - PeopleHub HR Microservices

An HR platform split into independent services: **employee-service** (people, departments, logins), **leave-service** (leave requests,
balances, approvals), **notification-service** (consumes Kafka events and stores notifications) and an **api-gateway** (single entry point).
You practice service boundaries, database-per-service, REST between services, resilience, Kafka messaging, idempotency and the outbox pattern.

| Module | Port | Database | Role |
|--------|-----:|----------|------|
| `api-gateway` | 8080 | - | Spring Cloud Gateway (reactive), routes `/api/employees/**`, `/api/leaves/**`, `/api/notifications/**` |
| `employee-service` | 8081 | `peoplehub_employee` | Employees, departments, authentication |
| `leave-service` | 8082 | `peoplehub_leave` | Leave requests, balances, outbox; **produces** `LeaveApproved` |
| `notification-service` | 8083 | `peoplehub_notification` | **Consumes** `LeaveApproved`, stores notifications |

Documents: [`PROJECT_INSTRUCTIONS.md`](PROJECT_INSTRUCTIONS.md) · [`DATA_MODEL.md`](DATA_MODEL.md) · [`GRADING_CRITERIA.md`](GRADING_CRITERIA.md) ·
[`database/DATABASE_SETUP.md`](database/DATABASE_SETUP.md) · [`docs/LEAVE_APPROVED_EVENT.md`](docs/LEAVE_APPROVED_EVENT.md) · Kafka installation: [`../setup/KAFKA_SETUP.md`](../setup/KAFKA_SETUP.md)

## Prerequisites

- JDK 21, Maven 3.9+
- PostgreSQL 17 + `psql` ([`../setup/POSTGRESQL_SETUP.md`](../setup/POSTGRESQL_SETUP.md))
- Apache Kafka in KRaft mode on `localhost:9092` for the messaging milestones ([`../setup/KAFKA_SETUP.md`](../setup/KAFKA_SETUP.md)). **Unit/slice tests never need Kafka or PostgreSQL** (H2 + `EmbeddedKafka`).
- Completed Days 1-50

## 1. Create the three databases

```bash
cd "Project 03 - PeopleHub HR Microservices"
# macOS/Linux: loops over the three services; Windows PowerShell version in database/DATABASE_SETUP.md
for svc in employee-service:peoplehub_employee leave-service:peoplehub_leave notification-service:peoplehub_notification; do
  dir=${svc%%:*}; db=${svc##*:}
  psql -d postgres -f "database/$dir/00_create_database.sql"
  psql -U course_user -h localhost -d "$db" -f "database/$dir/01_schema.sql"
  psql -U course_user -h localhost -d "$db" -f "database/$dir/02_seed_data.sql"
done
```

## 2. CRITICAL: database connection per service (`application-local.yml`)

Every service reads its connection from placeholders (`${DB_URL}`, `${DB_USERNAME}`, `${DB_PASSWORD}`) in its own `application.yml`.
Create the git-ignored local file **for each of the three services**:

```bash
for s in employee-service leave-service notification-service; do
  cp "$s/src/main/resources/application-local.yml.example" "$s/src/main/resources/application-local.yml"
done
```
```powershell
foreach ($s in "employee-service","leave-service","notification-service") {
  Copy-Item "$s\\src\\main\\resources\\application-local.yml.example" "$s\\src\\main\\resources\\application-local.yml"
}
```

Each example already points to the right database (`jdbc:postgresql://localhost:5432/peoplehub_<service>`, user `course_user`, password `change_me`);
edit the password if you changed it. Start each service with the `local` profile. **Never commit `application-local.yml`.**
Alternative: set `DB_URL`, `DB_USERNAME`, `DB_PASSWORD` as environment variables (they differ per service!).

## 3. Build and run each service

```bash
mvn -q -DskipTests install                     # from the project root: builds all modules

# one terminal per service
mvn -pl employee-service     spring-boot:run -Dspring-boot.run.profiles=local     # http://localhost:8081
mvn -pl leave-service        spring-boot:run -Dspring-boot.run.profiles=local     # http://localhost:8082
mvn -pl notification-service spring-boot:run -Dspring-boot.run.profiles=local     # http://localhost:8083
mvn -pl api-gateway          spring-boot:run                                      # http://localhost:8080 (no database)

curl http://localhost:8081/            # welcome JSON of employee-service
curl http://localhost:8080/api/employees/   # goes through the gateway once you implement the endpoint
```

Run all tests: `mvn test` (root) - every module has an H2 based smoke test; the gateway test verifies the three routes.

### Environment variables (leave-service and notification-service)

| Variable | Default | Meaning |
|----------|---------|---------|
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Broker address |
| `EMPLOYEE_SERVICE_URL` | `http://localhost:8081` | Used by leave-service (RestClient) and the gateway route |
| `LEAVE_SERVICE_URL`, `NOTIFICATION_SERVICE_URL` | localhost 8082 / 8083 | Gateway routes |

## 4. Kafka: the LeaveApproved event

1. Start Kafka (see `setup/KAFKA_SETUP.md`) and create the topics:
   ```bash
   kafka-topics --bootstrap-server localhost:9092 --create --topic leave.approved.v1 --partitions 3 --replication-factor 1
   kafka-topics --bootstrap-server localhost:9092 --create --topic leave.approved.v1.DLT --partitions 3 --replication-factor 1
   ```
2. **leave-service** approves a request (`PATCH /api/leaves/{id}/approve`), writes the outbox row in the same transaction and a poller publishes it.
3. **notification-service** consumes it in group `notification-service`, skips duplicates (`processed_events`) and inserts a notification.
4. Contract, flow and error handling: [`docs/LEAVE_APPROVED_EVENT.md`](docs/LEAVE_APPROVED_EVENT.md).

## Seed logins

Plain-text passwords below are for **local development only**; the database stores the BCrypt hashes (cost 10) found in
`database/employee-service/02_seed_data.sql`.

| Email | Role | Plain password | BCrypt hash stored in SQL |
|-------|------|----------------|---------------------------|
| `hr@peoplehub.com` | HR_ADMIN | `HrAdmin@123` | `@@ADMIN@@` |
| `manager@peoplehub.com` | MANAGER (manages Alice and Bob) | `Manager@123` | `@@MGR@@` |
| `alice@peoplehub.com` | EMPLOYEE | `Employee@123` | `@@EMP@@` |
| `bob@peoplehub.com` | EMPLOYEE | `Employee@123` | `@@EMP@@` |
| `carol@peoplehub.com` | EMPLOYEE | `Employee@123` | `@@EMP@@` |

## Layout

```
Project 03 - PeopleHub HR Microservices/
  pom.xml                      parent (Boot 3.4.x + Spring Cloud 2024.0.x BOM)
  employee-service/  leave-service/  notification-service/  api-gateway/     (Spring Boot modules)
  database/  employee-service/  leave-service/  notification-service/  DATABASE_SETUP.md
  docs/      LEAVE_APPROVED_EVENT.md
  README.md  PROJECT_INSTRUCTIONS.md  DATA_MODEL.md  GRADING_CRITERIA.md
```

## Git workflow

Branch `student/<id>/project-03`; one pull request per milestone/service; never commit `application-local.yml`, `.env`, `target/`.
"""

INSTR = """# PeopleHub - Project Instructions

## 1. Goal

Build four cooperating Spring Boot modules that together support leave management: employees exist in one service, leave requests in
another, and a third reacts to approvals asynchronously. Practice boundaries, REST between services with resilience, Kafka, idempotency and the outbox.

## 2. Rules

- Java 21, Spring Boot (3.4.x skeleton; course target Boot 4), Maven multi-module, PostgreSQL, Kafka in KRaft mode. No Lombok. No Docker.
- **Database per service.** No cross-database foreign keys or shared tables; cross-service data via API or events only.
- Schemas are given (`database/<service>/01_schema.sql`); `ddl-auto=validate`.
- Passwords BCrypt; JWT issued by employee-service and validated at the gateway **and** (defense in depth) in the services.
- All errors as `ProblemDetail`; secrets via env/`application-local.yml`.

## 3. Milestones

### Milestone A - Databases and skeleton running
All four modules build (`mvn test` green), each service starts against its own database, `/actuator/health` is UP, gateway routes configured.

### Milestone B - employee-service
Entities `Department`, `Employee` (self-reference to manager); `POST /api/auth/login` (JWT with `sub=employeeId`, `role`),
`GET /api/employees` (paged, HR_ADMIN/MANAGER), `GET /api/employees/{id}` (self, own manager, HR), `POST /api/employees` (HR_ADMIN).

### Milestone C - leave-service
- Entities `LeaveRequest`, `LeaveBalance`. `POST /api/leaves` (employee creates for self, validates dates, days, balance, overlaps with own pending/approved requests).
- `GET /api/leaves/my`, `GET /api/leaves/team` (manager: requests of direct reports, fetched through employee-service with `RestClient`).
- Resilience (Day 43): timeout, retry and circuit breaker with a clear fallback when employee-service is down (e.g. 503 `ProblemDetail`, no partial data).

### Milestone D - approvals and the LeaveApproved event
- `PATCH /api/leaves/{id}/approve` and `/reject` (manager of the employee or HR). Approval = update request + increment `used_days` + insert outbox row **in one transaction**; reject/approve twice -> 409.
- Outbox poller publishes `leave.approved.v1` (JSON, key = employeeId) and marks rows published (Day 46).
- Tests: `EmbeddedKafka` producer test, transactional rollback test, poller failure test.

### Milestone E - notification-service and edge
- `@KafkaListener` (group `notification-service`) with `DefaultErrorHandler` + DLT; idempotent processing via `processed_events`; tolerant JSON reader.
- `GET /api/notifications/my` (paged), `PATCH /api/notifications/{id}/read` (owner only).
- Gateway: JWT validation global filter, `X-Request-Id` propagation (provided), forwards `X-User-Id`/`X-User-Role`; rate limit idea documented.
- Production notes: profiles, env secrets, executable JARs, GitHub Actions matrix over modules.

## 4. API contract (through the gateway on port 8080)

| Method | Path | Role | Service | Success | Errors |
|--------|------|------|---------|---------|--------|
| POST | `/api/auth/login` | public | employee | 200 `{token}` | 401 |
| GET | `/api/employees` | HR_ADMIN, MANAGER | employee | 200 `Page` | 403 |
| GET | `/api/employees/{id}` | self, manager, HR | employee | 200 | 404 |
| POST | `/api/employees` | HR_ADMIN | employee | 201 | 400, 409 |
| POST | `/api/leaves` | EMPLOYEE, MANAGER | leave | 201 | 400, 409 |
| GET | `/api/leaves/my` | authenticated | leave | 200 | - |
| GET | `/api/leaves/team` | MANAGER | leave | 200 | 403, 503 |
| PATCH | `/api/leaves/{id}/approve` | MANAGER of employee, HR_ADMIN | leave | 200 | 404, 409 |
| PATCH | `/api/leaves/{id}/reject` | MANAGER of employee, HR_ADMIN | leave | 200 | 404, 409 |
| GET | `/api/notifications/my` | authenticated | notification | 200 | - |
| PATCH | `/api/notifications/{id}/read` | owner | notification | 200 | 404 |

## 5. User stories

1. As an employee I can request leave and see my balance and request history.
2. As a manager I can see my team's pending requests and approve or reject them.
3. As an employee I am notified when my leave is approved - even if notification-service was down during the approval.
4. As HR I can create employees and see everyone.
5. As an operator I can restart any service without losing events (outbox + consumer offsets) and without duplicate notifications (idempotency).
6. As an operator I see one `X-Request-Id` across gateway and service logs.

## 6. Business rules

- A request needs `endDate >= startDate`; `days` counts working days (Mon-Fri) between the dates, calculated by the server.
- `ANNUAL` leave cannot exceed the remaining balance; `SICK`/`UNPAID` do not consume balance.
- No overlapping PENDING/APPROVED requests per employee.
- Only `PENDING` requests can be approved/rejected; the approver cannot be the requester.

## 7. Security requirements

JWT (HS256 shared secret from env `JWT_SECRET`, >= 32 chars, expiry), services trust only requests that carry a valid token or come from the gateway
network path; object-level checks everywhere (employees see only their own leaves/notifications, managers only their reports); no secrets in Git; safe error messages.

## 8. Deliverables

Working modules, tests (unit, slice, `EmbeddedKafka`), per-service README addendum (endpoints, env vars), `DESIGN_NOTES.md` (boundaries, consistency, failure handling), pull requests per milestone.
"""

GRADING = """# PeopleHub - Grading Criteria (100 points)

| Category | Points | What graders look for |
|----------|-------:|-----------------------|
| Boundaries and database-per-service (A) | 10 | Each service starts with its own DB; no cross-DB FKs or shared tables; clean module structure |
| employee-service (B) | 12 | Auth, entities, paging, authorization |
| leave-service (C) | 18 | Business rules, balance logic, RestClient with timeout/retry/circuit breaker and fallback |
| Approval + outbox + Kafka producer (D) | 20 | One transaction for approval + outbox, poller semantics, JSON contract, EmbeddedKafka tests |
| notification-service consumer (E) | 14 | Consumer group, DLT/error handling, idempotency, owner-only endpoints |
| Gateway and security | 8 | Routes, JWT at the edge, request id, object-level checks, no secrets in Git |
| Testing | 10 | Unit/slice/Kafka tests, `mvn test` green without PostgreSQL/Kafka |
| Documentation and Git | 8 | README accuracy, per-service run notes, PR hygiene |

## Automatic deductions

- Cross-database foreign key or direct SQL access to another service's database: **-10**
- Kafka publish inside the approval transaction without outbox (dual write): **-8**
- Consumer without idempotency: **-8**
- `application-local.yml`, credentials or `target/` committed: **-10**
- `mvn test` red on a clean checkout: **-15**

## AI grading prompt

```
You are grading Project 03 (PeopleHub HR Microservices). Use repository evidence and `mvn test` output only.
Check: database per service, approval + outbox in one transaction, event contract matches docs/LEAVE_APPROVED_EVENT.md,
consumer idempotency + DLT, RestClient resilience with fallback, gateway routes + auth at the edge, owner-only access, no secrets committed.
Score /100 with GRADING_CRITERIA.md weights; list blocking issues first.
```
"""

LOCAL_EXAMPLE_NOTE = ""


def build(root: Path) -> None:
    base = root / NAME
    kw = dict(ADMIN=H_ADMIN, MGR=H_MGR, EMP=H_EMP)
    write(base / "README.md", sub(README, **kw))
    write(base / "PROJECT_INSTRUCTIONS.md", INSTR)
    write(base / "DATA_MODEL.md", DATA_MODEL)
    write(base / "GRADING_CRITERIA.md", GRADING)
    write(base / "docs/LEAVE_APPROVED_EVENT.md", EVENT_DOC)
    write(base / "pom.xml", sub(PARENT_POM, BOOT=BOOT_VERSION))

    # database
    db = base / "database"
    write(db / "DATABASE_SETUP.md", DB_SETUP)
    write(db / "employee-service/00_create_database.sql", sql_create("peoplehub_employee"))
    write(db / "employee-service/01_schema.sql", EMP_SCHEMA)
    write(db / "employee-service/02_seed_data.sql", sub(EMP_SEED, **kw))
    write(db / "employee-service/99_reset.sql", reset_sql("peoplehub_employee", ["employees", "departments"]))
    write(db / "leave-service/00_create_database.sql", sql_create("peoplehub_leave"))
    write(db / "leave-service/01_schema.sql", LEAVE_SCHEMA)
    write(db / "leave-service/02_seed_data.sql", LEAVE_SEED)
    write(db / "leave-service/99_reset.sql", reset_sql("peoplehub_leave", ["outbox_events", "leave_balances", "leave_requests"]))
    write(db / "notification-service/00_create_database.sql", sql_create("peoplehub_notification"))
    write(db / "notification-service/01_schema.sql", NOTIF_SCHEMA)
    write(db / "notification-service/02_seed_data.sql", NOTIF_SEED)
    write(db / "notification-service/99_reset.sql", reset_sql("peoplehub_notification", ["processed_events", "notifications"]))

    # services
    for folder, dbname, port, pkg, cls, title in SERVICES:
        kafka = KAFKA_DEP if folder in ("leave-service", "notification-service") else ""
        pom = SERVICE_POM.replace("@@KAFKA@@", kafka)
        extra = {}
        short = pkg.split(".")[1]
        if folder in ("leave-service", "notification-service"):
            extra["events/LeaveApprovedEvent.java"] = EVENT_JAVA.replace("@@SHORT@@", short)
        write_service(base / folder, pkg=pkg, cls=cls, artifact=folder, title=title, desc=title, appname=folder, db=dbname, port=port,
                      standalone_pom=False, pom_override=pom, extra_main=extra)
        if kafka:
            # Kafka settings appended to the service configuration (producer/consumer defaults, bootstrap from env)
            yml = base / folder / "src/main/resources/application.yml"
            block = ("  kafka:\n    bootstrap-servers: ${KAFKA_BOOTSTRAP_SERVERS:localhost:9092}\n"
                     + ("    producer:\n      acks: all\n      key-serializer: org.apache.kafka.common.serialization.StringSerializer\n      value-serializer: org.apache.kafka.common.serialization.StringSerializer\n"
                        if folder == "leave-service" else
                        "    consumer:\n      group-id: notification-service\n      auto-offset-reset: earliest\n      key-deserializer: org.apache.kafka.common.serialization.StringDeserializer\n      value-deserializer: org.apache.kafka.common.serialization.StringDeserializer\n    listener:\n      ack-mode: record\n"))
            text = yml.read_text(encoding="utf-8")
            yml.write_text(text.replace("server:\n", block + "server:\n", 1), encoding="utf-8")

    # gateway (reactive; does not use the MVC skeleton)
    gw = base / "api-gateway"
    write(gw / "pom.xml", GATEWAY_POM)
    jb = gw / "src/main/java/com/javaprep/peoplehub/gateway"
    write(jb / "GatewayApplication.java", GATEWAY_APP)
    write(jb / "RequestIdFilter.java", GATEWAY_FILTER)
    write(gw / "src/main/resources/application.yml", GATEWAY_YML)
    write(gw / "src/test/java/com/javaprep/peoplehub/gateway/GatewaySmokeTest.java", GATEWAY_TEST)
