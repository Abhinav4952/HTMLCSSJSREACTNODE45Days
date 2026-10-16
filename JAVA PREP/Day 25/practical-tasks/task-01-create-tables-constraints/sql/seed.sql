-- PROVIDED: valid once schema.sql is complete.
INSERT INTO customers (email, full_name) VALUES ('ana@x.io', 'Ana');
INSERT INTO customers (email, full_name) VALUES ('bob@x.io', 'Bob');
INSERT INTO customers (email, full_name) VALUES ('cy@x.io', 'Cy');
INSERT INTO products (sku, name, price_cents) VALUES ('SKU-1', 'Keyboard', 4999);
INSERT INTO products (sku, name, price_cents) VALUES ('SKU-2', 'Mouse', 1999);
INSERT INTO orders (customer_id) VALUES (1);
