# on-your-markets

# Database
## Components
- Postgresql
```docker compose up -d```

## First-time-Setup
In bash:
```shell
docker exec -it postgres-on-your-markets psql -U postgres -d postgres
```

Within psql terminal:
```sql
CREATE TABLE on_your_market_prices (
    id SERIAL PRIMARY KEY,
    coin_name VARCHAR(50),
    price INTEGER,
    timestamp TIMESTAMP
);
```


# Notes

- Heroku - Cloud application hosting (e.g. app & database) - redirect CNAME from owned DNS.
