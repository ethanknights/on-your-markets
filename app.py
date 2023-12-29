# appy.py
#
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from utils import call_coinmarketcap_api
from datetime import datetime
import psycopg2


# Load environment variables
env = 'dev'
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path=dotenv_path)


def main():

    # get data
    raw_coins = call_coinmarketcap_api()

    # config_coins = { # Version for sandbox call as they change!
    #     'BTC_ID': int(coins['data'][0]['id']),
    #     'ETH_ID': int(coins['data'][1]['id']),
    #                 }
    config_coins = {
        'BTC_ID': int(1),
        'ETH_ID': int(1027),
        'BNB_ID': int(1839),
        'SOL_ID': int(5426),
    }

    coins = [coin for coin in raw_coins['data'] if coin['id'] in config_coins.values()]
    assert coins, 'No `coins` present after filter'

    for coin in coins:
        price = int(round(coin['quote']['GBP']['price']))  # rounding due to volatility
        timestamp = datetime.strptime(coin['quote']['GBP']['last_updated'], "%Y-%m-%dT%H:%M:%S.%fZ")

        print(f'{price} {timestamp}')


if __name__ == '__main__':
    main()