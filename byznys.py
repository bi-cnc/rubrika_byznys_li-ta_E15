

import streamlit as st
import yfinance as yf
import pandas as pd

st.markdown("""
<style>
    body {
        font-size: 0.5%;
    }
</style>
""", unsafe_allow_html=True)

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
        history = yf.Ticker(ticker).history(period='5d')["Close"]
        previous_close = history.iloc[-2] if len(history) > 1 else 1422.34 ## problem u prazske burzy z nejakoho duvodu zmizela historicka data
        # Výpočet procentuální změny
        percentage_change = ((current_close - previous_close) / previous_close) * 100

        # Přidání řádku do dataframeu
        data = pd.concat([data, pd.DataFrame({"Ticker": [ticker], "Close": [current_close], "previ_close": [previous_close],"Change%": [percentage_change]})])

    return data



columns1 = st.empty()
columns2 = st.empty()
display_close = st.empty()  # vytváříme prázdný objekt k zobrazení hodnoty 'Close'


while True:
    data = get_data()
    data["Close"] = data["Close"].round(2)
    data["Change%"] = data["Change%"].round(2).astype(str)

    # Převod na string s oddělovači tisíců
    data["Close"] = data["Close"].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    display_close.markdown("<strong>EUR:</strong> " + data['Close'].iloc[0] + "&nbsp;&nbsp;&nbsp;&nbsp;<strong>USD:</strong> "
                            + data['Close'].iloc[1] + "&nbsp;&nbsp;&nbsp;&nbsp;<strong>PX - Pražská burza:</strong> " 
                            + data['Close'].iloc[2], unsafe_allow_html=True)



