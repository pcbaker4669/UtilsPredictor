# Utilities Stock Forecasting with Macroeconomic Indicators

This repository provides a reproducible forecasting model for U.S. utility stocks using macroeconomic variables. The project demonstrates how Treasury yields, inflation (CPI), and natural gas prices affect weekly returns of utility companies such as Duke Energy (DUK).

## Overview

Utility stocks are typically considered defensive, but they remain sensitive to macroeconomic pressures. This project explores whether simple macro indicators can predict short-term utility stock returns using linear regression.

## Project Structure

```
.
├── main.py              # Main analysis pipeline
├── myplots.py           # Plotting utilities for charts and figures
├── macro_data.csv       # FRED macroeconomic data (CPI, 10Y Yield, NatGas)
├── stock_returns.csv    # Weekly returns of Duke Energy (DUK)
├── README.md            # Project overview and instructions
```

## Setup

1. Clone the repository:
```bash
git clone https://github.com/pcbaker4669/UtilsPredictor.git
cd UtilsPredictor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your API keys in `main.py`:
```python
FRED_API_KEY = "your_fred_api_key"
POLYGON_API_KEY = "your_polygon_api_key"
```

## Running the Script

After setup, run:

```bash
python main.py
```

This script will:

- Load or download macroeconomic data
- Retrieve historical stock prices for DUK
- Run OLS regression
- Output model summary
- Generate and save plots to file

## Example Output

- OLS regression results
- Correlation matrix
- Scatter plots between weekly returns and macro indicators
- Line charts of macroeconomic indicators

## How to Cite

If you use this work for your own research or teaching:

> Baker, P. (2025). *Macroeconomic Signal-Driven Forecasting of U.S. Utility Stocks: A Simple Linear Model with Investment Implications*. GitHub repository: https://github.com/pcbaker4669/UtilsPredictor

## Future Work

- Add agent-based simulations for market dynamics
- Explore lagged features and interaction terms
- Deploy as a dashboard or interactive tool

## License

This project is released under the MIT License.
