import streamlit as st

# Page definitions
st.set_page_config(layout = 'wide')

# Variable definitions
mainLabel = st.title('PriceWatch: A Price Comparison Tool for Fair Resale Valuation of Luxury Watches')
logo = st.sidebar.image(Image.open())
addWatch = st.sidebar.text('Add Watch')
enterWatch = st.sidebar.text('Enter Watch Below')
watchTextBox = st.sidebar.text_input('Enter watch here')
searchWatchButton = st.sidebar.button('Search for Watch')
importListButton = st.sidebar.button('Import List from Clipboard')
st.session_state.watches = [] # Goes to session_state for persistent storage (MAYBE change? Not sure if this'll work.)

# Column formatting for buttons
col_1, col_2, col_3 = st.columns([1, 1, 1])
with col_1: 
    currencyConvButton = st.button('Currency Converter')

with col_2: 
    marginCalcButton = st.button('Margin Calculator')

with col_3: 
    exportListButton = st.button('Export Watchlist')