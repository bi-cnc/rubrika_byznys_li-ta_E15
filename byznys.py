import streamlit as st
import yfinance as yf
import pandas as pd

st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)


def get_data():
    # Seznam tickrů
    tickers = ["EURCZK=X", "CZK=X", "FPXAA.PR", "CEZ.PR", "BZ=F", "^GSPC", "BTC-USD", "^IXIC"]

    # Vytvoření prázdného dataframeu
    data = pd.DataFrame()

    # Procházení jednotlivých tickerů
    for ticker in tickers:
        # Získání historických dat (Close)
        current_close = yf.Ticker(ticker).history(period='1d', interval='1m')["Close"].iloc[-1]
        history = yf.Ticker(ticker).history(period='2d')["Close"]
        previous_close = history.iloc[-2] if len(history) > 1 else 1419.08 ## problem u prazske burzy z nejakoho duvodu zmizela historicka data
        # Výpočet procentuální změny
        percentage_change = ((current_close - previous_close) / previous_close) * 100

        # Přidání řádku do dataframeu
        data = pd.concat([data, pd.DataFrame({"Ticker": [ticker], "Close": [current_close], "previ_close": [previous_close],"Change%": [percentage_change]})])

    return data



columns1 = st.empty()
columns2 = st.empty()

while True:
    data = get_data()
    data["Close"] = data["Close"].round(2)
    data["Change%"] = data["Change%"].round(2).astype(str)

    # Převod na string s oddělovači tisíců
    data["Close"] = data["Close"].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    col1, col2, col3, col4 = columns1.columns(4)
    col1.metric("EUR", data['Close'].iloc[0] + " CZK", data['Change%'].iloc[0] + "%")
    col2.metric("USD", data['Close'].iloc[1] + " CZK", data['Change%'].iloc[1] + "%")
    col3.metric("PX - Pražská burza", data['Close'].iloc[2] + " CZK", data['Change%'].iloc[2] + "%")
    col4.metric("ČEZ", data['Close'].iloc[3] + " CZK", data['Change%'].iloc[3] + "%")

    col1, col2, col3, col4 = columns2.columns(4)
    col1.metric("Ropa Brent", data['Close'].iloc[4] + " $", data['Change%'].iloc[4] + "%")
    col2.metric("S&P 500", data['Close'].iloc[5] + " $", data['Change%'].iloc[5] + "%")
    col3.metric("NASDAQ", data['Close'].iloc[7] + " $", data['Change%'].iloc[7] + "%")
    col4.metric("Bitcoin", data['Close'].iloc[6] + " $", data['Change%'].iloc[6] + "%")


