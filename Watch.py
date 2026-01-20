# Import statements
import streamlit as st
import chrono24
import PIL

# Dynamic class for creation of a Watch class
class Watch: 

    # Init function with default None values
    def __init__(self, icon = None, name = None, priceRange = None, priceGraph = None, reliability = None, sentiment = None, finalRating = None): 
        
        # Initiates variables with default values
        self.icon = icon
        self.name = name or 'Name not found'
        self.priceRange = priceRange or []
        self.priceGraph = priceGraph or []
        self.reliability = reliability if reliability is not None else 0.0
        self.sentiment = sentiment if sentiment is not None else 0.0
        self.finalRating = finalRating if finalRating is not None else 0.0