# utils.py
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import streamlit as st
from datetime import datetime
import psycopg2
import pandas as pd


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
            timestamp = datetime.strptime(asset['quote']['GBP']['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ")

            print(f'Ready for psql write: {price} {timestamp}')
            data_to_insert = (asset_name, price, timestamp)
            conn_cursor.execute(insert_query, data_to_insert)

        conn_cursor.connection.commit()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn_cursor.close()

    return


def fetch_data_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM on_your_market_prices")
    data = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(data, columns=['id', 'coin_name', 'price', 'timestamp'])

    return df
