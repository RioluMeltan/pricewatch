# Import statements
import streamlit as st
import MainPage
import CurrencyConv
import MarginCalc
from PIL import Image

# Static class to access pages
class Navigation: 

    # Main page
    def mainPage(): 

        # Page definitions
        st.set_page_config(layout = 'wide')

        # Initializing persistent storage for watches
        if 'watches' not in st.session_state: 
            st.session_state.watches = []

        # UI elements
        st.title('PriceWatch: A Price Comparison Tool for Fair Resale Valuation of Luxury Watches')
        st.sidebar.image(Image.open())
        st.sidebar.text('Add Watch')
        st.sidebar.text('Enter Watch Below')
        watchInput = st.sidebar.text_input('Enter watch here')
        searchWatches = st.sidebar.button('Search for Watch')
        importList = st.sidebar.button('Import List from Clipboard')

        # Column formatting for buttons
        col_1, col_2, col_3 = st.columns([1, 1, 1])
        with col_1: 
            currencyConvButton = st.button('Currency Converter')

        with col_2: 
            marginCalcButton = st.button('Margin Calculator')

        with col_3: 
            exportListButton = st.button('Export Watchlist')

        if currencyConvButton: 
            st.session_state.page = 'CurrencyConv'

        if marginCalcButton: 
            st.session_state.page = 'MarginCalc'