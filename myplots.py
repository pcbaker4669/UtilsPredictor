import matplotlib.pyplot as plt
import seaborn as sns

def plot_regression_scatter(data, x_vars, y_var='weekly_return'):
    """
    Plots scatter plots with regression lines for each x variable vs the y variable.

    Parameters:
    - data: pandas DataFrame containing the data.
    - x_vars: list of column names to use as x variables.
    - y_var: the target variable (default: 'weekly_return')
    """
    for x_var in x_vars:
        plt.figure(figsize=(8, 6))
        sns.regplot(x=data[x_var], y=data[y_var], ci=95, line_kws={"color": "red"})
        plt.title(f'{y_var} vs {x_var}')
        plt.xlabel(x_var)
        plt.ylabel(y_var)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_macro_indicators(df):
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axs[0].plot(df.index, df['cpi'], label='CPI', color='tab:blue')
    axs[0].set_title('Consumer Price Index (CPI)')
    axs[0].set_ylabel('Index Level')
    axs[0].grid(True)

    axs[1].plot(df.index, df['10yr_yield'], label='10-Year Treasury Yield', color='tab:green')
    axs[1].set_title('10-Year Treasury Yield')
    axs[1].set_ylabel('Percent (%)')
    axs[1].grid(True)

    axs[2].plot(df.index, df['natgas'], label='Natural Gas Price', color='tab:red')
    axs[2].set_title('Henry Hub Natural Gas Price')
    axs[2].set_ylabel('Dollars per MMBtu')
    axs[2].grid(True)

    plt.xlabel('Date')
    plt.tight_layout()
    plt.show()
