-- docker compose up
-- docker exec -it postgres-on-your-markets psql -U postgres -d postgres
-- now in psql terminal:

CREATE TABLE on_your_market_prices (
    id SERIAL PRIMARY KEY,
    coin_name VARCHAR(50),
    price INTEGER,
    timestamp TIMESTAMP
);


SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_name = 'on_your_markets_prices';


-- reminder: DROP TABLE on_your_market_prices;
-- reminder: postgres superuser currently used vs. user whose role is GRANT-ed permissions for modifying the psql DB.