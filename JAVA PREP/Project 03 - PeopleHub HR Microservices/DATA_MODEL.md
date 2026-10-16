# PeopleHub - Data Model (database per service)

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
