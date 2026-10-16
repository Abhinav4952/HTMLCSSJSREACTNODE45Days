-- 01_schema.sql (peoplehub_employee)
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
