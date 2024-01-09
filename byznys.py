import streamlit as st
import yfinance as yf
import pandas as pd
import requests

def get_data():
    # Seznam tickerů
    tickers = ["EURCZK=X", "CZK=X", "CEZ.PR", "BZ=F", "^GSPC", "^IXIC", "BTC-USD"] ## "FPXAA.PR", Prazska burza ma problem s historickymi daty na yahoo finance, ozkousim to bez a pak ji kdyztak pridam

    # Vytvoření prázdného DataFrame
    data = pd.DataFrame()

    # Stažení nových dat pro FPXAA.PR (uzavírací hodnota)
    source_website = "https://finance.yahoo.com/quote/FPXAA.PR?p=FPXAA.PR&.tsrc=fin-srch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    html_content = requests.get(source_website, headers=headers).text
    source = pd.read_html(html_content); source = source[0]
    scraped = pd.DataFrame(source)
    scraped = scraped[1].iloc[0]

    # Procházení jednotlivých tickerů
    for ticker in tickers:
        ticker_obj = yf.Ticker(ticker)
        current_close = ticker_obj.history(period='1d', interval='1m')["Close"].iloc[-1]
        history = ticker_obj.history(period='5d')["Close"]

        # Získání historických dat za posledních 6 měsíců a výběr každé třetí hodnoty
        six_months_history = ticker_obj.history(period='6mo')["Close"].iloc[::3].round(2).tolist()

        # Použití scraped dat pro FPXAA.PR, jinak normální postup
        previous_close = scraped if ticker == "FPXAA.PR" else history.iloc[-2] if len(history) > 1 else current_close

        # Výpočet procentuální změny
        percentage_change = ((current_close - previous_close) / previous_close) * 100

        # Přidání řádku do DataFrame
        data = pd.concat([data, pd.DataFrame({
            "Ticker": [ticker], 
            "Close": [current_close], 
            "previ_close": [previous_close], 
            "Change%": [percentage_change], 
            "6mo_history": [six_months_history]
        })])

    return data

data = get_data()
data["Close"] = data["Close"].round(2)
data["Change%"] = data["Change%"].round(2).astype(str)




# Převod na string s oddělovači tisíců
data["Close"] = data["Close"].apply(lambda x: '{:,}'.format(x).replace(',', ' '))
data['Ticker'].iloc[0] = "EUR"
data['Ticker'].iloc[1] = "USD"
# data['Ticker'].iloc[2] = "PX - Pražská burza"
data['Ticker'].iloc[2] = "ČEZ"
data['Ticker'].iloc[3] = "Ropa Brent"
data['Ticker'].iloc[4] = "S&P 500"
data['Ticker'].iloc[5] = "NASDAQ"
data['Ticker'].iloc[6] = "Bitcoin"

data['Close'].iloc[0] = data['Close'].iloc[0] + " CZK"
data['Close'].iloc[1] = data['Close'].iloc[1] + " CZK"
data['Close'].iloc[2] = data['Close'].iloc[2] + " CZK"
data['Close'].iloc[3] = data['Close'].iloc[3] + " $"
data['Close'].iloc[4] = data['Close'].iloc[4] + " $"
data['Close'].iloc[5] = data['Close'].iloc[5] + " $"
data['Close'].iloc[6] = data['Close'].iloc[6] + " $"


ticker_column = st.column_config.TextColumn(label="", width="small")
price_column = st.column_config.TextColumn(label="Aktuální kurz/cena", width="small")

trend_column = st.column_config.LineChartColumn(label="Trend v posledních 6 měsících", width="large")

data = data[["Ticker","Close","6mo_history"]]


st.dataframe(data,width=650, hide_index=True,column_config={"Ticker":ticker_column,"Close": price_column,"6mo_history": trend_column},height=286)  




