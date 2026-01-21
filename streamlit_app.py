# Use this to test formatting before final app
# Import statements
import streamlit as st
import PIL
import chrono24
import clipboard_component
import requests
import io
from Watch import Watch
from Watch import SearchedWatch
# Method to search for watches and create a modal based on the given search terms, data is also cached if ever rereloaded
@st.cache_data
@st.dialog(title = 'Results for Your Search', width = 'large', dismissible = True)
def searchWatchesModal(term): 
    
    # Variable initialization
    resultList = []
    price = 0.0
    try: 
        query = chrono24.query(term).search()
    except: 
        print('Chrono24 request blocked; try again later.')

    # Iterating through list
    for i in query: 

        # Obtaining an image from a public URL
        try: 
            response = requests.get(i['image_urls'][0]).content
        except: 
            print('Image access failure')

        # Obtaining a price range
        price = float(i['price'].replace('$', '').replace(',', '').strip())

        # Initiating a watch object based on info returned from Chrono24
        resultList.append(SearchedWatch(PIL.Image.open(io.BytesIO(response)), i['title'], price))

    # Displaying results using columns and enumerated list to cycle
    cols = st.columns(3)
    for index, watch in enumerate(resultList): 
        col = cols[index % 3]
        with col:
            st.image(watch.icon, use_column_width = True)
            st.markdown(watch.name)
            st.markdown(f'${watch.price}')

searchWatchesModal('rolex daytona')