-- PROVIDED
CREATE TABLE customers (id INT PRIMARY KEY, email VARCHAR(120) NOT NULL);
CREATE TABLE orders (id INT PRIMARY KEY, customer_id INT NOT NULL REFERENCES customers(id));
CREATE TABLE order_items (
    order_id INT NOT NULL REFERENCES orders(id), sku VARCHAR(20) NOT NULL,
    qty INT NOT NULL, unit_price_cents INT NOT NULL, PRIMARY KEY (order_id, sku)
);
