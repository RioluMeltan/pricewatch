# Import statements
import streamlit as st
from PIL import Image

# Static class to access pages
class Navigation: 

    # Main page
    def mainPage(): 

        # Page definitions
        st.set_page_config(layout = 'wide')

        # Initializing persistent storage
        if 'watches' not in st.session_state: 
            st.session_state.watches = []

        # UI elements
        st.title('PriceWatch: A Price Comparison Tool for Fair Resale Valuation of Luxury Watches')
        st.sidebar.image(Image.open())
        st.sidebar.text('Add Watch')
        st.sidebar.text('Enter Watch Below')
        st.sidebar.text_input('Enter watch here')
        st.sidebar.button('Search for Watch')
        st.sidebar.button('Import List from Clipboard')

        # Column formatting for buttons
        col_1, col_2, col_3 = st.columns([1, 1, 1])
        with col_1: 
            currencyConvButton = st.button('Currency Converter')

        with col_2: 
            marginCalcButton = st.button('Margin Calculator')

        with col_3: 
            exportListButton = st.button('Export Watchlist')