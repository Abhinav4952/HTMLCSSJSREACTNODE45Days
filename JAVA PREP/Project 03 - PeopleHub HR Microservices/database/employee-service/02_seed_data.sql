-- 02_seed_data.sql (peoplehub_employee)
-- Logins (plain passwords are documented in README.md; only BCrypt hashes are stored):
--   hr@peoplehub.com / HrAdmin@123      manager@peoplehub.com / Manager@123
--   alice@peoplehub.com, bob@peoplehub.com, carol@peoplehub.com / Employee@123

INSERT INTO departments (id, name) VALUES (1, 'Human Resources'), (2, 'Engineering'), (3, 'Finance');

INSERT INTO employees (id, email, password_hash, full_name, role, department_id, manager_id, hire_date) VALUES
 (1, 'hr@peoplehub.com',      '$2a$10$AT4q/atqVTOFiepku8soV.IBYYPDcDXl4VMEbIZgbfgu9YciYpc3y', 'Hana Reyes',   'HR_ADMIN', 1, NULL, DATE '2020-01-15'),
 (2, 'manager@peoplehub.com', '$2a$10$/B1oGH3MSrfkgJEIJHBWdOBat26s5vI5HvBOqImGTMW9zO5npIL/m',   'Milo Grant',   'MANAGER',  2, 1,    DATE '2021-03-01'),
 (3, 'alice@peoplehub.com',   '$2a$10$GVpJM/q6STyj1bpCenjoQ.4jKsjz5F9V9.rz6OKM69PGNkXKHYJ46',   'Alice Walker', 'EMPLOYEE', 2, 2,    DATE '2022-06-20'),
 (4, 'bob@peoplehub.com',     '$2a$10$GVpJM/q6STyj1bpCenjoQ.4jKsjz5F9V9.rz6OKM69PGNkXKHYJ46',   'Bob Turner',   'EMPLOYEE', 2, 2,    DATE '2023-02-10'),
 (5, 'carol@peoplehub.com',   '$2a$10$GVpJM/q6STyj1bpCenjoQ.4jKsjz5F9V9.rz6OKM69PGNkXKHYJ46',   'Carol Diaz',   'EMPLOYEE', 3, 1,    DATE '2023-09-05');

SELECT setval(pg_get_serial_sequence('departments', 'id'), (SELECT MAX(id) FROM departments));
SELECT setval(pg_get_serial_sequence('employees', 'id'),   (SELECT MAX(id) FROM employees));
