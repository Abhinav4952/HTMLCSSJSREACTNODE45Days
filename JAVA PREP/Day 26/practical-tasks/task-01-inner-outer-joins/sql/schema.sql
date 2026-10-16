-- PROVIDED
CREATE TABLE departments (id INT PRIMARY KEY, name VARCHAR(30) NOT NULL);
CREATE TABLE employees (
    id INT PRIMARY KEY, name VARCHAR(30) NOT NULL,
    dept_id INT REFERENCES departments(id),
    manager_id INT REFERENCES employees(id)
);
