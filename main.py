from fastapi import FastAPI
import hmac, hashlib, time
import httpx
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://contract.mexc.com"

def sign_request(params, secret):
    sorted_params = sorted(params.items())
    query_string = "&".join(["{}={}".format(k, v) for k, v in sorted_params])
    return hmac.new(secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

async def send_order(symbol, vol, side, leverage):
    params = {
        "api_key": API_KEY,
        "req_time": str(int(time.time() * 1000)),
        "symbol": symbol,
        "price": 0,
        "vol": vol,
        "side": side,
        "type": 1,
        "open_type": 1,
        "position_id": 0,
        "leverage": leverage,
    }
    params["sign"] = sign_request(params, API_SECRET)

    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.post(BASE_URL + "/api/v1/private/order/submit", data=params)
        return res.text

@app.get("/")
def root():
    return {"message": "✅ Bot MEXC đang chạy trên Render"}

@app.get("/short")
async def short():
    return await send_order("BTC_USDT", 0.1, 3, 10)

@app.get("/close")
async def close():
    return await send_order("BTC_USDT", 0.1, 4, 10)
