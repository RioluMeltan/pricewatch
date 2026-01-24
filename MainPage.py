# Import statements
import streamlit as st
import PIL
import clipboard_component
import requests
import io
import pyperclip
import GoogleNews
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from Watch import Watch
from Watch import SearchedWatch

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
    st.session_state.watches = [] # Goes to session_state for persistent storage (MAYBE change? Not sure if this'll work.)

    # Column formatting for buttons
    col_1, col_2, col_3 = st.columns([1, 1, 1])
    with col_1: 
        currencyConvButton = st.button('Currency Converter')

    with col_2: 
        marginCalcButton = st.button('Margin Calculator')

    with col_3: 
        exportListButton = st.button('Export Watchlist')

    # Static method to find minimum in a list
    @staticmethod
    def findMin(toFind): 
        smallest = toFind[0]
        for i in toFind[1:]: 
            if i < smallest:
                smallest = i
        return smallest

    # Static method to find maximum in a list
    @staticmethod
    def findMax(toFind): 
        largest = toFind[0]
        for i in toFind[1:]: 
            if i > largest:
                largest = i
        return largest

    # Static method to find the sum of a list
    @staticmethod
    def findSum(toFind):
        total = 0
        for i in toFind:
            total += i
        return total

    # Static bubble sort method for lists
    @staticmethod
    def bubbleSort(toSort): 

        # Bubble sort
        for i in range(len(toSort)):
            for j in range(0, len(toSort) - i - 1):

                # Compare elements that are next to each other
                if toSort[j] > toSort[j + 1]:
                    toSort[j], toSort[j + 1] = toSort[j + 1], toSort[j]

        return toSort

    # Static method to calculate a reliability score for a watch query
    @staticmethod
    def reliabilityCalc(term): 

         # Querying the API for watches
        try: 

            # Parameters for eBay
            params = {'OPERATION-NAME': 'findItemsByKeywords', 'SERVICE-VERSION': '1.0.0', 'SECURITY-APPNAME': st.secrets['APP_ID'], 'RESPONSE-DATA-FORMAT': 'JSON', 'REST-PAYLOAD': '', 'keywords': term, 'paginationInput.entriesPerPage': '20'}

            # Performing the query
            query = requests.get('https://svcs.ebay.com/services/search/FindingService/v1', params = params).json()

        except: 

            # Exception handling
            print('Request unsuccessful. Try again later.')
    
        # Variable initation
        scores = []
        prices = []
        finalScore = 0

        # Iterating through results
        for index, i in enumerate(query): 

            # Image status check (weighted 0.15)
            if 'galleryURL' in i and i['galleryURL'][0].startswith('http'): 
                scores.append(0.15)
            else: 
                scores.append(0.0)

            # Reputation check (weighted 0.35)
            try: 
                scores[index] += float(i['sellerInfo'][0]['positiveFeedbackPercent'][0]) * 0.35
            except: 
                print('Seller info could not be found.')

            # Listing type check (weighted 0.2)
            try: 
                if i['listingInfo'][0]['listingType'][0] == 'FixedPrice': 
                    scores[index] += 0.2
                elif i['listingInfo'][0]['listingType'][0] == 'Auction': 
                    scores[index] += 0.1
            except:
                print('Pricing info could not be found.')
            
            # Append price to prices
            try: 
                prices += float(i['sellingStatus'][0]['currentPrice'][0]['__value__'])
            except: 
                print('Price could not be found.')

        # Final averaging
        for i in scores: 
            finalScore += i
            finalScore /= len(scores)

        # Price checking (weighted 0.3)
        if (MainPage.findMax(prices) - MainPage.findMin(prices)) / (MainPage.findSum(prices) / len(prices)) <= 1: 
            finalScore += (MainPage.findMax(prices) - MainPage.findMin(prices)) / (MainPage.findSum(prices) / len(prices)) * 0.3
        elif (MainPage.findMax(prices) - MainPage.findMin(prices)) / (MainPage.findSum(prices) / len(prices)) > 1: 
            finalScore += 0.3

        return int(finalScore * 100)

    # Static method to calculate the sentiment for a watch query using GoogleNews
    @staticmethod
    def sentimentCalc(term): 

        # Exception handling
        try: 
        
            # Accessing and searching the past week of GoogleNews for a watch
            news = GoogleNews.GoogleNews(lang = 'en', period = '7d')
            news.search(term)

            # Separating headlines and paragraphs into lists
            headlines = [item['title'] for item in news.result() if item.get('title')]
            paragraphs = [body['desc'] for body in news.result() if body.get('title')]

            # Accessing a pre-existing lexicon for sentiment analysis
            sia = SentimentIntensityAnalyzer(lexicon_file = 'sentiment/vader_lexicon/vader_lexicon.txt')

            # Setting original sentiment score as headline sentiment score before adding the sentiment scores of the paragraphs
            sentiment_scores = [sia.polarity_scores(headline)['compound'] for headline in headlines]
            sentiment_scores += [sia.polarity_scores(paragraph)['compound'] for paragraph in paragraphs]

            # Calculating an average sentiment for all results
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

        except: 

            # Default sentiment if something fails
            avg_sentiment = 0.0

        return avg_sentiment

    # Static method to search for watches and create a modal based on the given search terms, data is also cached if ever rereloaded
    @staticmethod
    @st.cache_data
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

    # Static method to import a list from clipboard
    @staticmethod
    def importList(): 

        # Import from clipboard
        imported_content = clipboard_component.paste_component('Read Clipboard')

        # Iterate through formatted content
        for i in imported_content.split(','): 

            # Append to list
            try: 
                st.session_state.watches.append(Watch(i.split(' ')[0], i.split(' ')[1], i.split(' ')[2], i.split(' ')[3], i.split(' ')[4], i.split(' ')[5], i.split(' ')[6]))
            except: 
                st.toast('An error occurred. Ensure that your pasted list is formatted correctly.')

    # Static method to copy the resale price to the clipboard
    @staticmethod
    def priceToClipboard(price, currency): 
        
        # Pyperclip copy
        pyperclip.copy(f'$ {price} {currency}')