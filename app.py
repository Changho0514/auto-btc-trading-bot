from flask import Flask, render_template_string
import pyupbit
import datetime
import redis 

app = Flask(__name__)

# Redis에 연결
r = redis.StrictRedis(host='localhost', port=6379, db=0)

access = "myaccess"
secret = "mysecret"

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

@app.route('/')
def index():
    # Redis에서 final_k 값을 읽어옴
    final_k = float(r.get('final_k'))

    target_price = get_target_price("KRW-BTC", final_k)
    current_price = get_current_price("KRW-BTC")
    difference = target_price - current_price

    # HTML 페이지 렌더링
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>실시간 자동매매 현황</title>
    </head>
    <body>
        <h1>실시간 자동매매 현황</h1>
        <p>목표가 : {target_price}</p>
        <p>현재가 : {current_price}</p>
        <p>차이 : {difference}</p>
        <p>k값 : {final_k}</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
