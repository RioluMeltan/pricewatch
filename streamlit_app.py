# I'll fix this later
import streamlit as st
import PIL
import clipboard_component
import requests
import io
import pyperclip
from Watch import Watch
from Watch import SearchedWatch

@st.dialog(title = 'Results for Your Search', width = 'large', dismissible = True)
def searchWatchesModal(term): 

    # Variable initialization
    resultList = []
    query = []

    # Querying the API for watches
    try: 

        # Parameters for eBay
        params = {'OPERATION-NAME': 'findItemsByKeywords', 'SERVICE-VERSION': '1.0.0', 'SECURITY-APPNAME': st.secrets['APP_ID'], 'RESPONSE-DATA-FORMAT': 'JSON', 'REST-PAYLOAD': '', 'keywords': term, 'paginationInput.entriesPerPage': '20'}

        # Performing the query
        query = requests.get('https://svcs.ebay.com/services/search/FindingService/v1', params = params).json()

    except: 

        # Exception handling
        print('Request unsuccessful. Try again later.')

    try: 
    
        # Iterating through list
        for i in query['findItemsByKeywordsResponse'][0]['searchResult'][0]['item']:  

            # Obtaining an image from a public URL
            try: 
                response = requests.get(i['galleryURL'][0]).content
            except: 
                print('Image access failed.')

            # Initiating a watch object based on info returned
            resultList.append(SearchedWatch(PIL.Image.open(io.BytesIO(response)), i['title'][0], float(i['sellingStatus'][0]['currentPrice'][0]['__value__']), i['sellingStatus'][0]['currentPrice'][0]['@currencyId']))

    except: 

        # Exception handling
        print('Iteration failed.')

    # Displaying results using columns and enumerated list to cycle
    cols = st.columns(3)
    for index, watch in enumerate(resultList): 
        col = cols[index % 3]
        with col:
            st.image(watch.getIcon(), use_column_width = True)
            st.markdown(watch.getName())
            st.markdown(f'${watch.getPrice()} {watch.getCurrency()}')

searchWatchesModal('rolex daytona')