-- 01_schema.sql  (PostgreSQL 17)
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
