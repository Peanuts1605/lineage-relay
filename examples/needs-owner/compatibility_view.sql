CREATE OR REPLACE VIEW orders_compat AS
SELECT order_id, buyer_id, buyer_id AS customer_id, created_at
FROM orders;
