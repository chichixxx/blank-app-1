import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Over/Under Analyzer", layout="wide")
st.title("Over/Under Market Analysis Tool")

np.random.seed(42)
price = 100 + np.cumsum(np.random.randn(600) * 0.1)
time = pd.date_range(start="2025-05-24 09:00:00", periods=600, freq="S")
df = pd.DataFrame({'time': time, 'price': price})
df['SMA_20'] = df['price'].rolling(window=20).mean()
df['volatility'] = df['price'].rolling(window=20).std()

df.dropna(inplace=True)
df['signal'] = np.where(
    (df['price'] > df['SMA_20']) & (df['volatility'] < 0.12), 'Over',
    np.where((df['price'] < df['SMA_20']) & (df['volatility'] < 0.12), 'Under', 'No Signal')
)

st.subheader("Signal Summary")
st.write(df['signal'].value_counts())
st.subheader("Latest Signals")
st.write(df[['time', 'price', 'SMA_20', 'volatility', 'signal']].tail(10))

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['time'], df['price'], label='Price', color='black')
ax.plot(df['time'], df['SMA_20'], label='SMA 20', linestyle='--', color='orange')
ax.scatter(df[df['signal'] == 'Over']['time'], df[df['signal'] == 'Over']['price'], color='green', label='Over', s=10)
ax.scatter(df[df['signal'] == 'Under']['time'], df[df['signal'] == 'Under']['price'], color='red', label='Under', s=10)
ax.legend()
st.pyplot(fig)