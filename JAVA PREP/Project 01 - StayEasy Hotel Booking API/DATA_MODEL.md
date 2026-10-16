# StayEasy - Data Model

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
