-- -- Aggregate metrics for business KPIs
-- INSERT INTO DIM_SALES_SUMMARY_GOLD (category, total_revenue, avg_order_value, order_count, last_updated)
-- SELECT 
--     product_category,
--     SUM(total_amount) as total_revenue,
--     AVG(total_amount) as avg_order_value,
--     COUNT(order_id) as order_count,
--     CURRENT_TIMESTAMP()
-- FROM FACT_SALES_SILVER
-- WHERE is_valid_transaction = TRUE
-- GROUP BY product_category;

-- Aggregate business KPIs while removing PII columns

INSERT INTO DIM_SALES_SUMMARY_GOLD (
    category,
    total_revenue,
    avg_order_value,
    order_count,
    completed_orders,
    last_updated
)

SELECT
    product_category,

    SUM(total_amount) AS total_revenue,

    AVG(total_amount) AS avg_order_value,

    COUNT(order_id) AS order_count,

    SUM(
        CASE
            WHEN is_valid_transaction = TRUE
            THEN 1
            ELSE 0
        END
    ) AS completed_orders,

    CURRENT_TIMESTAMP()

FROM FACT_SALES_SILVER

GROUP BY product_category;