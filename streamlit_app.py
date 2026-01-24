# I'll fix this later
import streamlit as st
import PIL
import clipboard_component
import requests
import io
import pyperclip
import base64
from Watch import Watch
from Watch import SearchedWatch

# Static method to search for watches and create a modal based on the given search terms, data is also cached if ever rereloaded
@staticmethod
@st.dialog(title = 'Results for Your Search', width = 'large', dismissible = True)
def searchWatchesModal(term): 

    # Variable initialization
    resultList = []
    query = []

    # Exception handling
    try: 

        # Parameters and headers for eBay
        client_id = st.secrets['CLIENT_ID']
        client_secret = st.secrets['CLIENT_SECRET']
        auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'client_credentials', 'scope': 'https://api.ebay.com/oauth/api_scope'}
        token = requests.post('https://api.ebay.com/identity/v1/oauth2/token', headers = headers, data = data).json()['access_token']

        # Querying for watches
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        query = requests.get('https://api.ebay.com/buy/browse/v1/item_summary/search', headers = headers, params = {'q': term, 'limit': 20}).json().get('itemSummaries', [])

    except: 

        # Exception handling
        print('Request unsuccessful. Try again later.')

    # Exception handling
    try: 
    
        # Iterating through list
        for i in query:  

            # Obtaining an image from a public URL
            try: 
                response = requests.get(i['image']['imageUrl']).content
            except: 
                print('Image access failed.')

            # Initiating a watch object based on info returned
            resultList.append(SearchedWatch(PIL.Image.open('watch_not_found.png'), i['title'], float(i['price']['value']), i['price']['currency']))

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

if st.button('testing'): 
    searchWatchesModal('rolex daytona')