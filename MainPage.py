# Import statements
import streamlit as st
import PIL
import chrono24
import clipboard_component
import requests
import io
from Watch import Watch

# Static class to represent the homepage
class MainPage: 

    # Page definitions
    st.set_page_config(layout = 'wide')

    # Variable definitions
    mainLabel = st.title('PriceWatch: A Price Comparison Tool for Fair Resale Valuation of Luxury Watches')
    logo = st.sidebar.image(PIL.Image.open())
    addWatch = st.sidebar.text('Add Watch')
    enterWatch = st.sidebar.text('Enter Watch Below')
    watchTextBox = st.sidebar.text_input('Enter watch here')
    searchWatchButton = st.sidebar.button('Search for Watch')
    importListButton = st.sidebar.button('Import List from Clipboard')
    watches = [] # Goes to session_state

    # Column formatting for buttons
    col_1, col_2, col_3 = st.columns([1, 1, 1])
    with col_1: 
        currencyConvButton = st.button('Currency Converter')

    with col_2: 
        marginCalcButton = st.button('Margin Calculator')

    with col_3: 
        exportListButton = st.button('Export Watchlist')

    # Method to search for watches and create a modal based on the given search terms
    @st.dialog(title = 'Watch Search Results', width = 'large', dismissible = True)
    def searchWatchesModal(term): 
        
        # List of results
        resultList = []

        # Iterating through list
        for i in chrono24.query(term).search(): 

            # Obtaining image from public URL
            response = requests.get(i['image_urls'][0]).content
            response.raise_for_status()

            # Obtaining 

            # Initiating a watch object based on info returned from Chrono24
            resultList.append(Watch(PIL.Image.open(io.BytesIO(response)), i['title'], ))

    # Method to import a list from clipboard
    def importList(): 

        # Import from clipboard
        imported_content = clipboard_component.paste_component('Read Clipboard')

        # Iterate through formatted content
        for i in imported_content.split(','): 

            # Exception handling
            try: 

                # Append to list
                st.session_state.watches.append(Watch(i.split(' ')[0], i.split(' ')[1], i.split(' ')[2], i.split(' ')[3], i.split(' ')[4], i.split(' ')[5], i.split(' ')[6]))

            except: 

                # Exception message
                st.toast('An error occurred. Ensure that your pasted list is formatted correctly.')