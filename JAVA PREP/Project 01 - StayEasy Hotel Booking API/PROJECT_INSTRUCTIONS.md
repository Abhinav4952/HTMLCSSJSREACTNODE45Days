# StayEasy - Project Instructions

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
