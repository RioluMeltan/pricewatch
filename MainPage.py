# Import statements
import streamlit as st
import clipboard_component
import requests
import io
import pyperclip
import GoogleNews
import base64
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from Watch import Watch
from Watch import SearchedWatch

# Static class to represent the homepage
class MainPage: 

    # Static method to find minimum in a list
    @staticmethod
    def findMin(toFind: list) -> float: 
        smallest = toFind[0]
        for i in toFind[1:]: 
            if i < smallest:
                smallest = i
        return smallest

    # Static method to find maximum in a list
    @staticmethod
    def findMax(toFind: list) -> float: 
        largest = toFind[0]
        for i in toFind[1:]: 
            if i > largest:
                largest = i
        return largest

    # Static method to find the sum of a list
    @staticmethod
    def findSum(toFind: list) -> float:
        total = 0
        for i in toFind:
            total += i
        return total

    # Static bubble sort method for lists
    @staticmethod
    def bubbleSort(toSort: list) -> list: 

        # Bubble sort
        for i in range(len(toSort)):
            for j in range(0, len(toSort) - i - 1):

                # Compare elements that are next to each other
                if toSort[j] > toSort[j + 1]:
                    toSort[j], toSort[j + 1] = toSort[j + 1], toSort[j]

        return toSort

    # Static method to calculate a reliability score for a watch query
    @staticmethod
    def reliabilityCalc(term: str) -> int: 

         # Querying the API for watches
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
            st.error('Request unsuccessful. Try again later.')
    
        # Variable initation
        scores = []
        prices = []
        finalScore = 0

        # Iterating through results
        for index, i in enumerate(query): 

            # Image status check (weighted 0.15)
            if 'image' in i and 'imageUrl' in i['image']: 
                scores.append(0.15)
            else: 
                scores.append(0.0)

            # Reputation check (weighted 0.35)
            try: 
                scores[index] += float(i['seller']['feedbackPercentage']) * 0.0035
            except: 
                st.error('Seller info could not be found.')

            # Listing type check (weighted 0.2)
            try: 
                if i['buyingOptions'][0] == 'FIXED_PRICE': 
                    scores[index] += 0.2
                elif i['buyingOptions'][0] == 'AUCTION': 
                    scores[index] += 0.1
            except:
                st.error('Pricing info could not be found.')
            
            # Append price to prices
            try: 
                prices.append(float(i['price']['value']))
            except: 
                st.error('Price could not be found.')

        # Final averaging
        finalScore += MainPage.findSum(scores) / len(scores)

        # Price checking (weighted 0.3)
        if (MainPage.findMax(prices) - MainPage.findMin(prices)) / (MainPage.findSum(prices) / len(prices)) <= 1: 
            finalScore += (MainPage.findMax(prices) - MainPage.findMin(prices)) / (MainPage.findSum(prices) / len(prices)) * 0.3
        elif (MainPage.findMax(prices) - MainPage.findMin(prices)) / (MainPage.findSum(prices) / len(prices)) > 1: 
            finalScore += 0.3

        return int(finalScore * 100)

    # Static method to calculate the sentiment for a watch query using GoogleNews
    @staticmethod
    def sentimentCalc(term: str) -> float: 

        # Exception handling
        try: 
        
            # Accessing and searching the past week of GoogleNews for a watch
            news = GoogleNews.GoogleNews(lang = 'en', period = '7d')
            news.search(term)

            # Separating headlines and paragraphs into lists
            headlines = [item['title'] for item in news.result() if item.get('title')]
            paragraphs = [body['desc'] for body in news.result() if body.get('title')]

            # Accessing a pre-existing lexicon for sentiment analysis
            sia = SentimentIntensityAnalyzer(lexicon_file = 'assets/vader_lexicon.txt')

            # Setting original sentiment score as headline sentiment score before adding the sentiment scores of the paragraphs
            sentimentScores = [sia.polarity_scores(headline)['compound'] for headline in headlines]
            sentimentScores += [sia.polarity_scores(paragraph)['compound'] for paragraph in paragraphs]

            # Calculating an average sentiment for all results
            avgSentiment = MainPage.findSum(sentimentScores) / len(sentimentScores) if sentimentScores else 0.0

        except: 

            # Default sentiment if something fails
            avgSentiment = 0.0

        return avgSentiment

    # Static method to search for watches and create a modal based on the given search terms
    @staticmethod
    @st.dialog(title = 'Results for Your Search', width = 'large', dismissible = True, on_dismiss = 'rerun')
    def searchWatchesModal(term: str) -> None: 

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
            st.error('Request unsuccessful. Try again later.')

        # Exception handling
        try: 
        
            # Iterating through list
            for i in query:  

                # Obtaining an image from a public URL
                try: 
                    response = io.BytesIO(requests.get(i['image']['imageUrl']).content)
                except: 
                    response = 'assets/watch_not_found.png'
                    st.error('Image access failed.')

                # Initiating a watch object based on info returned
                resultList.append(SearchedWatch(response, i['title'], i['price']['currency'], float(i['price']['value']), i['itemCreationDate']))

        except: 

            # Exception handling
            st.error('Iteration failed.')

        # Add to watchlist button
        if st.button('Add to Watchlist'): 

            # Variable definition
            toAdd = Watch()
            sumPrices = 0.0
            dateList = []
            priceList = []

            # Basic setters
            toAdd.setIcon(resultList[0].getIcon())
            toAdd.setName(resultList[0].getName())
            toAdd.setCurrency(resultList[0].getCurrency())
            
            # Iterate through and calculate each value
            for watch in resultList: 
                sumPrices += watch.getPrice()
                toAdd.setPrice(sumPrices / len(resultList))
                dateList.append(watch.getDate())
                priceList.append(watch.getPrice())

            # Final setters
            toAdd.setDateList(dateList)
            toAdd.setPriceList(priceList)
            toAdd.setPriceRange((MainPage.findMin(priceList), MainPage.findMax(priceList)))
            toAdd.setReliability(MainPage.reliabilityCalc(term))
            toAdd.setSentiment(MainPage.sentimentCalc(term))

            # Final resell rating and price calculation
            if (toAdd.getPriceRange()[1] - toAdd.getPriceRange()[0]) / toAdd.getPrice() <= 1: 
                toAdd.setFinalRating(0.5 * toAdd.getReliability() + 30 * toAdd.getSentiment() + 20 * (1 - ((toAdd.getPriceRange()[1] - toAdd.getPriceRange()[0]) / toAdd.getPrice())))
            else: 
                toAdd.setFinalRating(0.5 * toAdd.getReliability() + 30 * toAdd.getSentiment())
            toAdd.setResalePrice((toAdd.getPriceRange()[0] + toAdd.getPriceRange()[1]) / 2)

            # Appending to global variable
            st.session_state.watches.append(toAdd)

        # Displaying results using columns and enumerated list to cycle
        cols = st.columns(3)
        for index, watch in enumerate(resultList): 
            col = cols[index % 3]
            with col:
                st.image(Image.open(watch.getIcon()), use_column_width = True)
                st.markdown(watch.getName())
                st.markdown(f'${watch.getPrice()} {watch.getCurrency()}')

    # Static method to import a list from clipboard
    @staticmethod
    def importList() -> None: 

        # Import from clipboard
        imported_content = clipboard_component.paste_component('Read Clipboard')

        # Iterate through formatted content
        for i in imported_content.splitlines(): 

            # Append to list
            try: 
                st.session_state.watches.append(Watch(i.split(', ')[0], i.split(', ')[1], i.split(', ')[2], i.split(', ')[3], i.split(', ')[4], i.split(', ')[5], i.split(', ')[6], i.split(', ')[7], i.split(', ')[8], i.split(', ')[9], i.split(', ')[10], i.split(', ')[11], i.split(', ')[12], i.split(', ')[13]))
            except: 
                st.toast('An error occurred. Ensure that your pasted list is formatted correctly.')

    @staticmethod
    def exportList() -> None: 

        # String to export
        toEx = ''

        # Convert to export format
        for i in st.session_state.watches: 
            toEx += str(i.getIcon()) + ', ' + str(i.getName()) + ', ' + str(i.getPrice()) + ', ' + str(i.getCurrency()) + ', ' + str(i.getDate()) + ', ' + str(i.getDateList()) + ', ' + str(i.getPriceList()) + ', ' + str(i.getPriceRange()) + ', ' + str(i.getReliability()) + ', ' + str(i.getSentiment()) + ', ' + str(i.getFinalRating()) + ', ' + str(i.getResalePrice())

        # Exporting to clipboard
        pyperclip.copy(toEx)

    # Static method to fully display the watchlist
    @staticmethod
    def listRepeater() -> None: 

        # Iterate through watches
        for watch in st.session_state.watches: 

            # Columned container for consistent box sizes
            with st.container(height = 300): 
                col_1, col_2, col_3, col_4 = st.columns([3, 5, 3, 1])

                # Icon displaying
                with col_1: 
                    st.image(Image.open(watch.getIcon()))

                # Text-based info
                with col_2: 
                    st.markdown(f'**"{watch.getName()}"**')
                    st.markdown(f'**Market Price Range:** \\${watch.getPriceRange()[0]} {watch.getCurrency()} - \\${watch.getPriceRange()[1]} {watch.getCurrency()}')
                    st.markdown(f'**Reliability Score:** {watch.getReliability()}/100')
                    st.markdown(f'**Watch Sentiment:** {watch.getSentiment()}')
                    st.markdown(f'**Final Resale Rating:** {watch.getFinalRating()}/100')
                    
                    # Price graph modal
                    with st.popover(f'Display Price Graph'): 
                        st.line_chart(watch.returnPriceDataframe()['price'])

                # Resale price and copy to clipboard
                with col_3: 
                    st.write('DO NOT FORGET TO DO THIS')

                # Close button
                with col_4: 
                    st.write('AND THIS')

    # Static method to copy the resale price to the clipboard
    @staticmethod
    def priceToClipboard(price: float, currency: str) -> None: 
        
        # Pyperclip copy
        pyperclip.copy(f'$ {price} {currency}')