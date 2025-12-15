import random
import datetime

class MarketSim:
    def __init__(self):
        self.headlines = [
            ("FED Hikes Interest Rates by 50bps", "Bearish"),
            ("Apple Reports Record Q3 Earnings", "Bullish"),
            ("Oil Prices Surge Amid Supply Chain Crisis", "Bearish"),
            ("Tech Sector Rallies on AI Breakthrough", "Bullish"),
            ("Bitcoin Breaks $100k Resistance Level", "Bullish"),
            ("Global Manufacturing Output Slows Down", "Bearish"),
            ("Tesla Announces New Gigafactory in Europe", "Bullish")
        ]

    def get_live_feed(self, count=3):
        """Returns random headlines for stress testing."""
        return random.sample(self.headlines, count)

    def execute_trade(self, portfolio, action, price, amount=1):
        """
        portfolio: dict {'balance': float, 'shares': int}
        action: 'buy' or 'sell'
        """
        if action == 'buy':
            cost = price * amount
            if portfolio['balance'] >= cost:
                portfolio['balance'] -= cost
                portfolio['shares'] += amount
                return True, "ORDER FILLED"
            else:
                return False, "INSUFFICIENT FUNDS"
        
        elif action == 'sell':
            if portfolio['shares'] >= amount:
                gain = price * amount
                portfolio['balance'] += gain
                portfolio['shares'] -= amount
                return True, "ORDER FILLED"
            else:
                return False, "INSUFFICIENT ASSETS"
