# Static class for calculating the profit margin
class MarginCalc: 

    # Static method to calculate a profit margin based on cost and sell price
    @staticmethod
    def profitMargin(cost: float, sell: float) -> float: 
        
        # Negative value handling
        if sell <= 0: 
            return 0.0

        # Calculating profit margin
        margin = ((sell - cost) / sell) * 100
        return round(margin, 2)