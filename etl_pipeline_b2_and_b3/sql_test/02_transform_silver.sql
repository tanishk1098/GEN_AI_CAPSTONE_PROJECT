-- Clean, cast types, and filter out nulls/unknowns
INSERT INTO FACT_SALES_SILVER (order_id, customer_id, product_category, total_amount, order_date, order_status, is_valid_transaction)
SELECT 
    order_id::INT,
    customer_id::INT,
    product_category,
    amount::FLOAT,
    order_date::DATE,
    NVL(status, 'Unknown'),
    CASE WHEN status = 'Completed' THEN TRUE ELSE FALSE END
FROM RAW_SALES_BRONZE;