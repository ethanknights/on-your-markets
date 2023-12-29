-- Delete placeholder rows from initial code (id 1, 2)
DELETE FROM on_your_market_prices
WHERE id IN (
    SELECT id
    FROM on_your_market_prices
    ORDER BY timestamp
    LIMIT 2
);