import yfinance as yf
import pandas as pd
import numpy as np

def get_stock_data(ticker, period="6mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval)
    data.dropna(inplace=True)
    return data

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(series):
    exp1 = series.ewm(span=12, adjust=False).mean()
    exp2 = series.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def add_technical_indicators(df):
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['RSI'] = calculate_rsi(df['Close'])
    df['MACD'], df['MACD_Signal'] = calculate_macd(df['Close'])
    df['BB_High'] = df['Close'].rolling(20).mean() + 2 * df['Close'].rolling(20).std()
    df['BB_Low'] = df['Close'].rolling(20).mean() - 2 * df['Close'].rolling(20).std()
    return df

def get_stock_news(ticker):
    stock = yf.Ticker(ticker)
    try:
        news = stock.news  # list of dicts
        return news
    except Exception:
        return []
