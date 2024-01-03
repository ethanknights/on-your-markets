# <i>On-Your-Markets</i> - Market Tracker Application
Start tracking the markets you care about.

This application demonstrates how to use Streamlit with a FastAPI framework to:
- Collect external financial asset data from APIs using python.
- Write the requested data to a contained database server.
- Enable data consumption using an outward API framework.
- Visualise consumed data interactively.

# Local Quickstart
1. Start API server from root: `uvicorn src.fastAPI_app.app:app --reload`
2. Run application from root: `venv/bin/streamlit run src/streamlit_app/app.py`
3. Use application: http://localhost:8501
 
<b>Prerequisites</b>
- Install python packages in a virtual environment: `pip install -r requirements.txt`
- Install docker (`brew docker`) and start a local postgreSQL container: `docker compose up -d`
- Create the `psql` data table (refer to the `SQL` snippet in the section: [Database](#Database)).
- Add your API-Keys for each external service in `sample.env.dev` & rename this file to `.env.dev`.

# Tech-Stack
- Framework: `Streamlit`
- Source Code: `Python`
- Database: `PostgreSQL`
- Outward API: `FastAPI`
- CI/CD: `GitHub Actions`

## Framework
The frontend & runtime is handled by Streamlit: `venv/bin/streamlit run src/streamlit_app/app.py`

## Source Code
The bulk of this application is implemented in Python using `src/streamlit_app/app.py` with `src/common/utils.py`. 

Generally the flow involves:
- Connecting to the PostrgreSQL database table using `psycopg2`.
- Triggering realtime data collection by button-press, which writes data to `psql` from external API sources.
- Reading database data from FastAPI endpoints enabled in `src/fastAPI_app/app.py`.
- Plotting all-time data interactively using `plotly`.

## Database
### First-time-setup
 Connect to your PostgreSQL contained server in bash:
```shell
docker exec -it postgres-on-your-markets psql -U postgres -d postgres
```

Create the core table within the psql terminal:
```sql
CREATE TABLE on_your_market_prices (
    id SERIAL PRIMARY KEY,
    coin_name VARCHAR(50),
    price INTEGER,
    timestamp TIMESTAMP
);
```

## Outward API
The FastAPI framework is used to setup endpoints (see `src/fastAPI_app/app.py`) for consuming historical asset value's from the database:
`requests.get('http://127.0.0.1:8000/get_stocks_data')`

## CI/CD
Currently, basic linting & formatting (`black` & `flake8`) are applied by GitHub Actions for each repository push.


# Notes
- Heroku - Cloud application hosting (e.g. app & database) - redirect CNAME from owned DNS.
