import yfinance as yf
import numpy as np
from scipy.stats import norm
from datetime import datetime
from scipy.optimize import brentq

# Retrieve real-time stock data (for example, Apple)
stock_ticker = 'AAPL'
stock_data = yf.Ticker(stock_ticker)
stock_prices = stock_data.history(period="1y")['Close']
current_stock_price = stock_prices.iloc[-1]  # Access the most recent closing price using iloc

# Retrieve the option data (for example, for a 150 strike price)
option_data = stock_data.option_chain('2025-05-02')  # Use a valid expiration date
call_option_price = option_data.calls[option_data.calls['strike'] == 150]['lastPrice'].iloc[0]  # Price of the call option at 150 strike

# Retrieve risk-free rate (e.g., 13-week U.S. Treasury Bill rate)
rf_data = yf.Ticker("^IRX")  # 13-week U.S. Treasury Bill
risk_free_rate = rf_data.history(period="1d")['Close'].iloc[0] / 100  # Convert to decimal

# Calculate the time to expiry (T)
expiry_date = datetime(2025, 5, 2)  # Expiration date of the option (updated)
current_date = datetime.today()
time_to_expiry = (expiry_date - current_date).days / 365  # Time to expiry in years


print(f"Current Stock Price: {current_stock_price}")
print(f"Strike Price: 150")
print(f"Risk-Free Rate: {risk_free_rate * 100}%")
print(f"Time to Expiry: {time_to_expiry:.2f} years")

