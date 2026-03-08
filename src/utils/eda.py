import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_eda(df: pd.DataFrame) -> dict:
    """
    Compute EDA statistics and return them in a dict. Nothing is written to disk.

    Returns a dict with keys:
      1. overview             : dict  — shape, dtypes, columns, memory_usage_mb
      2. missing              : pd.DataFrame — count + % per column (only cols with nulls)
      3. duplicates           : dict  — total_rows, duplicate_rows, duplicate_pct
      4. summary              : pd.DataFrame — df.describe(include='all')
      5. unique_values        : pd.DataFrame — unique count + sample values per column
      6. genre_frequency      : pd.Series (or None) — exploded genre counts
      7. year_stats           : dict (or None) — min/max/median/mode/counts per year
      8. correlation          : pd.DataFrame (or None)
         covariance           : pd.DataFrame (or None)
         skewness             : pd.Series (or None)
         kurtosis             : pd.Series (or None)
      9. sample_records       : dict — head, tail, random_sample (5 rows each)
    """
    result = {
        # legacy keys kept for backward compatibility
        "summary": None, "missing": None,
        "skewness": None, "kurtosis": None,
        "correlation": None, "covariance": None,
        # new keys
        "overview": None, "duplicates": None,
        "unique_values": None, "genre_frequency": None,
        "year_stats": None, "sample_records": None,
    }

    if df.empty:
        return result

    # ── 1. Dataset overview ───────────────────────────────────────────────────
    result["overview"] = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "memory_usage_mb": round(df.memory_usage(deep=True).sum() / 1024 ** 2, 3),
    }

    # ── 2. Missing value analysis ─────────────────────────────────────────────
    miss_count = df.isnull().sum()
    miss_pct   = (miss_count / len(df) * 100).round(2)
    miss_df    = pd.DataFrame({"missing_count": miss_count, "missing_pct": miss_pct})
    result["missing"] = miss_df[miss_df["missing_count"] > 0]

    # ── 3. Duplicate detection ────────────────────────────────────────────────
    dup_count = int(df.duplicated().sum())
    result["duplicates"] = {
        "total_rows":     df.shape[0],
        "duplicate_rows": dup_count,
        "duplicate_pct":  round(dup_count / df.shape[0] * 100, 2),
    }

    # ── 4. Descriptive statistics ─────────────────────────────────────────────
    result["summary"] = df.describe(include="all")

    # ── 5. Unique value analysis ──────────────────────────────────────────────
    uniq_rows = []
    for col in df.columns:
        n_unique = df[col].nunique(dropna=False)
        samples  = df[col].dropna().unique()[:5].tolist()
        uniq_rows.append({
            "column":       col,
            "unique_count": n_unique,
            "sample_values": str(samples),
        })
    result["unique_values"] = pd.DataFrame(uniq_rows).set_index("column")

    # ── 6. Genre frequency analysis ───────────────────────────────────────────
    if "genres" in df.columns:
        genre_series = (
            df["genres"].dropna()
            .str.split(",")
            .explode()
            .str.strip()
            .str.title()
        )
        result["genre_frequency"] = genre_series[genre_series != ""].value_counts()

    # ── 7. Release year statistics ────────────────────────────────────────────
    if "year" in df.columns:
        years = df["year"].dropna().astype(int)
        yearly_counts = years.value_counts().sort_index()
        result["year_stats"] = {
            "min_year":        int(years.min()),
            "max_year":        int(years.max()),
            "median_year":     int(years.median()),
            "most_common_year": int(years.mode().iloc[0]),
            "counts_per_year": yearly_counts,
        }

    # ── 8. Correlation analysis ───────────────────────────────────────────────
    numeric_df = df.select_dtypes(include="number")
    if len(numeric_df.columns) >= 2:
        result["correlation"] = numeric_df.corr()
        result["covariance"]  = numeric_df.cov()
        result["skewness"]    = numeric_df.skew()
        result["kurtosis"]    = numeric_df.kurtosis()

    # ── 9. Record inspection ──────────────────────────────────────────────────
    sample_n = min(5, len(df))
    result["sample_records"] = {
        "head":          df.head(sample_n),
        "tail":          df.tail(sample_n),
        "random_sample": df.sample(sample_n, random_state=42) if len(df) >= sample_n else df.copy(),
    }

    return result


def run_visualizations(df: pd.DataFrame) -> list:
    """
    Generate movie-specific matplotlib figures for a transformed dataset.

    Returns a list of (category, title, Figure) tuples where category is one of:
      'ratings', 'trends', 'genres', 'people', 'technical', 'correlations'
    """
    figures = []

    if df.empty:
        return figures

    numeric_df = df.select_dtypes(include="number")

    # ── Ratings ───────────────────────────────────────────────────────────────
    if "rating" in df.columns:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.kdeplot(df["rating"].dropna(), ax=ax, fill=True, alpha=0.4, color="steelblue")
        ax.set_title("Rating Distribution")
        ax.set_xlabel("Rating")
        plt.tight_layout()
        figures.append(("ratings", "Rating Distribution", fig))

    if "rating" in df.columns and "title" in df.columns:
        top10 = df.dropna(subset=["rating", "title"]).nlargest(10, "rating")[["title", "rating"]].sort_values("rating")
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.barh(range(len(top10)), top10["rating"].values, color="steelblue")
        ax.set_yticks(range(len(top10)))
        ax.set_yticklabels([t[:35] + "…" if len(t) > 35 else t for t in top10["title"]], fontsize=9)
        ax.set_xlabel("Rating")
        ax.set_title("Top 10 Highest Rated Movies")
        ax.set_xlim(left=top10["rating"].min() - 0.5)
        plt.tight_layout()
        figures.append(("ratings", "Top 10 Rated", fig))

    if "rating" in df.columns and "popularity" in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        sample = df.dropna(subset=["rating", "popularity"])
        ax.scatter(sample["rating"], sample["popularity"], alpha=0.4, s=20, color="steelblue")
        ax.set_title("Rating vs Popularity")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Popularity")
        plt.tight_layout()
        figures.append(("ratings", "Rating vs Popularity", fig))

    if "rating" in df.columns and "vote_count" in df.columns:
        fig, ax = plt.subplots(figsize=(8, 5))
        sample = df.dropna(subset=["rating", "vote_count"])
        ax.scatter(sample["vote_count"], sample["rating"], alpha=0.4, s=20, color="darkorange")
        ax.set_title("Vote Count vs Rating")
        ax.set_xlabel("Vote Count")
        ax.set_ylabel("Rating")
        ax.ticklabel_format(style="plain", axis="x")
        plt.tight_layout()
        figures.append(("ratings", "Votes vs Rating", fig))

    # ── Trends over time ──────────────────────────────────────────────────────
    if "year" in df.columns:
        yearly = df["year"].dropna().astype(int)
        counts = yearly.value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(counts.index, counts.values, color="steelblue", width=0.8)
        ax.set_title("Movies Released per Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Count")
        plt.tight_layout()
        figures.append(("trends", "Movies per Year", fig))

        # Movies by decade
        decades = (yearly // 10 * 10).value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar([str(d) + "s" for d in decades.index], decades.values, color="teal", edgecolor="black")
        ax.set_xlabel("Decade")
        ax.set_ylabel("Number of Movies")
        ax.set_title("Movies by Decade")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        figures.append(("trends", "Movies by Decade", fig))

        if "rating" in df.columns:
            avg_rating = df.dropna(subset=["year", "rating"]).groupby("year")["rating"].mean()
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(avg_rating.index, avg_rating.values, color="tomato", linewidth=1.5)
            ax.set_title("Average Rating per Year")
            ax.set_xlabel("Year")
            ax.set_ylabel("Avg Rating")
            plt.tight_layout()
            figures.append(("trends", "Avg Rating per Year", fig))

    # ── Genres ────────────────────────────────────────────────────────────────
    if "genres" in df.columns:
        genre_series = (
            df["genres"].dropna()
            .str.split(",")
            .explode()
            .str.strip()
            .str.title()
        )
        genre_counts = genre_series[genre_series != ""].value_counts().head(15)
        if not genre_counts.empty:
            fig, ax = plt.subplots(figsize=(9, 5))
            sns.barplot(x=genre_counts.values, y=genre_counts.index, ax=ax, color="mediumseagreen")
            ax.set_title("Top 15 Genres (exploded)")
            ax.set_xlabel("Count")
            plt.tight_layout()
            figures.append(("genres", "Top Genres", fig))

        if "rating" in df.columns:
            top_genres = genre_series.value_counts().head(10).index.tolist()
            rows = []
            for _, row in df.dropna(subset=["genres", "rating"]).iterrows():
                for g in str(row["genres"]).split(","):
                    g = g.strip().title()
                    if g in top_genres:
                        rows.append({"genre": g, "rating": row["rating"]})
            if rows:
                genre_rating_df = pd.DataFrame(rows)
                order = genre_rating_df.groupby("genre")["rating"].median().sort_values(ascending=False).index
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.boxplot(data=genre_rating_df, x="rating", y="genre", order=order, ax=ax, color="lightskyblue")
                ax.set_title("Rating Distribution by Genre")
                ax.set_xlabel("Rating")
                plt.tight_layout()
                figures.append(("genres", "Rating by Genre", fig))

    # ── People ────────────────────────────────────────────────────────────────
    if "director" in df.columns:
        top_directors = df["director"].dropna().value_counts().head(15)
        if not top_directors.empty:
            fig, ax = plt.subplots(figsize=(9, 5))
            sns.barplot(x=top_directors.values, y=top_directors.index, ax=ax, color="mediumpurple")
            ax.set_title("Top 15 Most Frequent Directors")
            ax.set_xlabel("Movie Count")
            plt.tight_layout()
            figures.append(("people", "Top Directors", fig))

    if "language" in df.columns:
        top_langs = df["language"].dropna().value_counts().head(12)
        if not top_langs.empty:
            fig, ax = plt.subplots(figsize=(9, 4))
            sns.barplot(x=top_langs.values, y=top_langs.index, ax=ax, color="coral")
            ax.set_title("Top 12 Languages")
            ax.set_xlabel("Count")
            plt.tight_layout()
            figures.append(("people", "Top Languages", fig))

    if "country" in df.columns:
        top_countries = df["country"].dropna().value_counts().head(12)
        if not top_countries.empty:
            fig, ax = plt.subplots(figsize=(9, 4))
            sns.barplot(x=top_countries.values, y=top_countries.index, ax=ax, color="goldenrod")
            ax.set_title("Top 12 Countries")
            ax.set_xlabel("Count")
            plt.tight_layout()
            figures.append(("people", "Top Countries", fig))

    # ── Technical ─────────────────────────────────────────────────────────────
    if "runtime" in df.columns:
        rt = df["runtime"].dropna()
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(rt, bins=30, kde=True, ax=ax, color="slategray")
        ax.set_title("Runtime Distribution (minutes)")
        ax.set_xlabel("Runtime (min)")
        plt.tight_layout()
        figures.append(("technical", "Runtime Distribution", fig))

        if "rating" in df.columns:
            tmp = df.dropna(subset=["runtime", "rating"]).copy()
            bins = [0, 90, 120, 150, 9999]
            labels = ["Short (<90m)", "Medium (90-120m)", "Long (120-150m)", "Very Long (>150m)"]
            tmp["runtime_cat"] = pd.cut(tmp["runtime"], bins=bins, labels=labels)
            fig, ax = plt.subplots(figsize=(9, 5))
            order = [l for l in labels if l in tmp["runtime_cat"].cat.categories]
            sns.boxplot(data=tmp, x="runtime_cat", y="rating", order=order, ax=ax, palette="Blues")
            ax.set_title("Rating by Runtime Category")
            ax.set_xlabel("Runtime Category")
            ax.set_ylabel("Rating")
            plt.tight_layout()
            figures.append(("technical", "Rating by Runtime Category", fig))

    # ── Correlations ──────────────────────────────────────────────────────────
    if len(numeric_df.columns) >= 2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm",
                    center=0, linewidths=0.5, ax=ax)
        ax.set_title("Correlation Heatmap")
        plt.tight_layout()
        figures.append(("correlations", "Correlation Heatmap", fig))

    return figures
