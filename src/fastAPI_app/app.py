# fastAPI_integration.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.common.utils import (
    create_psql_connection, insert_psql_db_coinmarketcap, fetch_coins_data_from_db, fetch_stocks_data_from_db)

app = FastAPI()


class assetData(BaseModel):
    asset_name: str
    price: int
    timestamp: str


@app.get("/get_coins_data")
async def get_coins_data():
    conn = create_psql_connection()
    df = fetch_coins_data_from_db(conn)
    return df.to_dict(orient='records')

@app.get("/get_stocks_data")
async def get_stocks_data():
    conn = create_psql_connection()
    df = fetch_stocks_data_from_db(conn)
    return df.to_dict(orient='records')

# @app.post("/collect_coin_data")
# async def collect_coin_data(coin_data: CoinData):
#     conn = create_psql_connection()
#     insert_psql_db_coinmarketcap(
#         conn_cursor=conn.cursor(),
#         data=[{
#             'symbol': coin_data.coin_name,
#             'price': coin_data.price,
#             'timestamp': coin_data.timestamp,
#         }],
#     )
#     return {"status": "Data collection successful!"}


