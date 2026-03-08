import base64
import io
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ── helpers ───────────────────────────────────────────────────────────────────

def _fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    return encoded


def _df_to_html(df: pd.DataFrame, classes="data-table") -> str:
    return df.to_html(classes=classes, border=0, na_rep="—")


# ── chart builders ────────────────────────────────────────────────────────────

def _chart_rating_dist(df: pd.DataFrame) -> str | None:
    rating_cols = [c for c in ["tmdb_rating", "imdb_rating"] if c in df.columns]
    if not rating_cols:
        return None
    fig, ax = plt.subplots(figsize=(10, 4))
    for col in rating_cols:
        ax.hist(df[col].dropna(), bins=25, alpha=0.7, label=col.replace("_", " ").title())
    ax.set_xlabel("Rating"); ax.set_ylabel("Frequency")
    ax.set_title("Rating Distribution"); ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout()
    return _fig_to_b64(fig)


def _chart_corr_heatmap(df: pd.DataFrame) -> str | None:
    num = df.select_dtypes(include="number")
    if len(num.columns) < 2:
        return None
    fig, ax = plt.subplots(figsize=(10, 7))
    sns.heatmap(num.corr(), annot=True, fmt=".2f", cmap="coolwarm",
                center=0, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Matrix")
    plt.tight_layout()
    return _fig_to_b64(fig)


def _chart_movies_per_year(df: pd.DataFrame) -> str | None:
    if "year" not in df.columns:
        return None
    fig, ax = plt.subplots(figsize=(10, 4))
    counts = df.groupby("year").size().reset_index(name="count")
    ax.plot(counts["year"], counts["count"], marker="o", linewidth=2, markersize=3, color="#5B9BD5")
    ax.fill_between(counts["year"], counts["count"], alpha=0.3, color="#5B9BD5")
    ax.set_xlabel("Year"); ax.set_ylabel("Movies"); ax.set_title("Movies Released Per Year")
    ax.grid(alpha=0.3); plt.tight_layout()
    return _fig_to_b64(fig)


def _chart_top_genres(df: pd.DataFrame) -> str | None:
    if "genres" not in df.columns:
        return None
    items = []
    for v in df["genres"].dropna():
        items.extend([x.strip() for x in str(v).split(",")])
    if not items:
        return None
    counts = pd.Series(items).value_counts().head(15)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(counts.index[::-1], counts.values[::-1], color="#70AD47", edgecolor="black")
    ax.set_xlabel("Count"); ax.set_title("Top Genres"); ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    return _fig_to_b64(fig)


def _chart_histograms(df: pd.DataFrame) -> list[tuple[str, str]]:
    num = df.select_dtypes(include="number")
    results = []
    for col in num.columns:
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.histplot(num[col].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title(f"{col} Distribution"); plt.tight_layout()
        results.append((col, _fig_to_b64(fig)))
    return results


def _chart_top10_cats(df: pd.DataFrame) -> list[tuple[str, str]]:
    results = []
    for col in df.select_dtypes(include="object").columns:
        top = df[col].value_counts().head(10)
        if top.empty:
            continue
        fig, ax = plt.subplots(figsize=(8, 3))
        sns.barplot(x=top.values, y=top.index, ax=ax)
        ax.set_title(f"Top 10: {col}"); plt.tight_layout()
        results.append((col, _fig_to_b64(fig)))
    return results


# ── HTML template ─────────────────────────────────────────────────────────────

_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',sans-serif; background:#f0f2f5; padding:24px; color:#333; }
.container { max-width:1300px; margin:0 auto; background:#fff;
             border-radius:12px; box-shadow:0 4px 24px rgba(0,0,0,.12); overflow:hidden; }
.header { background:linear-gradient(135deg,#667eea,#764ba2);
          color:#fff; padding:40px; text-align:center; }
.header h1 { font-size:2.2em; margin-bottom:8px; }
.header p  { opacity:.9; }
.kpi-row { display:flex; flex-wrap:wrap; gap:16px; padding:32px;
            background:#f8f9fa; justify-content:center; }
.kpi { background:#fff; padding:20px 28px; border-radius:10px;
       box-shadow:0 2px 8px rgba(0,0,0,.08); text-align:center;
       border-left:4px solid #667eea; min-width:160px; }
.kpi h3 { color:#667eea; font-size:1.9em; }
.kpi p  { color:#666; font-size:.85em; margin-top:4px; }
.section { padding:32px; }
.section h2 { color:#667eea; border-bottom:3px solid #667eea;
              padding-bottom:8px; margin-bottom:20px; font-size:1.5em; }
.section h3 { color:#444; margin:20px 0 8px; font-size:1.1em; }
.chart { margin:16px 0; text-align:center; }
.chart img { max-width:100%; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,.1); }
.grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:20px; }
.grid-3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; }
.data-table { width:100%; border-collapse:collapse; margin:8px 0;
              box-shadow:0 2px 8px rgba(0,0,0,.08); border-radius:8px; overflow:hidden; }
.data-table thead { background:linear-gradient(135deg,#667eea,#764ba2); color:#fff; }
.data-table th { padding:12px 14px; text-align:left; font-weight:600; }
.data-table td { padding:10px 14px; border-bottom:1px solid #eee; }
.data-table tbody tr:nth-child(even) { background:#f9f9f9; }
.footer { background:#2c3e50; color:#fff; text-align:center; padding:18px; font-size:.85em; }
@media(max-width:768px){ .grid-2,.grid-3 { grid-template-columns:1fr; } }
"""


def _img_tag(b64: str) -> str:
    return f'<img src="data:image/png;base64,{b64}" alt="chart">'


def generate_html_report(df: pd.DataFrame, dataset_name: str) -> str:
    """
    Generate a self-contained HTML report for *df* and return it as a string.
    All charts are embedded as base64 PNGs — no files written to disk.
    """
    ts = datetime.now().strftime("%B %d, %Y at %H:%M")
    num = df.select_dtypes(include="number")

    # ── KPIs ──────────────────────────────────────────────────────────────────
    kpi_items = [("Total Rows", f"{len(df):,}"), ("Columns", str(len(df.columns)))]
    for col, label in [("year", "Year Range"), ("imdb_rating", "Avg IMDb"),
                       ("tmdb_rating", "Avg TMDB"), ("runtime", "Avg Runtime (min)"),
                       ("director", "Directors"), ("title", "Titles")]:
        if col not in df.columns:
            continue
        if label == "Year Range":
            kpi_items.append((label, f"{int(df[col].min())}–{int(df[col].max())}"))
        elif label in ("Avg IMDb", "Avg TMDB"):
            kpi_items.append((label, f"{df[col].mean():.2f}"))
        elif label == "Avg Runtime (min)":
            kpi_items.append((label, f"{df[col].mean():.0f}"))
        elif label == "Directors":
            kpi_items.append((label, f"{df[col].nunique():,}"))
        elif label == "Titles":
            kpi_items.append((label, f"{df[col].nunique():,}"))

    kpi_html = "".join(
        f'<div class="kpi"><h3>{v}</h3><p>{k}</p></div>' for k, v in kpi_items
    )

    # ── Charts ────────────────────────────────────────────────────────────────
    b64_rating   = _chart_rating_dist(df)
    b64_year     = _chart_movies_per_year(df)
    b64_genres   = _chart_top_genres(df)
    b64_corr     = _chart_corr_heatmap(df)
    hist_list    = _chart_histograms(df)
    cat_list     = _chart_top10_cats(df)

    def maybe(b64, title=""):
        if not b64:
            return ""
        head = f"<h3>{title}</h3>" if title else ""
        return f'{head}<div class="chart">{_img_tag(b64)}</div>'

    charts_row1 = ""
    if b64_rating and b64_year:
        charts_row1 = (
            f'<div class="grid-2">'
            f'<div class="chart">{_img_tag(b64_rating)}</div>'
            f'<div class="chart">{_img_tag(b64_year)}</div>'
            f'</div>'
        )
    elif b64_rating:
        charts_row1 = maybe(b64_rating)
    elif b64_year:
        charts_row1 = maybe(b64_year)

    hists_html = ""
    if hist_list:
        items = "".join(f'<div class="chart">{_img_tag(b)}</div>' for _, b in hist_list)
        hists_html = f'<h3>Distributions</h3><div class="grid-3">{items}</div>'

    cats_html = "".join(
        f'<h3>Top 10: {col}</h3><div class="chart">{_img_tag(b)}</div>'
        for col, b in cat_list
    )

    # ── Top movies table ──────────────────────────────────────────────────────
    top_movies_html = ""
    rating_col = next((c for c in ["imdb_rating", "tmdb_rating"] if c in df.columns), None)
    if rating_col:
        show_cols = [c for c in ["title", "year", "director", "genres", "imdb_rating", "tmdb_rating", "runtime"]
                     if c in df.columns]
        top_movies_html = _df_to_html(df.nlargest(20, rating_col)[show_cols].reset_index(drop=True))

    # ── Summary stats table ───────────────────────────────────────────────────
    summary_html = _df_to_html(df.describe(include="all").T.reset_index().rename(columns={"index": "column"}))

    # ── Assemble HTML ─────────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Report — {dataset_name}</title>
<style>{_CSS}</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>🎬 {dataset_name}</h1>
    <p>Generated on {ts}</p>
  </div>

  <div class="kpi-row">{kpi_html}</div>

  <div class="section">
    <h2>📊 Charts</h2>
    {charts_row1}
    {maybe(b64_genres, "Top Genres")}
    {maybe(b64_corr,   "Correlation Heatmap")}
    {hists_html}
    {cats_html}
  </div>

  {'<div class="section"><h2>🏆 Top 20 Movies</h2>' + top_movies_html + '</div>' if top_movies_html else ''}

  <div class="section">
    <h2>📋 Summary Statistics</h2>
    {summary_html}
  </div>

  <div class="footer">Movie Analysis Report · {datetime.now().year}</div>
</div>
</body>
</html>"""
    return html
