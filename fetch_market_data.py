import json
import datetime
import yfinance as yf

# Indian Standard Time (UTC+5:30)
now_utc = datetime.datetime.now(datetime.timezone.utc)
ist_time = now_utc + datetime.timedelta(hours=5, minutes=30)

tickers = {
    "us_sp500": "^GSPC",
    "us_nasdaq": "^IXIC",
    "asia_nikkei": "^N225",
    "asia_hangseng": "^HSI",
    "brent_crude": "BZ=F",
    "dxy": "DX-Y.NYB",
    "india_vix": "^INDIAVIX",
    "hdfc": "HDFCBANK.NS",
    "reliance": "RELIANCE.NS",
    "icici": "ICICIBANK.NS",
    "infy": "INFY.NS",
    "tcs": "TCS.NS"
}

data_out = {
    "timestamp": ist_time.strftime("%d-%b-%Y %I:%M %p IST"),
    "global": {},
    "heavyweights": {}
}

for key, sym in tickers.items():
    try:
        t = yf.Ticker(sym)
        hist = t.history(period="2d")
        if len(hist) >= 2:
            prev_close = hist['Close'].iloc[-2]
            last_price = hist['Close'].iloc[-1]
            pct = ((last_price - prev_close) / prev_close) * 100
            diff = last_price - prev_close
        elif len(hist) == 1:
            last_price = hist['Close'].iloc[-1]
            prev_close = hist['Open'].iloc[-1]
            pct = ((last_price - prev_close) / prev_close) * 100
            diff = last_price - prev_close
        else:
            last_price, pct, diff = 0, 0, 0
            
        target = data_out["heavyweights"] if key in ["hdfc", "reliance", "icici", "infy", "tcs"] else data_out["global"]
        target[key] = {
            "price": round(float(last_price), 2),
            "pct": round(float(pct), 2),
            "change": round(float(diff), 2)
        }
    except Exception as e:
        print(f"Error fetching {sym}: {e}")

with open("data.json", "w") as f:
    json.dump(data_out, f, indent=2)

print("Market data updated successfully.")
