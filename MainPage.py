# Import statements
import streamlit as st
import PIL

# Static class to represent the homepage
class MainPage: 

    # Variable definitions
    mainLabel = 'PriceWatch: A Price Comparison Tool for Fair Resale Valuation of Luxury Watches'
    logo = PIL.Image.open()
    addWatch = 'Add Watch'
    enterWatch = 'Enter Watch Below'
    watchTextInput = st.sidebar.text_input('Enter watch here')