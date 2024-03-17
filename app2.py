import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# 銘柄リスト

tickers = {
    'GOLD': '1540.T',  # 日本の証券コードにはサフィックスとして .T を付ける
    'WTI　OIL': '1671.T',  # 同上
    'Sony': '6758.T',  # 同上
    'NVIDIA': 'NVDA',  # NASDAQ上場のためサフィックスは不要
    'Tesla': 'TSLA',  # 同上
    'Google': 'GOOGL'  # すでにリストに存在
}


# Streamlitのサイドバーで日付を選択
start_date = st.sidebar.date_input('開始日', datetime.now().date().replace(year=datetime.now().year - 3))
end_date = st.sidebar.date_input('終了日', datetime.now().date())

# yfinanceを使用してデータを取得する関数
def get_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Adj Close']

# 描画するデータフレームの初期化
df = pd.DataFrame()

# 選択された銘柄ごとにデータを取得し、データフレームに追加
for name, ticker in tickers.items():
    df[name] = get_data(ticker, start_date, end_date)

# データフレームのインデックスをDateTime型に変換
df.index = pd.to_datetime(df.index)

# matplotlibを使用してグラフを描画
plt.figure(figsize=(15, 5))
for column in df.columns:
    plt.plot(df.index, df[column], label=column)

# X軸のフォーマットを調整
locator = mdates.AutoDateLocator()  # 自動で日付の間隔を決定
formatter = mdates.ConciseDateFormatter(locator)  # 日付のフォーマットを調整
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)

# X軸とY軸のラベル、凡例、タイトルを設定
plt.xlabel('Date')
plt.ylabel('Adjusted Close Price')
plt.title('Selected Stocks Adjusted Close Price Over Time')
plt.legend()

# X軸の目盛りを自動的に回転
plt.xticks(rotation=45)

# グラフのレイアウトを自動調整
plt.tight_layout()

st.pyplot(plt)
