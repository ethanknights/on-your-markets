# utils.py
from requests import Session, get
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import streamlit as st
from datetime import datetime
import psycopg2
import pandas as pd
import plotly.subplots as sp
import plotly.graph_objects as go
import datetime as dt


def create_psql_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432"
    )


def call_coinmarketcap_api():
    # base_url = 'https://sandbox-api.coinmarketcap.com'
    base_url = 'https://pro-api.coinmarketcap.com'
    url = f'{base_url}/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '5',
        'convert': 'GBP',
        'cryptocurrency_type': 'coins',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('API-KEY-COINMARKETCAP'),
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        json_data = json.loads(response.text)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        json_data = None
        st.error(f"Error: {e}")

    return json_data


def process_coinmarketcap_api(raw_coins):

    config_coins = {
        'BTC_ID': int(1),
        'ETH_ID': int(1027),
        'BNB_ID': int(1839),
        'SOL_ID': int(5426),
    }

    coins = [coin for coin in raw_coins['data'] if coin['id'] in config_coins.values()]
    assert coins, 'No `coins` present after filter'

    return coins


def insert_psql_db_coinmarketcap(conn_cursor, data):
    insert_query = """
        INSERT INTO on_your_market_prices (coin_name, price, timestamp)
        VALUES (%s, %s, %s);
    """

    try:
        for asset in data:
            asset_name = asset['symbol']
            price = int(round(asset['quote']['GBP']['price']))
            timestamp = datetime.strptime(asset
                                          ['quote']['GBP']['last_updated'],
                                          "%Y-%m-%dT%H:%M:%S.%fZ")

            print(f'Ready for psql write: {price} {timestamp}')
            data_to_insert = (asset_name, price, timestamp)
            conn_cursor.execute(insert_query, data_to_insert)

        conn_cursor.connection.commit()
        st.success("Data collection successful!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn_cursor.close()

    return


def fetch_coins_data_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM on_your_market_prices "
                   "WHERE coin_name IN ('BTC','ETH','BNB','SOL');")
    data = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(data, columns=['id', 'coin_name', 'price', 'timestamp'])

    return df


def plot_coins(df):
    # Plot coins in 2x2 grid
    fig = sp.make_subplots(rows=2, cols=2, subplot_titles=df['coin_name'].unique())

    # Iterate through each coin and add a line chart to the corresponding subplot
    for i, coin_name in enumerate(df['coin_name'].unique()):
        coin_data = df[df['coin_name'] == coin_name]

        # Add a line chart to the subplot
        fig.add_trace(go.Scatter(x=coin_data['timestamp'],
                                 y=coin_data['price'],
                                 mode='lines+markers',
                                 name=coin_name),
                      row=(i // 2) + 1, col=(i % 2) + 1)

    st.plotly_chart(fig)


# Alpha Vantage Integrations
# ----------------------------------------------
def call_alphavantage_api(symbol):
    # symbol = 'IBM'

    base_url = 'https://www.alphavantage.co'
    endpoint = 'query'
    function = 'TIME_SERIES_DAILY'
    interval = '1d'
    api_key = os.getenv('API-KEY-ALPHAVANTAGE')

    url = f'{base_url}/{endpoint}' \
          f'?function={function}&symbol={symbol}&interval={interval}&apikey={api_key}'

    headers = {
        'Accepts': 'application/json',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url,)
        json_data = response.json()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        json_data = None
        st.error(f"Error: {e}")

    return json_data


def create_st_ticker_search_box():

    # Create a text input for the user to enter the ticker
    ticker_input = st.text_input("Ticker Symbol Search:", "TESCO")

    if st.button("Search"):
        result = ticker_search_alphavantage(ticker_input)
        st.json(result)  # Display the result in the Streamlit app

    return


def ticker_search_alphavantage(query_term):
    api_key = os.getenv('API-KEY~ALPHAVANTAGE')

    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' \
          f'{query_term}&apikey={api_key}'
    r = get(url)
    data = r.json()

    return data


# Polygon Integrations
# ----------------------------------------------
def call_polygon_api(symbol):
    # symbol = 'VOO'

    base_url = 'https://api.polygon.io'
    endpoint = 'v2/aggs'
    date_start = '2023-01-09'
    date_end = '2023-01-09'

    api_key = os.getenv('API-KEY-POLYGON')

    url = f'{base_url}/{endpoint}' \
          f'/ticker/{symbol}/range/1/day/{date_start}/{date_end}' \
          f'?adjusted=true&sort=asc&limit=3&apiKey={api_key}'

    headers = {
        'Accepts': 'application/json',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url,)
        json_data = response.json()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        json_data = None
        st.error(f"Error: {e}")

    return json_data


def insert_psql_db_polygon(conn_cursor, raw_stock):

    insert_query = """
        INSERT INTO on_your_market_prices (coin_name, price, timestamp)
        VALUES (%s, %s, %s);
    """

    try:
        assert raw_stock, 'No `raw_stock` found'

        asset_name = raw_stock['ticker']
        price = raw_stock['results'][0]['c']
        timestamp = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        print(f'Ready for psql write: {price} {timestamp}')
        data_to_insert = (asset_name, price, timestamp)
        conn_cursor.execute(insert_query, data_to_insert)

        conn_cursor.connection.commit()
        st.success(f"Data collection successful - {asset_name}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn_cursor.close()

    return


def fetch_stocks_data_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM on_your_market_prices "
                   "WHERE coin_name IN ('IBM','VOO');")
    data = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(data, columns=['id', 'coin_name', 'price', 'timestamp'])

    return df


def plot_stocks(df):
    # Plot coins in 2x2 grid
    fig = sp.make_subplots(rows=1, cols=2, subplot_titles=df['coin_name'].unique())

    # Iterate through each coin and add a line chart to the corresponding subplot
    for i, asset_name in enumerate(df['coin_name'].unique()):
        data = df[df['coin_name'] == asset_name]

        # Add a line chart to the subplot
        fig.add_trace(go.Scatter(x=data['timestamp'],
                                 y=data['price'],
                                 mode='lines+markers',
                                 name=asset_name),
                      row=(i // 2) + 1, col=(i % 2) + 1)

    st.plotly_chart(fig)
