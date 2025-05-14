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
    label_map = {
        'cpi': 'Consumer Price Index (CPI)',
        'natgas': 'Henry Hub Natural Gas ($/MMBtu)',
        'delta_yield': 'Change in 10-Year Treasury Yield (%)',
        'weekly_return': 'Weekly Return of Utility Stock (%)'
    }

    for x_var in x_vars:
        plt.figure(figsize=(8, 6))
        sns.regplot(x=data[x_var], y=data[y_var], ci=95, line_kws={"color": "red"})
        plt.title(f'{label_map.get(y_var, y_var)} vs {label_map.get(x_var, x_var)}', fontsize=14)
        plt.xlabel(label_map.get(x_var, x_var), fontsize=12)
        plt.ylabel(label_map.get(y_var, y_var), fontsize=12)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{x_var}.png", dpi=300)
        plt.show()


def plot_macro_indicators(data):
    """
    Plots individual line plots for key macro indicators and
    a combined subplot chart for CPI, Treasury Yield, and Natural Gas.
    Saves each figure as a PNG.
    """
    import seaborn as sns

    columns_to_plot = ['weekly_return', 'cpi', '10yr_yield', 'natgas']
    title_map = {
        'weekly_return': 'Weekly Stock Return (%)',
        'cpi': 'Consumer Price Index (CPI)',
        '10yr_yield': '10-Year Treasury Yield (%)',
        'natgas': 'Henry Hub Natural Gas Price ($/MMBtu)'
    }

    # --- Plot each individually ---
    for col in columns_to_plot:
        if col in data.columns:
            plt.figure(figsize=(10, 4))
            sns.lineplot(x=data.index, y=data[col])
            plt.title(title_map.get(col, col), fontsize=14, pad=15)
            plt.xlabel("Date")
            plt.ylabel(title_map.get(col, col))
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.savefig(f"{col}.png")
            plt.close()

    # --- Create Combined Macro Indicator Chart ---
    if all(col in data.columns for col in ['cpi', '10yr_yield', 'natgas']):
        fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

        axs[0].plot(data.index, data['cpi'], color='blue')
        axs[0].set_title('Consumer Price Index (CPI)')
        axs[0].set_ylabel('Index Level')

        axs[1].plot(data.index, data['10yr_yield'], color='green')
        axs[1].set_title('10-Year Treasury Yield')
        axs[1].set_ylabel('Percent (%)')

        axs[2].plot(data.index, data['natgas'], color='red')
        axs[2].set_title('Henry Hub Natural Gas Price')
        axs[2].set_ylabel('Dollars per MMBtu')
        axs[2].set_xlabel('Date')

        plt.tight_layout()
        plt.savefig("macro_indicators_combined.png")
        plt.show()