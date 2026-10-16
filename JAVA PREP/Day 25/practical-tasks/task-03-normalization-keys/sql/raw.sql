-- PROVIDED: the flat, denormalized source data (do not edit)
CREATE TABLE raw_orders (
    order_id INT, customer_email VARCHAR(120), customer_name VARCHAR(100),
    sku VARCHAR(30), product_name VARCHAR(100), qty INT, unit_price_cents INT
);
INSERT INTO raw_orders VALUES (1, 'ana@x.io', 'Ana', 'SKU-A', 'Keyboard', 1, 5000);
INSERT INTO raw_orders VALUES (1, 'ana@x.io', 'Ana', 'SKU-B', 'Mouse', 2, 2000);
INSERT INTO raw_orders VALUES (2, 'bob@x.io', 'Bob', 'SKU-A', 'Keyboard', 1, 5000);
INSERT INTO raw_orders VALUES (2, 'bob@x.io', 'Bob', 'SKU-C', 'Monitor', 1, 20000);
INSERT INTO raw_orders VALUES (3, 'ana@x.io', 'Ana', 'SKU-C', 'Monitor', 2, 20000);
