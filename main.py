import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date
from prophet import *
from prophet.plot import plot_plotly
from plotly import graph_objs as go


home_page_tab, compare_stocks_tab, forcast_stocks_tab= st.tabs(["Home Page","Compare Stocks", "Forcast Stocks"])


with home_page_tab:
    st.header("Building a Profitable Financial Strategy Through Focasting of Real-Time Stock Market Report Analysis")
    st.subheader("By Oluwafemi Adeleke")
    st.markdown("""
    This project is expected to help me do... This project is expected to help me do 
    This project is expected to help me do This project is expected to help me do
    This project is expected to help me do This project is expected to help me do 
    
    This project is expected to help me do This project is expected to help me do .
    This project is expected to help me do This project is expected to help me do .
    This project is expected to help me do... This project is expected to help me do 
    This project is expected to help me do This project is expected to help me do
    This project is expected to help me do This project is expected to help me do 
    
    This project is expected to help me do This project is expected to help me do .
    This project is expected to help me do This project is expected to help me do .
    
    """)
    
    
    st.markdown("[Yahoo Finance Python API](https://pypi.org/project/yfinance/)")
    st.markdown("[Facebook Prophet](https://facebook.github.io/prophet/docs/quick_start.html)")
    st.markdown("[Streamlit ](https://docs.streamlit.io/)")




with compare_stocks_tab:
    st.title('Stock Analyses')

    tickers = ('TSLA', 'AAPL','MSFT',  'AMZN', 'GOOG','AAPL', 'ORCL', 'PREM.L', 'UKOG.L', 'KOD.L', 'TOM.L', 'VELA.L')

    dropdown = st.multiselect('Pick your assets', tickers)

    start_date = st.date_input('Start Date', value=pd.to_datetime('2022-11-01'))
    end_date = st.date_input('End Date', value=pd.to_datetime('today'))



    def releativeret(df):
        rel = df.pct_change()
        cumret = (1+rel).cumprod() -1
        cumret = cumret.fillna(0)
        return cumret

    if len(dropdown) > 0:
        df = releativeret(yf.download(dropdown,start_date, end_date)['Adj Close'])
        st.line_chart(df)

with forcast_stocks_tab:
    START = st.date_input('Date', value=pd.to_datetime('2022-11-01'))
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title('Stock Forecast App')

    stocks = ('TSLA', 'AAPL','MSFT',  'AMZN', 'GOOG','AAPL', 'ORCL', 'PREM.L', 'UKOG.L', 'KOD.L', 'TOM.L', 'VELA.L')
    selected_stock = st.selectbox('Select dataset for prediction', stocks)

    n_years = st.slider('Years of prediction:', 1, 4)
    period = n_years * 365


    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data


    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')

    st.subheader('Raw data')
    st.write(data.tail())

    # Plot raw data
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)
