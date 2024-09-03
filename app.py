# TODO : calculate_final_k() 캐싱, 

app = Flask(__name__)

access = "xU8Z9GgjCq7q0onexxhQF3rRosk5hBAv3CC1OB9Q"
secret = "wAoqtClKKsL3dxRdxrhoY861Ap9JbMpeNc0KGCWU"

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

@app.route('/')
def index():
    final_k = bestk.calculate_final_k()
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
        <title>Auto Trading Bot Status</title>
    </head>
    <body>
        <h1>Auto Trading Bot Status</h1>
        <p>Target Price: {target_price}</p>
        <p>Current Price: {current_price}</p>
        <p>Difference: {difference}</p>
        <p>Final k: {final_k}</p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
