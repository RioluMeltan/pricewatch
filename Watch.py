# Import statements
import pandas
from PIL import Image

# Dynamic class for creation of a SearchedWatch class
class SearchedWatch: 

    # Init function with default none values
    def __init__(self, icon: Image.Image | None = None, name: str | None = None, currency: str | None = None, price: float | None = None, date: str | None = None) -> None: 

        # Initiates variables with default values
        self.__icon = icon
        self.__name = name or 'Name not found'
        self.__price = price if price is not None else 0.0
        self.__currency = currency or 'USD'
        self.__date = date or 'Date not found'
    
    # Getter methods
    def getIcon(self): 
        return self.__icon
    
    def getName(self): 
        return self.__name

    def getCurrency(self): 
        return self.__currency
    
    def getPrice(self): 
        return self.__price

    def getDate(self): 
        return self.__date

    # Setter methods
    def setIcon(self, icon): 
        self.__icon = icon
    
    def setName(self, name): 
        self.__name = name

    def setCurrency(self, currency): 
        self.__currency = currency

    def setPrice(self, price): 
        self.__price = price

    def setDate(self, date): 
        self.__date = date

# Extends from SearchedWatch
class Watch(SearchedWatch): 

    # Init function with default None values
    def __init__(self, dateList: list[str] | None = None, priceList: list[float] | None = None, priceRange: tuple[float, float] | None = None, reliability: int | None = None, sentiment: float | None = None, finalRating: int | None = None, resalePrice: float | None = None) -> None: 
        
        # Parent class initiation
        super().__init__()

        # Initiates variables with default values
        self.__dateList = dateList or []
        self.__priceList = priceList or []
        self.__priceRange = priceRange or ()
        self.__reliability = reliability if reliability is not None else 0.0
        self.__sentiment = sentiment if sentiment is not None else 0.0
        self.__finalRating = finalRating if finalRating is not None else 0.0
        self.__resalePrice = resalePrice if resalePrice is not None else 0.0
    
    # Getter methods
    def getDateList(self): 
        return self.__dateList
    
    def getPriceList(self): 
        return self.__priceList
    
    def getPriceRange(self): 
        return self.__priceRange

    def getReliability(self): 
        return self.__reliability
    
    def getSentiment(self): 
        return self.__sentiment
    
    def getFinalRating(self): 
        return self.__finalRating

    def getResalePrice(self): 
        return self.__resalePrice
    
    # Setter methods
    def setDateList(self, dateList): 
        self.__dateList = dateList

    def setPriceList(self, priceList): 
        self.__priceList = priceList

    def setPriceRange(self, priceRange): 
        self.__priceRange = priceRange

    def setReliability(self, reliability): 
        self.__reliability = reliability
    
    def setSentiment(self, sentiment): 
        self.__sentiment = sentiment
    
    def setFinalRating(self, finalRating): 
        self.__finalRating = finalRating

    def setResalePrice(self, resalePrice): 
        self.__resalePrice = resalePrice

    # Return highest price
    def returnMaxPrice(self): 
        return self.__priceRange[1]

    # Return lowest price
    def returnMinPrice(self): 
        return self.__priceRange[0]
    
    # Return graphable dataframe for prices in conjunction to date
    def returnPriceDataframe(self): 

        # Iterate through price and date list
        data = []
        for index, i in enumerate(self.__priceList): 
            data.append({'date': self.__dateList[index], 'price': i})

            # Create dataframe using Pandas
            dataframe = pandas.DataFrame(data)
            dataframe['date'] = pandas.to_datetime(dataframe['date'])
            return dataframe