
import streamlit as st
import yfinance as yf
import pandas as pd
import time
import requests

# CSS kód pro změnu barvy pozadí

st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)

st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

def get_data():
    # Seznam tickrů
    tickers = ["EURCZK=X", "CZK=X", "FPXAA.PR", "CEZ.PR", "BZ=F", "^GSPC","^IXIC", "BTC-USD"]

    # Vytvoření prázdného dataframeu
    data = pd.DataFrame()

    # nejriv stahnu nova data za vcerejsek (uzaviraci hodnota)
    source_website = "https://finance.yahoo.com/quote/FPXAA.PR?p=FPXAA.PR&.tsrc=fin-srch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(source_website, headers=headers).text
    source = pd.read_html(html_content); source = source[0]
    scraped = pd.DataFrame(source)
    scraped = scraped[1].iloc[0]

    # Procházení jednotlivých tickerů
    for ticker in tickers:

        # Získání historických dat (Close)
        current_close = yf.Ticker(ticker).history(period='1d', interval='1m')["Close"].iloc[-1]
        history = yf.Ticker(ticker).history(period='5d')["Close"]
        previous_close = history.iloc[-2] if len(history) > 1 else scraped ## problem u prazske burzy z nejakoho duvodu zmizela historicka data
        
        # Výpočet procentuální změny
        percentage_change = ((current_close - previous_close) / previous_close) * 100

        # Přidání řádku do dataframeu
        data = pd.concat([data, pd.DataFrame({"Ticker": [ticker], "Close": [current_close], "previ_close": [previous_close],"Change%": [percentage_change]})])

    return data


columns1 = st.empty()
columns2 = st.empty()
columns3 = st.empty()
display_close = st.empty()  # vytváříme prázdný objekt k zobrazení hodnoty 'Close'

while True:
    data = get_data()
    data["Close"] = data["Close"].round(2)
    data["Change%"] = data["Change%"].round(2).astype(str)

    # Převod na string s oddělovači tisíců
    data["Close"] = data["Close"].apply(lambda x: '{:,}'.format(x).replace(',', ' '))

    # Upravené rozložení sloupců s přidaným prázdným sloupcem
    col1, col2, col3, col4, col5, col6, col7, col8 = columns1.columns(8)
    col1.metric("EUR", data['Close'].iloc[0] + " CZK", data['Change%'].iloc[0] + "%")
    col2.metric("USD", data['Close'].iloc[1] + " CZK", data['Change%'].iloc[1] + "%")
    col3.metric("ČEZ", data['Close'].iloc[3] + " CZK", data['Change%'].iloc[3] + "%")
    # col4.metric("PX - Pražská burza", data['Close'].iloc[2] + " CZK", data['Change%'].iloc[2] + "%")
    col4.metric("Ropa Brent", data['Close'].iloc[4] + " $", data['Change%'].iloc[4] + "%")
    col5.metric("S&P 500", data['Close'].iloc[5] + " $", data['Change%'].iloc[5] + "%")
    col6.metric("NASDAQ", data['Close'].iloc[7] + " $", data['Change%'].iloc[7] + "%")
    # col8.metric("Bitcoin", data['Close'].iloc[6] + " $", data['Change%'].iloc[6] + "%")
    time.sleep(20)


