import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Stock Market Analyzer",
    layout="wide",
)

st.title("📈 Stock Market Analyzer")
st.markdown("Professional Stock Data Visualization App")

# -------------------------------------------------
# Sidebar Inputs
# -------------------------------------------------
st.sidebar.header("User Input")

stock_symbol = st.sidebar.text_input("Enter Stock Symbol", "AAPL")
start_date = st.sidebar.date_input("Start Date", date(2015, 1, 1))
end_date = st.sidebar.date_input(
    "End Date",
    date.today(),
    max_value=date.today()
)

# -------------------------------------------------
# Data Loading Function
# -------------------------------------------------
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(
        symbol.strip().upper(),
        start=start,
        end=end,
        progress=False
    )
    return data

# -------------------------------------------------
# Fetch Data
# -------------------------------------------------
if stock_symbol:

    data = load_data(stock_symbol, start_date, end_date)

    if data.empty:
        st.error("No data found. Please check the stock symbol or date range.")
    else:
        st.success("Data Loaded Successfully!")

        # -----------------------------------------
        # Display Raw Data
        # -----------------------------------------
        st.subheader("📊 Raw Stock Data (Last 5 Rows)")
        st.dataframe(data.tail())

        # -----------------------------------------
        # Moving Averages
        # -----------------------------------------
        data["MA_100"] = data["Close"].rolling(100).mean()
        data["MA_200"] = data["Close"].rolling(200).mean()

        # -----------------------------------------
        # Plot 1: Closing Price
        # -----------------------------------------
        st.subheader("📈 Closing Price")

        fig1, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(data["Close"])
        ax1.set_title(f"{stock_symbol.upper()} Closing Price")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price")
        st.pyplot(fig1)

        # -----------------------------------------
        # Plot 2: Closing + Moving Averages
        # -----------------------------------------
        st.subheader("📉 Closing Price with Moving Averages")

        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(data["Close"], label="Close")
        ax2.plot(data["MA_100"], label="MA 100")
        ax2.plot(data["MA_200"], label="MA 200")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Price")
        ax2.legend()
        st.pyplot(fig2)

        # -----------------------------------------
        # Statistical Summary
        # -----------------------------------------
        st.subheader("📋 Statistical Summary")
        st.write(data.describe())