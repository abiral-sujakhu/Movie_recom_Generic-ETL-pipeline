import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
from src.utils.eda import run_eda

PROCESSED_DIR = ROOT / "data" / "processed"

st.title("🔍 EDA")

# ── Dataset selector ──────────────────────────────────────────────────────────
csv_files = sorted(PROCESSED_DIR.glob("*.csv"))
if not csv_files:
    st.warning("No processed datasets found. Run **ETL** first to generate one.")
    st.stop()

selected = st.selectbox("Select a processed dataset", csv_files, format_func=lambda p: p.name)

if st.button("Run EDA"):
    with st.spinner("Running EDA..."):
        try:
            df = pd.read_csv(selected)
            result = run_eda(df)
            st.session_state["eda_result"] = result
            st.session_state["eda_stem"]   = selected.stem
        except Exception as e:
            st.error(f"EDA failed: {e}")
            st.exception(e)

# ── Display results ───────────────────────────────────────────────────────────
# Discard stale results that predate the current EDA schema
if "eda_result" in st.session_state:
    _r = st.session_state["eda_result"]
    if not isinstance(_r, dict) or "overview" not in _r:
        del st.session_state["eda_result"]

if "eda_result" in st.session_state:
    result = st.session_state["eda_result"]
    stem   = st.session_state.get("eda_stem", "")

    st.subheader(f"Dataset: {stem}")

    # ── 1. Dataset Overview ───────────────────────────────────────────────────
    st.markdown("### 1️⃣ Dataset Overview")
    ov = result.get("overview")
    if ov:
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows",    ov["rows"])
        col2.metric("Columns", ov["columns"])
        col3.metric("Memory",  f"{ov['memory_usage_mb']} MB")
        with st.expander("Column names & dtypes"):
            dtype_df = pd.DataFrame.from_dict(ov["dtypes"], orient="index", columns=["dtype"])
            st.dataframe(dtype_df, use_container_width=True)

    # ── 2. Missing Value Analysis ─────────────────────────────────────────────
    st.markdown("### 2️⃣ Missing Value Analysis")
    miss = result.get("missing")
    if miss is not None and not miss.empty:
        st.dataframe(miss, use_container_width=True)
    else:
        st.success("No missing values detected.")

    # ── 3. Duplicate Detection ────────────────────────────────────────────────
    st.markdown("### 3️⃣ Duplicate Detection")
    dup = result.get("duplicates")
    if dup:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows",      dup["total_rows"])
        col2.metric("Duplicate Rows",  dup["duplicate_rows"])
        col3.metric("Duplicate %",     f"{dup['duplicate_pct']}%")
        if dup["duplicate_rows"] == 0:
            st.success("No duplicate rows found.")
        else:
            st.warning(f"{dup['duplicate_rows']} duplicate row(s) detected.")

    # ── 4. Descriptive Statistics ─────────────────────────────────────────────
    st.markdown("### 4️⃣ Descriptive Statistics")
    if result["summary"] is not None:
        st.dataframe(result["summary"], use_container_width=True)

    # ── 5. Unique Value Analysis ──────────────────────────────────────────────
    st.markdown("### 5️⃣ Unique Value Analysis")
    uv = result.get("unique_values")
    if uv is not None:
        st.dataframe(uv, use_container_width=True)

    # ── 6. Genre Frequency Analysis ───────────────────────────────────────────
    st.markdown("### 6️⃣ Genre Frequency Analysis")
    gf = result.get("genre_frequency")
    if gf is not None and not gf.empty:
        st.dataframe(
            gf.rename("count").reset_index().rename(columns={"index": "genre"}),
            use_container_width=True,
        )
    else:
        st.info("No 'genres' column found in this dataset.")

    # ── 7. Release Year Statistics ────────────────────────────────────────────
    st.markdown("### 7️⃣ Release Year Statistics")
    ys = result.get("year_stats")
    if ys:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Earliest",    ys["min_year"])
        col2.metric("Latest",      ys["max_year"])
        col3.metric("Median",      ys["median_year"])
        col4.metric("Most Common", ys["most_common_year"])
        with st.expander("Movies count per year"):
            st.dataframe(
                ys["counts_per_year"].rename("count").reset_index().rename(columns={"index": "year"}),
                use_container_width=True,
            )
    else:
        st.info("No 'year' column found in this dataset.")

    # ── 8. Correlation Analysis ───────────────────────────────────────────────
    st.markdown("### 8️⃣ Correlation Analysis")
    if result["correlation"] is not None:
        st.dataframe(
            result["correlation"].style.background_gradient(cmap="coolwarm", axis=None),
            use_container_width=True,
        )
        col1, col2 = st.columns(2)
        if result["skewness"] is not None:
            with col1:
                st.markdown("**Skewness**")
                st.dataframe(result["skewness"].rename("skewness").to_frame(), use_container_width=True)
        if result["kurtosis"] is not None:
            with col2:
                st.markdown("**Kurtosis**")
                st.dataframe(result["kurtosis"].rename("kurtosis").to_frame(), use_container_width=True)
        with st.expander("Covariance Matrix"):
            if result["covariance"] is not None:
                st.dataframe(result["covariance"], use_container_width=True)
    else:
        st.info("Not enough numeric columns for correlation analysis.")

    # ── 9. Record Inspection ──────────────────────────────────────────────────
    st.markdown("### 9️⃣ Record Inspection")
    sr = result.get("sample_records")
    if sr:
        tab1, tab2, tab3 = st.tabs(["First 5 rows", "Last 5 rows", "Random sample"])
        with tab1:
            st.dataframe(sr["head"], use_container_width=True)
        with tab2:
            st.dataframe(sr["tail"], use_container_width=True)
        with tab3:
            st.dataframe(sr["random_sample"], use_container_width=True)



