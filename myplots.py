import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set consistent theme and output directory
sns.set_theme(style="whitegrid", context="paper")
FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

# Mapping for feature labels
FEATURE_LABELS = {
    'delta_yield': 'Δ Yield (bp)',
    'vix': 'VIX (Index)',
    'natgas': 'NatGas (USD)',
}

# Short firm labels
FIRM_LABELS = {'DUK': 'Duke', 'SO': 'Southern', 'NEE': 'NextEra'}


def plot_adj_r2_by_lag(r2_dict, lag_range, symbol):
    """Plot adjusted R² across lags for each macro variable and firm."""
    plt.figure(figsize=(10, 6))
    for variable, r2_values in r2_dict.items():
        firm, var = variable.split('_', 1)
        label = f"{FIRM_LABELS.get(firm, firm)}: {FEATURE_LABELS.get(var, var)}"
        plt.plot(lag_range, r2_values, label=label, linewidth=2, marker='o')

    plt.title(f"Adjusted R² Across Lags – {symbol}", fontsize=16)
    plt.xlabel("Lag (weeks)", fontsize=14)
    plt.ylabel("Adjusted R²", fontsize=14)
    # Improved legend: two columns, smaller font, outside plot
    plt.legend(title="Series", fontsize=8, title_fontsize=10,
               loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    output_path = os.path.join(FIGURES_DIR, f"adj_r2_by_lag_{symbol}.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def plot_lag_r2_scores(r2_scores_all, symbol):
    """Plot lag sweep R² scores for a single firm."""
    plt.figure(figsize=(8, 5))
    for var, scores in r2_scores_all.items():
        plt.plot(range(len(scores)), scores, marker='o', label=FEATURE_LABELS.get(var.replace('_lag',''), var))

    plt.title(f"Lag Sweep – Adjusted R² for {symbol}", fontsize=14)
    plt.xlabel("Lag (weeks)", fontsize=12)
    plt.ylabel("Adjusted R²", fontsize=12)
    plt.legend(loc='upper right', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    output_path = os.path.join(FIGURES_DIR, f"lag_r2_sweep_{symbol}.png")
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_regression_scatter_individual(df, feature, symbol):
    """
    Plot a single scatter of a lagged macro feature against weekly returns.
    Label axes dynamically based on feature units.
    """
    base_feature = feature.replace('_lag', '')
    xlabel = FEATURE_LABELS.get(base_feature, feature)
    ylabel = 'Weekly Return (%)'
    # convert to percent
    df_plot = df.copy()
    df_plot['weekly_return_pct'] = df_plot['weekly_return'] * 100

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.regplot(x=feature, y='weekly_return_pct', data=df_plot, ax=ax,
                scatter_kws={'s': 10, 'alpha': 0.6}, line_kws={'color': 'black'})
    ax.set_title(f"{symbol}: {xlabel} vs Weekly Return", fontsize=14)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.5)
    fig.tight_layout()

    output_path = os.path.join(FIGURES_DIR, f"scatter_{symbol}_{base_feature}.png")
    fig.savefig(output_path, dpi=300)
    plt.close()


def plot_macro_timeseries(df, columns, symbol):
    """
    Plots macroeconomic indicators over time for a given firm.
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    for col in columns:
        base = col.replace('_lag','')
        label = FEATURE_LABELS.get(base, col)
        ax.plot(df.index, df[col], label=label, linewidth=1.8)

    ax.set_title(f"Macroeconomic Indicators Over Time – {symbol}", fontsize=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    fig.tight_layout()

    output_path = os.path.join(FIGURES_DIR, f"macro_timeseries_{symbol}.png")
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_regression_scatter(df, features, symbol, title=None):
    """
    Wrapper to generate individual scatter plots for each lagged feature.
    Maintains legacy function name for compatibility.
    """
    for feature in features:
        plot_regression_scatter_individual(df, feature, symbol)
