# Static class for calculating the profit margin
class MarginCalc: 

    # Static method to calculate a profit margin based on price and desired margin
    @staticmethod
    def profitMargin(cost: float, margin: float) -> float: 
        
        # Negative value handling
        if margin <= 0: 
            return 0.0

        # Calculating profit margin
        price = cost * (1 + margin / 100)
        return round(price, 2)
