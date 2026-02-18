# Import statements
import streamlit as st
import requests

# Static class to represent the currency conversion page
class CurrencyConv: 

    # Static method to convert an amount of a certain currency from one to another
    @staticmethod
    def convert(amount: float, start: str, end: str) -> float: 

        # Exception handling
        try: 

            # Querying ECB for euro-based exchange rates
            response = requests.get('https://api.exchangerate.host/latest').json()
            rates = response['rates']

            # If converting from euro to the target or vice versa
            if start == 'EUR': 
                return amount * rates[end]
            if end == 'EUR': 
                return amount / rates[start]

            # Otherwise convert to euro before converting to the target currency
            return (amount / rates[start]) * rates[end]

        except: 

            # Returning no price if conversion failed
            st.error('Currency conversion failed.')
            return 0.0