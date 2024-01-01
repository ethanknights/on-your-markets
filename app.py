# appy.py
#
from dotenv import load_dotenv
import streamlit as st
from utils import (
    create_psql_connection,
    call_coinmarketcap_api,
    process_coinmarketcap_api,
    insert_psql_db_coinmarketcap,
    fetch_coins_data_from_db,
    plot_coins
)

env = 'dev'
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path=dotenv_path)


def main():

    conn = create_psql_connection()

    # Define buttons to trigger data collection
    button_col_left, button_col_right = st.columns(2)

    if button_col_left.button("Collect Latest Data From CoinMarketCap"):
        raw_coins = call_coinmarketcap_api()
        coins = process_coinmarketcap_api(raw_coins=raw_coins)
        insert_psql_db_coinmarketcap(conn_cursor=conn.cursor(), data=coins)
        st.success("Data collection successful!")

    if button_col_right.button("Collect Latest Data From stocks"):
        # raw_coins = call_coinmarketcap_api()
        # coins = process_coinmarketcap_api(raw_coins=raw_coins)
        # insert_psql_db_coinmarketcap(conn_cursor=conn.cursor(), data=coins)
        st.success("Warning Not Implemented Yet")

    # Fetch & plot data from postgresql
    df = fetch_coins_data_from_db(conn)
    plot_coins(df)  # Plot coins in 2x2 grid

    print('debug')


if __name__ == '__main__':
    main()
