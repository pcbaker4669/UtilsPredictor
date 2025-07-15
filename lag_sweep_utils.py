import pandas as pd
import statsmodels.api as sm
import numpy as np
import seaborn as sns

def find_best_lag(returns_df, macro_series, max_lag=12):
    r2_scores = []
    for lag in range(max_lag + 1):
        lagged_macro = macro_series.shift(lag)
        temp_df = pd.concat([returns_df, lagged_macro.rename(
            f"{macro_series.name}_lag")], axis=1).dropna()
        if temp_df.empty:
            r2_scores.append(float('-inf'))
            continue
        X = sm.add_constant(temp_df[f"{macro_series.name}_lag"])
        y = temp_df["weekly_return"]
        model = sm.OLS(y, X).fit()
        r2_scores.append(model.rsquared_adj)

    best_lag = int(np.argmax(r2_scores))
    best_r2 = r2_scores[best_lag]
    return best_lag, best_r2, r2_scores