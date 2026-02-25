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

            # Querying for exchange rates
            response = requests.get(f'https://hexarate.paikama.co/api/rates/{start}/{end}/latest').json()
            rate = response['data']['mid']

            # Return amount times rate
            return amount * rate

        except Exception as ex: 

            # Returning no price if conversion failed
            st.error('Currency conversion failed.')
            return 0.0
