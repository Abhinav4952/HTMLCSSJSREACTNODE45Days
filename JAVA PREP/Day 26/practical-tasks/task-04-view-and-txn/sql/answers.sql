-- @create_view_order_totals
-- TODO(Day26-task04): CREATE VIEW order_totals AS SELECT order_id, SUM(qty * unit_price_cents) AS total_cents FROM order_items GROUP BY order_id

-- @q_big_orders
-- TODO(Day26-task04): SELECT order_id, total_cents FROM the VIEW where total_cents >= 10000 ORDER BY order_id

-- @q_domain_counts
-- TODO(Day26-task04): email domain (text after '@') and number of customers per domain, ORDER BY domain.
--              Hint: SUBSTR(email, POSITION('@' IN email) + 1)
