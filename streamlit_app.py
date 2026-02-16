# Import statements
import streamlit as st
from Navigation import Navigation

# Initializing page navigation
if 'page' not in st.session_state: 
    st.session_state.page = 'MainPage'

# Navigating through the pages
if st.session_state.page == 'MainPage': 
    Navigation.mainPage()
elif st.session_state.page == 'CurrencyConv': 
    Navigation.currencyConv()
elif st.session_state.page == 'MarginCalc': 
    Navigation.marginCalc()