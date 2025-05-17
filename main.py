import pandas as pd
import requests
from fredapi import Fred
import statsmodels.api as sm
import os
import myplots as mp


# === USER INPUTS ===
FRED_API_KEY = ""
POLYGON_API_KEY = ""
stock_symbol = "DUK"  # Duke Energy
start_date = "2021-05-01"
end_date = "2025-05-01"

# === Step 1: Get macroeconomic data from FRED ===
fred = Fred(api_key=FRED_API_KEY)

# Load from file if exists
if os.path.exists("data/macro_data.csv"):
    macro_df = pd.read_csv("data/macro_data.csv", index_col=0, parse_dates=True)
    print("Loaded macro data from file.")
else:
    print("Fetching macro data from FRED...")
    # Fetch from FRED and save
    cpi = fred.get_series("CPIAUCSL", observation_start=start_date, observation_end=end_date)
    treasury = fred.get_series("DGS10", observation_start=start_date, observation_end=end_date)
    natgas = fred.get_series("DHHNGSP", observation_start=start_date, observation_end=end_date)

    macro_df = pd.concat([cpi, treasury, natgas], axis=1)
    macro_df.columns = ["cpi", "10yr_yield", "natgas"]
    macro_df = macro_df.resample("W").mean()
    macro_df['cpi'] = macro_df['cpi'].ffill().bfill()
    macro_df['10yr_yield'] = macro_df['10yr_yield'].ffill().bfill()
    macro_df['natgas'] = macro_df['natgas'].ffill().bfill()
    macro_df.to_csv("macro_data.csv")

# Repeat for stock prices
if os.path.exists("data/stock_returns.csv"):
    prices = pd.read_csv("data/stock_returns.csv", index_col=0, parse_dates=True)
    print("Loaded stock returns from file.")
else:
    # === Step 2: Get stock price data from Polygon.io ===
    print("Pulling stock data from Polygon.io...")
    polygon_url = f"https://api.polygon.io/v2/aggs/ticker/{stock_symbol}/range/1/day/{start_date}/{end_date}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": POLYGON_API_KEY
    }

    print("Fetching stock data from Polygon.io...")
    response = requests.get(polygon_url, params=params).json()
    prices = pd.DataFrame(response['results'])
    prices['t'] = pd.to_datetime(prices['t'], unit='ms')
    prices.set_index('t', inplace=True)
    prices = prices['c'].resample('W').last().pct_change().dropna()
    prices.name = "weekly_return"
    prices.to_csv("stock_returns.csv")

# === Step 3: Merge datasets ===
full_df = pd.concat([prices, macro_df], axis=1).dropna()
full_df['delta_yield'] = full_df['10yr_yield'].diff()
full_df = full_df.dropna()
# Check for remaining gaps for cpi, 10yr_yield, or natgas
print(macro_df.isna().sum())
# if under 100 observations, might need more data
print("Final sample size:", len(full_df))


# === Step 4: Regression Analysis ===
X = full_df[['delta_yield', 'cpi', 'natgas']]
X = sm.add_constant(X)
y = full_df['weekly_return']

model = sm.OLS(y, X).fit()
print(model.summary())

# Call the function
mp.plot_macro_indicators(full_df)
# correlation overlay is interesting but not a great visual.
# mp.plot_correlation_overlay(full_df)
mp.plot_regression_scatter(full_df, ['delta_yield', 'cpi', 'natgas'])
