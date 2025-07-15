import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

# Utility function to ensure a column is a 1D Series
def ensure_series(col):
    return col.iloc[:, 0] if isinstance(col, pd.DataFrame) else col

st.title("NSE500 Stock Screener & Predictor")
st.write("Screen and predict qualifying stocks for the next trading session using technical indicators.")

uploaded_file = st.file_uploader("Upload your nse500.csv file", type="csv")
if uploaded_file is not None:
    stocks_df = pd.read_csv(uploaded_file)
    stock_symbols = stocks_df['Stock_Code'].tolist()
else:
    st.warning("Please upload the nse500.csv file to proceed.")
    st.stop()

def analyze_single_stock(stock):
    ticker = stock + ".NS"
    try:
        # Use multi_level_index=False to avoid MultiIndex columns
        df = yf.download(
            ticker,
            period="250d",
            interval="1d",
            progress=False,
            multi_level_index=False
        )
        if df.empty:
            return None

        # Ensure all columns are 1D Series
        close = ensure_series(df['Close'])
        high = ensure_series(df['High'])
        low = ensure_series(df['Low'])
        volume = ensure_series(df['Volume'])

        df['RSI'] = ta.momentum.RSIIndicator(close=close).rsi()
        macd = ta.trend.MACD(close=close)
        df['MACD_Hist'] = macd.macd_diff()
        df['MACD_Line'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['Volume_Avg'] = volume.rolling(window=20).mean()
        df['20_SMA'] = close.rolling(window=20).mean()
        df['50_SMA'] = close.rolling(window=50).mean()
        df['200_SMA'] = close.rolling(window=200).mean()
        df['ATR'] = ta.volatility.AverageTrueRange(
            high=high, low=low, close=close
        ).average_true_range()
        adx_ind = ta.trend.ADXIndicator(
            high=high, low=low, close=close, window=14, fillna=False
        )
        df['ADX'] = adx_ind.adx()
        df['DI+'] = adx_ind.adx_pos()
        df['DI-'] = adx_ind.adx_neg()
        df.dropna(inplace=True)
        if df.empty:
            return None
        latest = df.iloc[-1]

        # Trade setup conditions
        conditions = [
            55 < latest["RSI"] < 65,
            latest["MACD_Hist"] > 0,
            latest["MACD_Line"] > latest["MACD_Signal"],
            (latest['Volume'] > latest["Volume_Avg"]) and (latest['Close'] > df.iloc[-2]['Close']),
            latest["20_SMA"] > latest["50_SMA"] > latest["200_SMA"]
        ]
        if all(conditions):
            return {
                "Stock": stock,
                "Close Price": f"₹{latest['Close']:.2f}",
                "RSI": f"{latest['RSI']:.2f}",
                "MACD Histogram": f"{latest['MACD_Hist']:.5f}",
                "MACD Line": f"{latest['MACD_Line']:.5f}",
                "MACD Signal": f"{latest['MACD_Signal']:.5f}",
                "Current Volume": f"{int(latest['Volume']):,}",
                "Average Volume (20)": f"{int(latest['Volume_Avg']):,}",
                "20 SMA": f"₹{latest['20_SMA']:.2f}",
                "50 SMA": f"₹{latest['50_SMA']:.2f}",
                "200 SMA": f"₹{latest['200_SMA']:.2f}",
                "ATR": f"₹{latest['ATR']:.2f}",
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            return None
    except Exception as e:
        st.error(f"Error downloading data for {stock}: {e}")
        return None

if st.button("Run Screener"):
    qualifying_stocks = []
    progress = st.progress(0)
    for i, stock in enumerate(stock_symbols):
        result = analyze_single_stock(stock)
        if result:
            qualifying_stocks.append(result)
        progress.progress((i + 1) / len(stock_symbols))
    if qualifying_stocks:
        qualifying_df = pd.DataFrame(qualifying_stocks)
        qualifying_df.sort_values(by="RSI", ascending=False, inplace=True)
        st.success(f"Found {len(qualifying_stocks)} qualifying stocks.")
        st.dataframe(qualifying_df)
        csv = qualifying_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", csv, "qualified_stocks.csv", "text/csv")
    else:
        st.warning("No stocks qualified for the trade setup.")
