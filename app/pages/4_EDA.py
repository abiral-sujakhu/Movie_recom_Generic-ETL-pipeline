import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
from src.utils.eda import run_eda

PROCESSED_DIR = ROOT / "data" / "processed"

st.markdown("""
<style>
/* ── Section cards ── */
.eda-card {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 1.2rem 1.4rem 1rem 1.4rem;
    margin: 1rem 0 .5rem 0;
}
.eda-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: .8rem;
}
.eda-badge {
    background: #1e3a5f;
    color: #38bdf8;
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: .08em;
    padding: 2px 8px;
    border-radius: 4px;
}
.eda-card-title {
    font-size: 1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0;
}
/* ── Page hero ── */
.eda-hero {
    background: linear-gradient(135deg, #0c1a2e 0%, #0f172a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
}
.eda-hero h2 {
    margin: 0 0 .3rem 0;
    font-size: 1.6rem;
    color: #f1f5f9;
}
.eda-hero p {
    margin: 0;
    color: #94a3b8;
    font-size: .9rem;
}
/* ── Dataset tag ── */
.ds-tag {
    display: inline-block;
    background: #1e293b;
    color: #38bdf8;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 3px 10px;
    font-size: .82rem;
    font-family: monospace;
    margin-bottom: .8rem;
}
</style>
""", unsafe_allow_html=True)


def card(num: str, title: str):
    st.markdown(
        f'<div class="eda-card-header">'
        f'<span class="eda-badge">{num}</span>'
        f'<span class="eda-card-title">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ── Hero header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="eda-hero">
  <h2>Exploratory Data Analysis</h2>
  <p>Select a processed dataset and run a full statistical profile — overview, missing values,
  duplicates, distributions, correlations, and more.</p>
</div>
""", unsafe_allow_html=True)

# ── Dataset selector ──────────────────────────────────────────────────────────
csv_files = sorted(PROCESSED_DIR.glob("*.csv"))
if not csv_files:
    st.warning("No processed datasets found. Run **ETL** first to generate one.")
    st.stop()

col_sel, col_btn = st.columns([4, 1])
with col_sel:
    selected = st.selectbox("Dataset", csv_files, format_func=lambda p: p.name,
                            label_visibility="collapsed")
with col_btn:
    run_clicked = st.button("Run EDA", type="primary", use_container_width=True)

if run_clicked:
    with st.spinner("Analysing dataset…"):
        try:
            df = pd.read_csv(selected)
            result = run_eda(df)
            st.session_state["eda_result"] = result
            st.session_state["eda_stem"]   = selected.stem
        except Exception as e:
            st.error(f"EDA failed: {e}")
            st.exception(e)

# ── Stale result guard ────────────────────────────────────────────────────────
if "eda_result" in st.session_state:
    _r = st.session_state["eda_result"]
    if not isinstance(_r, dict) or "overview" not in _r:
        del st.session_state["eda_result"]

if "eda_result" not in st.session_state:
    st.stop()

result = st.session_state["eda_result"]
stem   = st.session_state.get("eda_stem", "")

st.markdown(f'<div class="ds-tag">{stem}</div>', unsafe_allow_html=True)
st.divider()

# ── 1. Dataset Overview ───────────────────────────────────────────────────────
with st.container():
    card("01", "Dataset Overview")
    ov = result.get("overview")
    if ov:
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows",    f"{ov['rows']:,}")
        c2.metric("Columns", ov["columns"])
        c3.metric("Memory",  f"{ov['memory_usage_mb']} MB")
        with st.expander("Column names & dtypes"):
            dtype_df = pd.DataFrame.from_dict(ov["dtypes"], orient="index", columns=["dtype"])
            st.dataframe(dtype_df, use_container_width=True)

st.divider()

# ── 2. Missing Value Analysis ─────────────────────────────────────────────────
with st.container():
    card("02", "Missing Value Analysis")
    miss = result.get("missing")
    if miss is not None and not miss.empty:
        st.dataframe(miss, use_container_width=True)
    else:
        st.success("No missing values detected.")

st.divider()

# ── 3. Duplicate Detection ────────────────────────────────────────────────────
with st.container():
    card("03", "Duplicate Detection")
    dup = result.get("duplicates")
    if dup:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows",     f"{dup['total_rows']:,}")
        c2.metric("Duplicate Rows", dup["duplicate_rows"])
        c3.metric("Duplicate %",    f"{dup['duplicate_pct']}%")
        if dup["duplicate_rows"] == 0:
            st.success("No duplicate rows found.")
        else:
            st.warning(f"{dup['duplicate_rows']} duplicate row(s) detected.")

st.divider()

# ── 4. Descriptive Statistics ─────────────────────────────────────────────────
with st.container():
    card("04", "Descriptive Statistics")
    if result["summary"] is not None:
        numeric_summary = result["summary"].loc[
            :, result["summary"].loc["mean"].notna()
        ]
        st.dataframe(numeric_summary, use_container_width=True)

st.divider()

# ── 5. Unique Value Analysis ──────────────────────────────────────────────────
with st.container():
    card("05", "Unique Value Analysis")
    uv = result.get("unique_values")
    if uv is not None:
        st.dataframe(uv, use_container_width=True)

st.divider()

# ── 6. Genre Frequency Analysis ───────────────────────────────────────────────
with st.container():
    card("06", "Genre Frequency Analysis")
    gf = result.get("genre_frequency")
    if gf is not None and not gf.empty:
        st.dataframe(
            gf.rename("count").reset_index().rename(columns={"index": "genre"}),
            use_container_width=True,
        )
    else:
        st.info("No 'genres' column found in this dataset.")

st.divider()

# ── 7. Release Year Statistics ────────────────────────────────────────────────
with st.container():
    card("07", "Release Year Statistics")
    ys = result.get("year_stats")
    if ys:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Earliest",    ys["min_year"])
        c2.metric("Latest",      ys["max_year"])
        c3.metric("Median",      ys["median_year"])
        c4.metric("Most Common", ys["most_common_year"])
        with st.expander("Movies count per year"):
            st.dataframe(
                ys["counts_per_year"].rename("count").reset_index().rename(columns={"index": "year"}),
                use_container_width=True,
            )
    else:
        st.info("No 'year' column found in this dataset.")

st.divider()

# ── 8. Correlation Analysis ───────────────────────────────────────────────────
with st.container():
    card("08", "Correlation Analysis")
    if result["correlation"] is not None:
        st.dataframe(
            result["correlation"].style.background_gradient(cmap="coolwarm", axis=None),
            use_container_width=True,
        )
        c1, c2 = st.columns(2)
        if result["skewness"] is not None:
            with c1:
                st.markdown("**Skewness**")
                st.dataframe(result["skewness"].rename("skewness").to_frame(), use_container_width=True)
        if result["kurtosis"] is not None:
            with c2:
                st.markdown("**Kurtosis**")
                st.dataframe(result["kurtosis"].rename("kurtosis").to_frame(), use_container_width=True)
        with st.expander("Covariance Matrix"):
            if result["covariance"] is not None:
                st.dataframe(result["covariance"], use_container_width=True)
    else:
        st.info("Not enough numeric columns for correlation analysis.")

st.divider()

# ── 9. Record Inspection ──────────────────────────────────────────────────────
with st.container():
    card("09", "Record Inspection")
    sr = result.get("sample_records")
    if sr:
        tab1, tab2, tab3 = st.tabs(["First 5 rows", "Last 5 rows", "Random sample"])
        with tab1:
            st.dataframe(sr["head"], use_container_width=True)
        with tab2:
            st.dataframe(sr["tail"], use_container_width=True)
        with tab3:
            st.dataframe(sr["random_sample"], use_container_width=True)

