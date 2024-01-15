# fastAPI_integration.py
from fastapi import FastAPI
from pydantic import BaseModel
from src.common.utils import (
    create_psql_connection,
    fetch_coins_data_from_db,
    fetch_stocks_data_from_db,
)

app = FastAPI()


class AssetData(BaseModel):
    asset_name: str
    price: int
    timestamp: str


@app.get("/read_coins_data_from_psql_db")
async def read_coins_data_from_psql_db():
    conn = create_psql_connection()
    df = fetch_coins_data_from_db(conn)
    return df.to_dict(orient="records")


@app.get("/read_stocks_data_from_psql_db")
async def read_stocks_data_from_psql_db():
    conn = create_psql_connection()
    df = fetch_stocks_data_from_db(conn)
    return df.to_dict(orient="records")
