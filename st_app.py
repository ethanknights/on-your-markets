# st_appy.py
# Use utils function to get data and display through streamlit (see app.py first).

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from utils import call_coinmarketcap_api


# Load environment variables
env = 'dev'
dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path=dotenv_path)

# Function to call CoinMarketCap API


def main():
    st.set_page_config(layout="wide")
    # st.write("This is a Streamlit app. To run it, use the command: streamlit run filename.py")


    # Get data from CoinMarketCap API
    data = call_coinmarketcap_api()

    # Streamlit app
    st.title("Latest Cryptocurrency Data")

    if data:

        for crypto_data in data['data']:
            print(crypto_data)

            quote_data = crypto_data['quote']['GBP']


            st.write(quote_data['price'])
            st.subheader(f"({crypto_data['symbol']})")
            st.write(f"Rank: {crypto_data['cmc_rank']}")

        # Loop through keys in the JSON data
        st.subheader("Key-Value Pairs:")
        for key, value in crypto_data.items():
            st.write(f"{key}: {value}")

        # Plot data
        st.subheader("Price and Market Cap Over Time:")
        df = pd.DataFrame({'Price (GBP)': [quote_data['price']], 'Market Cap (GBP)': [quote_data['market_cap']]})
        st.line_chart(df)

    else:
        st.error("Unable to fetch data from CoinMarketCap API.")

# Run the Streamlit app
if __name__ == '__main__':
    main()
