# Import statements
import streamlit as st
import chrono24
import PIL


# Dynamic class for creation of a SearchedWatch class
class SearchedWatch: 

    # Init function with default none values
    def __init__(self, icon = None, name = None, price = None): 
        
        # Initiates variables with default values
        self.__icon = icon
        self.__name = name or 'Name not found'
        self.__price = price if price is not None else 0.0
    
    # Getter methods
    def getIcon(self): 
        return self.__icon
    
    def getName(self): 
        return self.__name
    
    def getPrice(self): 
        return self.__price

    # Setter methods
    def setIcon(self, icon): 
        self.__icon = icon
    
    def setName(self, name): 
        self.__name = name

    def setPrice(self, price): 
        self.__price = price

# Extends from SearchedWatch
class Watch(SearchedWatch): 

    # Init function with default None values
    def __init__(self, priceRange = None, priceGraph = None, reliability = None, sentiment = None, finalRating = None): 
        
        # Parent class initiation
        super.__init__()

        # Initiates variables with default values
        self.__priceRange = priceRange or []
        self.__priceGraph = priceGraph or []
        self.__reliability = reliability if reliability is not None else 0.0
        self.__sentiment = sentiment if sentiment is not None else 0.0
        self.__finalRating = finalRating if finalRating is not None else 0.0
    
    # Getter methods
    def getPriceRange(self): 
        return self.__priceRange
    
    def getPriceGraph(self): 
        return self.__priceGraph

    def getReliability(self): 
        return self.__reliability
    
    def getSentiment(self): 
        return self.__sentiment
    
    def getFinalRating(self): 
        return self.__finalRating
    
    # Setter methods
    def setPriceRange(self, priceRange): 
        self.__priceRange = priceRange
    
    def setPriceGraph(self, priceGraph): 
        self.__priceGraph = priceGraph

    def setReliability(self, reliability): 
        self.__reliability = reliability
    
    def setSentiment(self, sentiment): 
        self.__sentiment = sentiment
    
    def setFinalRating(self, finalRating): 
        self.__finalRating = finalRating