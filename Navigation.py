# Import statements
import streamlit as st
from MainPage import MainPage
from CurrencyConv import CurrencyConv
from MarginCalc import MarginCalc
from PIL import Image

# Static class to access pages
class Navigation: 

    # Main page static method
    @staticmethod
    def mainPage() -> None: 

        # Page definitions
        st.set_page_config(layout = 'wide')

        # Initializing persistent storage for watches
        if 'watches' not in st.session_state: 
            st.session_state.watches = []

        # UI elements
        st.title('PriceWatch: A Price Comparison Tool for Fair Resale Valuation of Luxury Watches')
        st.sidebar.image(Image.open('assets/logo.png'))
        st.sidebar.title('Add Watch')
        st.sidebar.text('Enter Watch Below')
        watchInput = st.sidebar.text_input('Enter watch here')
        searchWatches = st.sidebar.button('Search for Watch')
        importList = st.sidebar.button('Import List from Clipboard')

        # Column formatting for buttons
        col_1, col_2, col_3 = st.columns([1, 1, 1])
        with col_1: 
            if st.button('Currency Converter'): 
                st.session_state.page = 'CurrencyConv'
                st.rerun()

        with col_2: 
            if st.button('Margin Calculator'): 
                st.session_state.page = 'MarginCalc'
                st.rerun()

        with col_3: 
            if st.button('Export Watchlist'): 
                MainPage.exportList()

        if searchWatches and watchInput: 
            MainPage.searchWatchesModal(watchInput)

        if importList: 
            MainPage.importList()

        MainPage.listRepeater()

    # Currency converter page static method
    @staticmethod
    def currencyConv() -> None: 

        # Page definitions
        st.set_page_config(layout = 'wide')

        # UI elements
        st.title('Currency Converter')
        
    # Margin calculator page static method
    @staticmethod
    def marginCalc() -> None: 

        # Page definitions
        st.set_page_config(layout = 'wide')

        # UI elements
        st.title('Margin Calculator')
        
        # Inputs
        price = st.number_input('Price', min_value = 0.0, step = 0.01)
        desired_margin = st.number_input('Desired Profit Margin (%)', min_value = 0.0, step = 0.1)

        # Button calculation
        if st.button('Calculate'): 
            st.write(f'Revenue: ${MarginCalc.profitMargin(price, desired_margin)}')
            st.write(f'Profit: ${MarginCalc.profitMargin(price, desired_margin) - price}')

        # Return button
        if st.button('Back'): 
            st.session_state.page = 'MainPage'
            st.rerun()
