import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from PIL import Image
import plotly.subplots as sp


page_bg_img = """
<style>
[data-testid="stSidebar"] {
background-color: #e5e5f7;
opacity: 1;
background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #e5e5f7 4px ), repeating-linear-gradient( #ffb00d55, #ffb00d );
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# Define the color palette
PRIMARY_COLOR = "#e8b924"


image = Image.open('bitcoin.png')
st.image(image, width=250)


# Set the color of the page title and subtitle
st.markdown(f"""<h1 style='color:{PRIMARY_COLOR};font-size:50px;'>Bitcoin Price App</h1>""", unsafe_allow_html=True)
st.write("""
* **Python libraries:** pandas, streamlit, yfinance, plotly
Shown are the stock **Hourly Closing Price** , ***Candlestick Chart*** and ***Daily Closing Price*** of Bitcoin!
""")
         

sidebar = st.sidebar.container()

# Add information about Bitcoin
st.markdown(f"""<h1 style='color:{PRIMARY_COLOR};font-size:35px;'>What is Bitcoin?</h1>""", unsafe_allow_html=True)
st.write("Bitcoin is a decentralized digital currency that was created in 2009 by an unknown person or group of people using the name Satoshi Nakamoto. It is a decentralized system, meaning that it operates on a peer-to-peer network without a central authority. Transactions are recorded on a public ledger called the blockchain, and users can send and receive bitcoins without the need for a middleman like a bank.")
st.write("Bitcoin has become a popular form of investment and has been used as a means of payment for goods and services. Its price is determined by supply and demand, and it is widely considered to be a store of value, similar to gold.")

# Add instructions on how to use the app
st.write(f"""<h1 style='color:{PRIMARY_COLOR};font-size:35px;'>Instructions</h1>""", unsafe_allow_html=True)
st.write("""
1. Use the "Select a date range" section on the left-side panel to select the start and end dates for the data.
2. Use the "Select the Time Period" dropdown menu to choose a predefined time period, or leave it set to "All" to see all available data.
3. The app will display the Hourly Closing Price, Candlestick Chart, and Daily Closing Price of Bitcoin based on the selected date range.
""")



with sidebar:
    st.sidebar.subheader("Select a date range")
    start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2022-1-28"))
    end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2023-3-28"))
    date_range = st.sidebar.selectbox("Select the Time Period", ["1 Hour", "5 Days", "1 Month", "3 Months", "6 Months", "1 Year", "All"])


# Add conditionals to set the date range based on the selected option
if date_range == "1 Hour":
    end_date = pd.to_datetime("now")
    start_date = end_date - pd.Timedelta(hours=1)
elif date_range == "5 Days":
    end_date = pd.to_datetime("now")
    start_date = end_date - pd.Timedelta(days=5)
elif date_range == "1 Month":
    end_date = pd.to_datetime("now")
    start_date = end_date - pd.Timedelta(days=30)
elif date_range == "3 Months":
    end_date = pd.to_datetime("now")
    start_date = end_date - pd.Timedelta(days=90)
elif date_range == "6 Months":
    end_date = pd.to_datetime("now")
    start_date = end_date - pd.Timedelta(days=180)
elif date_range == "1 Year":
    end_date = pd.to_datetime("now")
    start_date = end_date - pd.Timedelta(days=365)
else:
    start_date = pd.to_datetime("2022-1-28")
    end_date = pd.to_datetime("2023-3-28")


tickerSymbol = 'BTC-USD'    

interval = '1h'
tickerDf = yf.download(tickerSymbol, start=start_date, end=end_date, interval=interval)

tickerDf.index = pd.to_datetime(tickerDf.index)



# Resample the data to hourly
tickerDf_hourly = tickerDf.resample('H').mean()

# Create Candlestick
fig = go.Figure(data=[go.Candlestick(
    x=tickerDf.index,
    open=tickerDf['Open'],
    high=tickerDf['High'],
    low=tickerDf['Low'],
    close=tickerDf['Close']
)])

# Set the layout for the candlestick chart
fig.update_layout(
    title=tickerSymbol + ' Candlestick Chart (Hourly)',
    title_font=dict(size=24,color='#333'),
font=dict(size=12, color='#333'),
plot_bgcolor='#f5f5f5', # Set background color
paper_bgcolor='white',
xaxis_title='Date',
xaxis_tickformat='%Y-%m-%d %H:%M:%S',
xaxis_rangeslider_visible=False,
yaxis_title='Price ($)',
legend=dict( # Add a legend
orientation='h',
yanchor='bottom',
y=1.02,
xanchor='right',
x=1,
font=dict(size=12, color='#333')
)
)

# Resample the data to hourly
if date_range == "1 Hour":
    tickerDf_hourly = tickerDf.resample('H').mean()
    xaxis_format = '%H:%M:%S'
else:
    tickerDf_hourly = tickerDf
    xaxis_format = '%Y-%m-%d'

hourly_line_fig = go.Figure(data=[go.Scatter(
    x=tickerDf_hourly.index,
    y=tickerDf_hourly['Close'],
    line=dict(color=PRIMARY_COLOR),
    mode='lines' # Set mode to 'lines' to remove markers
)])

# Set the layout for the hourly line chart
hourly_line_fig.update_layout(
    title=tickerSymbol + ' Hourly Closing Price',
    title_font=dict(size=24, color='#333'),
    font=dict(size=12, color='#333'),
    plot_bgcolor='#f5f5f5', # Set background color
    paper_bgcolor='white',
    xaxis_title='Date',
    xaxis_tickformat=xaxis_format,
    yaxis_title='Price ($)',
    legend=dict( # Add a legend
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=12, color='#333')
    )
)
# Display the hourly line chart
st.plotly_chart(hourly_line_fig)



# Create Candlestick
fig = go.Figure(data=[go.Candlestick(
    x=tickerDf.index,
    open=tickerDf['Open'],
    high=tickerDf['High'],
    low=tickerDf['Low'],
    close=tickerDf['Close']
)])

# Set the layout for the candlestick chart
fig.update_layout(
    title=tickerSymbol + ' Candlestick Chart',
    title_font=dict(size=24, color='#333'),
    font=dict(size=12, color='#333'),
    plot_bgcolor='#f5f5f5',  # Set background color
    paper_bgcolor='white',
    legend=dict(  # Add a legend
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=12, color='#333')
    )
)

st.plotly_chart(fig)

# Resample the data to daily
tickerDf_daily = tickerDf.resample('D').mean()


# Create a subplot with two charts side by side
fig = sp.make_subplots(rows=1, cols=2)

# Add the bar chart to the first subplot
fig.add_trace(go.Bar(
    x=tickerDf_daily.index,
    y=tickerDf_daily['Close'],
    marker=dict(color=PRIMARY_COLOR),
), row=1, col=1)

# Set the layout for the first subplot
fig.update_layout(
    title=tickerSymbol + ' Daily Closing Price',
    title_font=dict(size=30, color='#333'),
    font=dict(size=12, color='#333'),
    plot_bgcolor='#f5f5f5',  # Set background color
    paper_bgcolor='white',
    xaxis_title='Date',
    xaxis_tickformat='%Y-%m-%d',
    yaxis_title='Price ($)'
)

# Add the line chart to the second subplot
fig.add_trace(go.Scatter(
    x=tickerDf_daily.index,
    y=tickerDf_daily['Close'],
    line=dict(color=PRIMARY_COLOR),
    mode='lines'
), row=1, col=2)

# Set the layout for the second subplot
fig.update_layout(
    title=tickerSymbol + ' Daily Closing Price',
    title_font=dict(size=30, color='#333'),
    font=dict(size=12, color='#333'),
    plot_bgcolor='#f5f5f5',  # Set background color
    paper_bgcolor='white',
    xaxis_title='Date',
    xaxis_tickformat='%Y-%m-%d',
    yaxis_title='Price ($)'
)

st.plotly_chart(fig)

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=Space+Mono&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Playfair Display', serif;
			}

			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
# --- hide streamlit style ---

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)
