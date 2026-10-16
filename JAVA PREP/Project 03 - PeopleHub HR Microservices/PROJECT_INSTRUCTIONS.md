# PeopleHub - Project Instructions

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
