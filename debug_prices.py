import yfinance as yf

# Test with Bitcoin
data = yf.download('BTC-USD', period='2d', progress=False)
print("Data type:", type(data))
print("Data shape:", data.shape)
print("Data columns:", list(data.columns))
print("\nFull data:")
print(data)
print("\nLatest row:")
latest = data.iloc[-1]
print("Type of latest:", type(latest))
print(latest)
print("\nValue of latest['Close']:")
val = latest['Close']
print("Type:", type(val))
print("Value:", val)
print("\nTrying to convert to float:")
try:
    f = float(val)
    print("Success:", f)
except Exception as e:
    print("Error:", e)
