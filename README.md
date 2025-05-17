# Forecasting Weekly Utility Stock Returns Using Macroeconomic Signals

## Overview

This project builds and runs a simple predictive model that estimates weekly returns of a utility stock (e.g., Duke Energy - DUK) using key macroeconomic variables. The model uses weekly changes in the 10-Year Treasury Yield, the Consumer Price Index (CPI), and Henry Hub Natural Gas prices to perform an ordinary least squares (OLS) regression.

The intended purpose is both academic (for publication as part of a PhD program) and practical (to monitor and potentially forecast utility stock performance based on economic signals).

## Features

- Downloads macroeconomic data from the Federal Reserve (FRED)
- Retrieves adjusted stock prices from Polygon.io
- Merges datasets into a weekly view
- Runs OLS regression to estimate influence of macro variables on stock returns
- Stores data locally to avoid redundant API calls
- Prints regression results and optionally plots trends

## Requirements

```bash
pip install pandas requests statsmodels matplotlib fredapi
```

## Setup

1. Get your **FRED API key**: https://fred.stlouisfed.org/docs/api/api_key.html
2. Get your **Polygon.io API key**: https://polygon.io/
3. Save them inside the Python script as:
    ```python
    FRED_API_KEY = "your_fred_key_here"
    POLYGON_API_KEY = "your_polygon_key_here"
    ```

4. To avoid excessive API calls, macroeconomic data and stock return data are stored locally as:
    - `macro_data.csv`
    - `stock_returns.csv`

## Running the Script

Run the script directly:
```bash
python stock_model.py
```

This will:
- Check if the data files exist
- Download them if not
- Merge the datasets
- Run and print a linear regression model
- Save the output for further analysis

## File Descriptions

| File Name           | Description |
|---------------------|-------------|
| `stock_model.py`    | Main script to fetch data and run regression |
| `macro_data.csv`    | Weekly CPI, Treasury yield, and NatGas prices |
| `stock_returns.csv` | Weekly return percentage of selected utility stock |
| `README.md`         | Project overview and documentation |

## Sample Output

```
Dep. Variable:          weekly_return   R-squared:                       0.251
Model:                            OLS   Adj. R-squared:                  0.196
...
delta_yield    -0.0439      0.013     -3.284      0.002
```

## Limitations

- The regression does not include company-specific fundamentals (e.g., P/E ratio, debt levels).
- Assumes linear relationships between macro variables and stock returns.
- Only supports weekly returns for now.
- Current model does not test for multicollinearity or autocorrelation.

## Author

Peter C. Baker  
PhD Student in Computational Social Sciences, George Mason University  
Specializing in Global Policy, Commerce, and Infrastructure Economics  

## Citation

Please cite this project as:

> Baker, P. (2025). Predicting Weekly Utility Stock Returns Using Macroeconomic Indicators. Computational Social Science Research Archive.
