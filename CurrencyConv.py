# Import statements
import requests

# Static class to represent the currency conversion page
class CurrencyConv: 

    # Static method to convert an amount of a certain currency from one to another
    @staticmethod
    def convert(amount, start, end) -> float: 

        # Exception handling
        try: 

            # Querying ECB for euro-based exchange rates
            url = 'https://api.exchangerate.host/latest'
            response = requests.get(url).json()
            rates = response['rates']

            # If converting from euro to the target or vice versa
            if start == 'EUR': 
                return amount * rates[end]
            if end == 'EUR': 
                return amount / rates[start]

            # Otherwise convert to euro before converting to the target currency
            euroAmount = amount / rates[start]
            return euroAmount * rates[end]

        except: 

            # Returning no price if conversion failed
            print('Currency conversion failed.')
            return 0.0