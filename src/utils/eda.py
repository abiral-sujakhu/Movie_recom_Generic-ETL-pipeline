import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_eda(df: pd.DataFrame) -> dict:
    """
    Compute EDA statistics and return them in a dict. Nothing is written to disk.

    Returns a dict with keys:
      summary    : pd.DataFrame
      missing    : pd.Series
      skewness   : pd.Series  (or None)
      kurtosis   : pd.Series  (or None)
      correlation: pd.DataFrame (or None)
      covariance : pd.DataFrame (or None)
    """
    result = {
        "summary": None, "missing": None,
        "skewness": None, "kurtosis": None,
        "correlation": None, "covariance": None,
    }

    if df.empty:
        return result

    result["summary"] = df.describe(include="all")

    missing = df.isnull().sum()
    result["missing"] = missing[missing > 0]

    numeric_df = df.select_dtypes(include="number")
    if len(numeric_df.columns) >= 2:
        result["correlation"] = numeric_df.corr()
        result["covariance"]  = numeric_df.cov()
        result["skewness"]    = numeric_df.skew()
        result["kurtosis"]    = numeric_df.kurtosis()

    return result


def run_visualizations(df: pd.DataFrame) -> list:
    """
    Generate matplotlib figures for the DataFrame. Nothing is written to disk.

    Returns a list of (title, Figure) tuples.
    """
    figures = []

    if df.empty:
        return figures

    numeric_df = df.select_dtypes(include="number")
    cat_cols   = df.select_dtypes(include="object").columns.tolist()

    # Correlation heatmap
    if len(numeric_df.columns) >= 2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm",
                    center=0, linewidths=0.5, ax=ax)
        ax.set_title("Correlation Heatmap")
        plt.tight_layout()
        figures.append(("Correlation Heatmap", fig))

        # Histograms per numeric column
        for col in numeric_df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(numeric_df[col].dropna(), bins=20, kde=True, ax=ax)
            ax.set_title(f"{col} Distribution")
            plt.tight_layout()
            figures.append((col, fig))

    # Categorical top-10 bar charts
    for col in cat_cols:
        top = df[col].value_counts().head(10)
        if top.empty:
            continue
        fig, ax = plt.subplots(figsize=(8, 3))
        sns.barplot(x=top.values, y=top.index, ax=ax)
        ax.set_title(f"Top 10: {col}")
        plt.tight_layout()
        figures.append((f"Top 10: {col}", fig))

    return figures
