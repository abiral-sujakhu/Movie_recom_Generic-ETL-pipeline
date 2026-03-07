import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_eda(df: pd.DataFrame, file_stem: str, out_dir: str) -> list[str]:
    """
    Run EDA on a DataFrame and save all outputs to out_dir.

    Parameters
    ----------
    df        : transformed DataFrame to analyse
    file_stem : base name used for output files (e.g. 'movies_transformed')
    out_dir   : folder where PNGs and CSVs are saved

    Returns
    -------
    List of paths to every PNG file that was saved.
    """
    os.makedirs(out_dir, exist_ok=True)
    saved_pngs: list[str] = []

    if df.empty:
        print(f"[WARN] DataFrame is empty — skipping EDA for '{file_stem}'")
        return saved_pngs

    # ── Summary stats ─────────────────────────────────────────────────────────
    summary_path = os.path.join(out_dir, f"{file_stem}_summary.csv")
    df.describe(include="all").to_csv(summary_path)
    print(f"[INFO] Summary stats → {summary_path}")

    numeric_df = df.select_dtypes(include="number")
    cat_cols   = df.select_dtypes(include="object").columns.tolist()

    # ── Correlation & covariance ───────────────────────────────────────────────
    if len(numeric_df.columns) >= 2:
        numeric_df.corr().to_csv(os.path.join(out_dir, f"{file_stem}_correlation.csv"))
        numeric_df.cov().to_csv(os.path.join(out_dir, f"{file_stem}_covariance.csv"))
        print("[INFO] Skewness:\n", numeric_df.skew())
        print("[INFO] Kurtosis:\n", numeric_df.kurtosis())

        # Correlation heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm",
                    center=0, linewidths=0.5, ax=ax)
        ax.set_title(f"Correlation — {file_stem}")
        plt.tight_layout()
        path = os.path.join(out_dir, f"{file_stem}_heatmap.png")
        fig.savefig(path, dpi=100, bbox_inches="tight")
        saved_pngs.append(path)
        plt.close(fig)

        # Histograms per numeric column
        for col in numeric_df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(numeric_df[col].dropna(), bins=20, kde=True, ax=ax)
            ax.set_title(f"{col} Distribution")
            plt.tight_layout()
            path = os.path.join(out_dir, f"{file_stem}_{col}_hist.png")
            fig.savefig(path, dpi=100, bbox_inches="tight")
            saved_pngs.append(path)
            plt.close(fig)

    # ── Categorical top-10 bar charts ─────────────────────────────────────────
    for col in cat_cols:
        top = df[col].value_counts().head(10)
        if top.empty:
            continue
        fig, ax = plt.subplots(figsize=(8, 3))
        sns.barplot(x=top.values, y=top.index, ax=ax)
        ax.set_title(f"Top 10: {col}")
        plt.tight_layout()
        path = os.path.join(out_dir, f"{file_stem}_{col}_top10.png")
        fig.savefig(path, dpi=100, bbox_inches="tight")
        saved_pngs.append(path)
        plt.close(fig)

    print(f"[INFO] EDA complete — {len(saved_pngs)} plots saved to '{out_dir}'")
    return saved_pngs
