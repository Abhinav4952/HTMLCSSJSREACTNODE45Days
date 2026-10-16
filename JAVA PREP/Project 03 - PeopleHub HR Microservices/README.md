# Project 03 - PeopleHub HR Microservices

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
  Copy-Item "$s\src\main\resources\application-local.yml.example" "$s\src\main\resources\application-local.yml"
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
| `hr@peoplehub.com` | HR_ADMIN | `HrAdmin@123` | `$2a$10$AT4q/atqVTOFiepku8soV.IBYYPDcDXl4VMEbIZgbfgu9YciYpc3y` |
| `manager@peoplehub.com` | MANAGER (manages Alice and Bob) | `Manager@123` | `$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m` |
| `alice@peoplehub.com` | EMPLOYEE | `Employee@123` | `$2a$10$GVpJM/q6STyj1bpCenjoQ.4jKsjz5F9V9.rz6OKM69PGNkXKHYJ46` |
| `bob@peoplehub.com` | EMPLOYEE | `Employee@123` | `$2a$10$GVpJM/q6STyj1bpCenjoQ.4jKsjz5F9V9.rz6OKM69PGNkXKHYJ46` |
| `carol@peoplehub.com` | EMPLOYEE | `Employee@123` | `$2a$10$GVpJM/q6STyj1bpCenjoQ.4jKsjz5F9V9.rz6OKM69PGNkXKHYJ46` |

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
