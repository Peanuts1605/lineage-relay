SELECT COUNT(*) AS mismatches
FROM orders_compat
WHERE buyer_id IS DISTINCT FROM customer_id;
