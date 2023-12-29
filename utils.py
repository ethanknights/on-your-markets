# utils.py
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
import streamlit as st

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