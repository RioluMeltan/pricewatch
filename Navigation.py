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
    def mainPage(): 

        # Page definitions
        st.set_page_config(layout = 'wide')

        # Initializing persistent storage for watches
        if 'watches' not in st.session_state: 
            st.session_state.watches = []

        # UI elements
        st.title('PriceWatch: A Price Comparison Tool for Fair Resale Valuation of Luxury Watches')
        # st.sidebar.image(Image.open('')) REMEMBER TO ADD A LOGO LATER
        st.sidebar.text('Add Watch')
        st.sidebar.text('Enter Watch Below')
        watchInput = st.sidebar.text_input('Enter watch here')
        searchWatches = st.sidebar.button('Search for Watch')
        importList = st.sidebar.button('Import List from Clipboard')

        # Column formatting for buttons
        col_1, col_2, col_3 = st.columns([1, 1, 1])
        with col_1: 
            if st.button('Currency Converter'): 
                st.session_state.page = 'CurrencyConv'

        with col_2: 
            if st.button('Margin Calculator'): 
                st.session_state.page = 'MarginCalc'

        with col_3: 
            if st.button('Export Watchlist'): 
                MainPage.exportList()

        if searchWatches and watchInput.value: 
            MainPage.searchWatchesModal(watchInput.value)

        if importList: 
            MainPage.importList()

        MainPage.listRepeater()