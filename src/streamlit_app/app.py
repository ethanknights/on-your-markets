# app.py
#
from dotenv import load_dotenv
import requests
import streamlit as st
from src.common.utils import (
    create_psql_connection,
    call_coinmarketcap_api,
    process_coinmarketcap_api,
    insert_psql_db_coinmarketcap,
    fetch_coins_data_from_db,
    plot_coins,
    call_polygon_api,
    insert_psql_db_polygon,
    fetch_stocks_data_from_db,
    plot_stocks,
)


env = 'dev'
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path=dotenv_path)


def main():

    conn = create_psql_connection()

    st.title('Tracker - On Your Markets')
    # Define buttons to trigger data collection
    button_col_left, button_col_right = st.columns(2)

    if button_col_left.button("Collect Latest Data From CoinMarketCap"):
        raw_coins = call_coinmarketcap_api()
        coins = process_coinmarketcap_api(raw_coins=raw_coins)
        insert_psql_db_coinmarketcap(conn_cursor=conn.cursor(), data=coins)

    if button_col_right.button("Collect Latest Data From stocks"):
        symbol_names = ['IBM', 'VOO']
        for symbol_name in symbol_names:
            raw_stock = call_polygon_api(symbol_name)
            insert_psql_db_polygon(conn_cursor=conn.cursor(), raw_stock=raw_stock)
            st.success("Data collection successful!")

    # Fetch & plot data from postgresql
    st.subheader('Digital Currency')
    st.caption('Source: Coin Market Cap')
    coins_data_response = requests.get('http://127.0.0.1:8000/read_coins_data_from_psql_db')
    df_coins = coins_data_response.json()
    plot_coins(df_coins)  # 2x2 grid

    st.subheader('Stocks')
    st.caption('Source: Polygon.io')
    df_stocks = fetch_stocks_data_from_db(conn)
    plot_stocks(df_stocks)  # 1x2 grid

    print('debug')


if __name__ == '__main__':
    main()
