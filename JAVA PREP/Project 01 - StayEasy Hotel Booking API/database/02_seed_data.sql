-- 02_seed_data.sql
-- Demo data. Run after 01_schema.sql:  psql -U course_user -d stayeasy -f database/02_seed_data.sql
--
-- Seed accounts (plain-text passwords are documented in README.md; the database stores only the BCrypt hashes):
--   admin@stayeasy.com    / Admin@123
--   manager@stayeasy.com  / Manager@123
--   manager2@stayeasy.com / Manager@123
--   guest@stayeasy.com    / Guest@123
--   guest2@stayeasy.com   / Guest@123

INSERT INTO users (id, email, password_hash, full_name, role) VALUES
 (1, 'admin@stayeasy.com',    '$2a$10$6Ai9fZGYXWcJcFj2FxED0eBQ5dBwrOgfgQg/1dRO.Cq6F4VT/ku2C', 'Ada Admin',      'ADMIN'),
 (2, 'manager@stayeasy.com',  '$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m', 'Mia Manager',    'MANAGER'),
 (3, 'manager2@stayeasy.com', '$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m', 'Marco Manager',  'MANAGER'),
 (4, 'guest@stayeasy.com',    '$2a$10$/lC0I8o7r/LGYFuyJ2z8/edADXBrSE3CwVyeaXeggQxEba501CfNS', 'Gina Guest',     'GUEST'),
 (5, 'guest2@stayeasy.com',   '$2a$10$/lC0I8o7r/LGYFuyJ2z8/edADXBrSE3CwVyeaXeggQxEba501CfNS', 'Gus Guest',      'GUEST');

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
