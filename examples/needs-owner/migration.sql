ALTER TABLE orders ADD COLUMN buyer_id VARCHAR;
UPDATE orders SET buyer_id = customer_id WHERE buyer_id IS NULL;
-- Do not drop customer_id in this release.
