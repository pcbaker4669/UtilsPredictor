import matplotlib.pyplot as plt
import os
import seaborn as sns


def plot_adj_r2_by_lag(r2_dict, lag_range, output_path):
    plt.figure(figsize=(10, 6))
    for variable, r2_values in r2_dict.items():
        plt.plot(lag_range, r2_values, label=variable, linewidth=2, marker='o')

    plt.title("Adjusted R² Across Lags", fontsize=16)
    plt.xlabel("Lag (weeks)", fontsize=14)
    plt.ylabel("Adjusted R²", fontsize=14)
    plt.legend(title="Macro Variable")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_lag_r2_scores(r2_scores_dict, symbol):
    """
    Plot R² values across lags for each macro variable.
    Parameters:
        r2_scores_dict: dict where key = variable name, value = list of R² values by lag
        symbol: str, stock symbol being analyzed
    """
    plt.figure(figsize=(10, 6))
    for var, r2_scores in r2_scores_dict.items():
        plt.plot(range(len(r2_scores)), r2_scores, label=var)

    plt.xlabel("Lag (weeks)", fontsize=12)
    plt.ylabel("Adjusted R²", fontsize=12)
    plt.title(f"Lag Sweep - Adjusted R² for {symbol}", fontsize=14)
    plt.legend(title="Macro Variable")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"lag_r2_sweep_{symbol}.png", dpi=300)
    plt.close()

def plot_regression_scatter(df, features, title="Regression Scatter Plot", output_path=None):
    """
    Plots scatter plots of each lagged macro feature against weekly_return.

    Parameters:
    - df: DataFrame with 'weekly_return' and lagged features
    - features: list of lagged feature column names
    - title: plot title
    - output_path: if provided, saves the figure to this path
    """
    sns.set(style="whitegrid", context="talk")
    num_vars = len(features)
    fig, axs = plt.subplots(1, num_vars, figsize=(6 * num_vars, 5))

    if num_vars == 1:
        axs = [axs]

    for i, feature in enumerate(features):
        sns.regplot(x=feature, y='weekly_return', data=df, ax=axs[i], scatter_kws={'s': 10}, line_kws={'color': 'red'})
        axs[i].set_title(f"{feature} vs Return")
        axs[i].set_xlabel(feature)
        axs[i].set_ylabel("Weekly Return")

    fig.suptitle(title, fontsize=18)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    if output_path:
        plt.savefig(output_path, dpi=300)
    else:
        plt.show()

    plt.close()