# StayEasy - Grading Criteria (100 points)

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
