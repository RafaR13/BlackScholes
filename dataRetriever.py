import yfinance as yf
import numpy as np
from datetime import datetime

class DataRetriever:
    def __init__(self, stock_name_or_ticker, strike_price, expiry_str):
        self.stock_name_or_ticker = stock_name_or_ticker
        self.strike_price = strike_price
        self.expiry_str = expiry_str  # Format: 'YYYY-MM-DD'
        
        self.stock = yf.Ticker(self.stock_name_or_ticker)
        self.current_price = None
        self.call_option_price = None
        self.risk_free_rate = None
        self.time_to_expiry = None

    def fetch_data(self):
        # Get current stock price
        stock_prices = self.stock.history(period="1y")['Close']
        self.current_price = stock_prices.iloc[-1]

        # Get option chain
        option_chain = self.stock.option_chain(self.expiry_str)
        call_options = option_chain.calls
        strike_match = call_options[call_options['strike'] == self.strike_price]
        
        if strike_match.empty:
            raise ValueError(f"No call option found at strike {self.strike_price}")

        self.call_option_price = strike_match['lastPrice'].iloc[0]

        # Risk-free rate (from 13-week treasury bill "^IRX")
        rf_data = yf.Ticker("^IRX")
        self.risk_free_rate = rf_data.history(period="1d")['Close'].iloc[0] / 100  # Convert to decimal

        # Time to expiry
        expiry_date = datetime.strptime(self.expiry_str, "%Y-%m-%d")
        current_date = datetime.today()
        self.time_to_expiry = (expiry_date - current_date).days / 365
        
        if self.time_to_expiry <= 0:
            raise ValueError("The option has already expired!")

    def get_data(self):
        return self.current_price, self.call_option_price, self.risk_free_rate, self.time_to_expiry
