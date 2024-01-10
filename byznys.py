
import streamlit as st
import yfinance as yf
import pandas as pd
import time
import requests

# CSS kód pro změnu barvy pozadí

st.markdown("""
<style>
    [data-testid="stMetricValue"] {
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

def get_data():
    # Seznam tickrů
    tickers = ["EURCZK=X", "CZK=X","CEZ.PR","BZ=F", "FPXAA.PR", "^GSPC","^IXIC", "BTC-USD","ETH-USD"]

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
    kratsi = data.iloc[:4]
    delsi = data.iloc[4:]

    kratsi["Close"] = kratsi["Close"].round(2)
    delsi["Close"] = delsi["Close"].round(0).astype(int)
    # Převod na string s oddělovači tisíců
    kratsi["Close"] = kratsi["Close"].apply(lambda x: '{:,}'.format(x).replace(',', ' ')).astype(str)
    delsi["Close"] = delsi["Close"].apply(lambda x: '{:,}'.format(x).replace(',', ' ')).astype(str)
    kratsi["Change%"] = kratsi["Change%"].round(2).astype(str)
    delsi["Change%"] = delsi["Change%"].round(2).astype(str)

    # Upravené rozložení sloupců s přidaným prázdným sloupcem
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = columns1.columns(9)
    col1.metric("EUR", kratsi['Close'].iloc[0] + " CZK", kratsi['Change%'].iloc[0] + "%")
    col2.metric("USD", kratsi['Close'].iloc[1] + " CZK", kratsi['Change%'].iloc[1] + "%")
    col3.metric("ČEZ", kratsi['Close'].iloc[2] + " CZK", kratsi['Change%'].iloc[2] + "%")
    col4.metric("Ropa Brent", kratsi['Close'].iloc[3] + " $", kratsi['Change%'].iloc[3] + "%")
    col5.metric("S&P 500", delsi['Close'].iloc[1] + " $", delsi['Change%'].iloc[1] + "%")
    col6.metric("Bitcoin", delsi['Close'].iloc[3] + " $", delsi['Change%'].iloc[3] + "%")
    col7.metric("PX", delsi['Close'].iloc[0] + " CZK", delsi['Change%'].iloc[0] + "%")
    col8.metric("NASDAQ", delsi['Close'].iloc[2] + " $", delsi['Change%'].iloc[2] + "%")
    col9.metric("Ethereum", delsi['Close'].iloc[4] + " $", delsi['Change%'].iloc[4] + "%")

    st.write('''<style>

    [data-testid="column"] {
        width: calc(33.3333% - 1rem) !important;
        flex: 1 1 calc(33.3333% - 1rem) !important;
        min-width: calc(33% - 1rem) !important;
    }
    </style>''', unsafe_allow_html=True)

    time.sleep(120)

