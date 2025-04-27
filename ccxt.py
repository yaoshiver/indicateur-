import ccxt
import pandas as pd

exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '1d'
limit = 100

ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = calculate_rsi(df['close'])

def get_signal(rsi_value):
    if rsi_value > 70:
        return 'Surachetée'
    elif rsi_value < 30:
        return 'Survendue'
    else:
        return 'Neutre'

df['Signal'] = df['RSI'].apply(get_signal)

import streamlit as st
import plotly.graph_objects as go

st.title('Analyse RSI des Cryptomonnaies')

crypto = st.text_input('Entrez le symbole de la cryptomonnaie (ex: BTC/USDT):', 'BTC/USDT')

# Récupération et traitement des données comme précédemment

fig = go.Figure()
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['close'], name='Prix de clôture'))
fig.add_trace(go.Scatter(x=df['timestamp'], y=df['RSI'], name='RSI'))

st.plotly_chart(fig)

st.write(f"Signal actuel : {df['Signal'].iloc[-1]}")
