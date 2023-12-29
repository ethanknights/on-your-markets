# appy.py
#
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from utils import (
    create_psql_connection,
    call_coinmarketcap_api,
    process_coinmarketcap_api,
    insert_psql_db_coinmarketcap,
    fetch_data_from_db
)
import plotly.express as px

env = 'dev'
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path=dotenv_path)


def main():

    # Request and write latest data from APIs
    conn = create_psql_connection()

    # raw_coins = call_coinmarketcap_api()
    # coins = process_coinmarketcap_api(raw_coins=raw_coins)
    #
    # insert_psql_db_coinmarketcap(conn_cursor=conn.cursor(), data=coins)

    df = fetch_data_from_db(conn)

    for coin_name in df['coin_name'].unique():
        st.title(f"{coin_name} Price")
        coin_data = df[df['coin_name'] == coin_name]

        # streamlit plot (inflexible)
        # st.line_chart(data=coin_data, x='timestamp',y='price', use_container_width=True)

        # plotly plot (more customisable)
        fig = px.line(coin_data, x='timestamp', y='price', markers=True, line_shape='linear', title=f"{coin_name}")
        st.plotly_chart(fig)

    print('debug')


if __name__ == '__main__':
    main()