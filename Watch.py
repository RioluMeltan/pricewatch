# Import statements
import streamlit as st
import chrono24
import PIL

# Dynamic class for creation of a Watch class
class Watch: 

    # Init function with default None values
    def __init__(self, icon = None, name = None, priceRange = None, priceGraph = None, reliability = None, sentiment = None, finalRating = None): 
        
        # Initiates variables with default values
        self.__icon = icon
        self.__name = name or 'Name not found'
        self.__priceRange = priceRange or []
        self.__priceGraph = priceGraph or []
        self.__reliability = reliability if reliability is not None else 0.0
        self.__sentiment = sentiment if sentiment is not None else 0.0
        self.__finalRating = finalRating if finalRating is not None else 0.0
    
    # Getter methods
    def getIcon(self): 
        return self.__icon
    
    def getName(self): 
        return self.__name
    
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
    def setIcon(self, icon): 
        self.__icon = icon
    
    def setName(self, name): 
        self.__name = name

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