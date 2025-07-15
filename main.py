import os
import pandas as pd
from myplots import plot_adj_r2_by_lag
import yfinance as yf
from fredapi import Fred
import statsmodels.api as sm
from lag_sweep_utils import find_best_lag
import myplots as mp


# === USER INPUTS ===
FRED_API_KEY = ""
start_date = "2005-01-01"
end_date = "2025-05-01"
stock_symbols = ["DUK", "SO", "NEE"]

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# === Step 1: Fetch macroeconomic data ===
macro_path = "data/macro_data.csv"
fred = Fred(api_key=FRED_API_KEY)

if os.path.exists(macro_path):
    macro_df = pd.read_csv(macro_path, index_col=0, parse_dates=True)
    print("Loaded macro data from file.")
else:
    print("Fetching macro data from FRED...")
    cpi = fred.get_series("CPIAUCSL", observation_start=start_date, observation_end=end_date)
    treasury = fred.get_series("DGS10", observation_start=start_date, observation_end=end_date)
    natgas = fred.get_series("DHHNGSP", observation_start=start_date, observation_end=end_date)

    macro_df = pd.concat([cpi, treasury, natgas], axis=1)
    macro_df.columns = ["cpi", "10yr_yield", "natgas"]
    macro_df = macro_df.resample("W").mean().ffill().bfill()
    macro_df.to_csv(macro_path)

# === Step 2: Function to get stock returns ===
def get_weekly_returns(symbol, start_date, end_date):
    stock_path = f"data/{symbol}_returns.csv"
    if os.path.exists(stock_path):
        print(f"Loaded stock returns for {symbol} from file.")
        returns = pd.read_csv(stock_path, index_col=0, parse_dates=True)
    else:
        print(f"Downloading {symbol} data from Yahoo Finance...")
        df = yf.download(symbol, start=start_date, end=end_date, auto_adjust=True)
        if df.empty:
            raise ValueError(f"No data found for {symbol} in the specified range.")
        print(f"{symbol} date range: {df.index.min().date()} to {df.index.max().date()}")
        returns = df['Close'].resample('W').last().pct_change().dropna()
        if isinstance(returns, pd.Series):
            returns = returns.to_frame(name="weekly_return")
        else:
            returns.columns = ["weekly_return"]
        returns.to_csv(stock_path)
    return returns

# === Step 3: Run analysis per stock ===
all_r2_results = {}
for symbol in stock_symbols:
    print(f"\n--- Analyzing {symbol} ---")
    returns = get_weekly_returns(symbol, start_date, end_date)
    full_df = pd.concat([returns, macro_df], axis=1).dropna()
    full_df['delta_yield'] = full_df['10yr_yield'].diff()
    full_df = full_df.dropna()
    print(f"{symbol} return data starts: {returns.index.min()}")
    print("Columns in full_df:", full_df.columns)

    # === Step 4: Lag Sweep ===
    # Step: Run lag sweep for each macro variable
    macro_df['delta_yield'] = macro_df['10yr_yield'].diff()
    macro_vars = ['delta_yield', 'cpi', 'natgas']
    best_lags = {}
    r2_scores_all = {}
    for var in macro_vars:
        best_lag, best_r2, r2_scores = find_best_lag(returns, macro_df[var], max_lag=12)
        # This assumes your `find_best_lag` returns (best_lag, best_r2, r2_scores)
        all_r2_results[f"{symbol}_{var}"] = r2_scores
        r2_scores_all[var] = r2_scores

        best_lags[var] = best_lag
        print(f"Best lag for {var}: {best_lag} weeks (Adj. R² = {best_r2:.4f})")

    # Apply best lags
    for feature in ['delta_yield', 'cpi', 'natgas']:
        lag = best_lags[feature]
        full_df[f'{feature}_lag'] = full_df[feature].shift(lag)
    full_df = full_df.dropna()

    # === Step 5: Regression with Lagged Features ===
    X = full_df[[f"{f}_lag" for f in ['delta_yield', 'cpi', 'natgas']]]
    y = full_df['weekly_return']
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    print(model.summary())

    # Save regression summary
    with open(f"data/{symbol}_regression_summary.txt", "w") as f:
        f.write(model.summary().as_text())

    # Plots
    mp.plot_lag_r2_scores(r2_scores_all, symbol)
    mp.plot_regression_scatter(full_df, [f"{f}_lag" for f in ['delta_yield', 'cpi', 'natgas']], title=f"{symbol} Lagged Regression")

print("Analysis complete.")

mp.plot_adj_r2_by_lag(all_r2_results, lag_range=range(13), output_path="plots/adj_r2_by_lag.png")
