import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import requests
import ta
import xml.etree.ElementTree as ET

# App Title
st.title("📈 Stock Market Analysis with Technical Indicators + News")

# Popular stock symbols for dropdown
popular_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'TCS.NS', 'INFY.NS', 'RELIANCE.NS', 'HDFCBANK.NS', 'SBIN.NS', 'ICICIBANK.NS', 'Custom...']
selected = st.selectbox("Select Stock Symbol", popular_symbols, index=0)
if selected == 'Custom...':
    symbol = st.text_input("Or enter a custom Stock Symbol (e.g., NFLX, BAJAJ-AUTO.NS)", "AAPL")
else:
    symbol = selected

# Date range
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

# Load data
df = yf.download(symbol, start=start_date, end=end_date)

if df.empty:
    st.error(f"No data found for symbol: {symbol}. Please check the symbol and try again.")
    st.stop()

# Flatten multi-level columns (just in case)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = ['_'.join(col).strip() for col in df.columns.values]

# Remove symbol suffix from columns if present (e.g., 'Close_AAPL' -> 'Close')
suffix = f"_{symbol.upper()}"
df.columns = [col[:-len(suffix)] if col.endswith(suffix) else col for col in df.columns]

st.write('Data columns:', list(df.columns))  # Debug: Show columns

if 'Close' not in df.columns:
    st.error(f"The 'Close' column is missing from the data. Columns available: {list(df.columns)}. Please check the symbol or try again later.")
    st.stop()

# Technical indicators
try:
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    rolling_std = df['Close'].rolling(window=20).std()
    df['Upper'] = df['SMA_20'] + (2 * rolling_std)
    df['Lower'] = df['SMA_20'] - (2 * rolling_std)

    # RSI and MACD
    rsi = ta.momentum.RSIIndicator(df['Close']).rsi()
    macd = ta.trend.MACD(df['Close'])
    df['RSI'] = rsi
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
except Exception as e:
    st.warning(f"Technical indicator calculation failed: {e}")

# Charts
st.subheader("📊 Price and Bollinger Bands")
required_cols = ['Close', 'SMA_20', 'Upper', 'Lower']
if all(col in df.columns for col in required_cols):
    st.line_chart(df[required_cols])
else:
    st.warning(f"Some columns are missing for the Bollinger Bands chart: {', '.join([col for col in required_cols if col not in df.columns])}")

st.markdown("""
🟢 **Chart Explanation:**
- `Close`: Daily closing price of the stock.
- `SMA_20`: 20-day Simple Moving Average, used to smooth out short-term fluctuations.
- `Upper/Lower`: Bollinger Bands, indicating volatility range.
""")

st.subheader("📉 RSI (Relative Strength Index)")
if 'RSI' in df.columns:
    st.line_chart(df[['RSI']])
else:
    st.warning("RSI column missing.")
st.markdown("RSI above 70 may indicate overbought; below 30, oversold.")

st.subheader("📈 MACD (Moving Average Convergence Divergence)")
if 'MACD' in df.columns and 'MACD_Signal' in df.columns:
    st.line_chart(df[['MACD', 'MACD_Signal']])
else:
    st.warning("MACD or MACD_Signal column missing.")
st.markdown("MACD crossing above signal → bullish; below → bearish.")

# 📢 News Section
st.subheader("📰 Latest News for " + symbol)

news_url = f"https://news.google.com/rss/search?q={symbol}+stock"
try:
    news_feed = requests.get(news_url)
    root = ET.fromstring(news_feed.content)
    items = root.findall('.//item')
    if items:
        for art in items[:5]:
            title = art.find('title').text if art.find('title') is not None else 'No Title'
            link = art.find('link').text if art.find('link') is not None else '#'
            st.markdown(f"- **[{title}]({link})**")
    else:
        st.warning("⚠️ No news articles found.")
except Exception as e:
    st.error(f"❌ Failed to fetch news: {e}")

# --- Feedback Section ---
st.markdown("---")
st.header("💬 Feedback")

st.write("We value your feedback! Please let us know your thoughts or suggestions.")

feedback = st.text_area("Your feedback", "")
if st.button("Submit Feedback"):
    if feedback.strip():
        st.success("Thank you for your feedback!")
    else:
        st.warning("Please enter some feedback before submitting.")

st.write("Alternatively, you can fill out our [Google Form](https://forms.gle/your-google-form-link) for more detailed feedback.")
