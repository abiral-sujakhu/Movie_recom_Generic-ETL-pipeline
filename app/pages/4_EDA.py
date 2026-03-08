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
if "eda_result" in st.session_state and not isinstance(st.session_state["eda_result"], dict):
    del st.session_state["eda_result"]

if "eda_result" in st.session_state:
    result = st.session_state["eda_result"]
    stem   = st.session_state.get("eda_stem", "")

    st.subheader(f"Dataset: {stem}")

    # Summary statistics
    if result["summary"] is not None:
        st.markdown("### Summary Statistics")
        st.dataframe(result["summary"], use_container_width=True)

    # Missing values
    if result["missing"] is not None and not result["missing"].empty:
        st.markdown("### Missing Values")
        st.dataframe(result["missing"].rename("missing_count").to_frame(), use_container_width=True)
    else:
        st.success("No missing values.")

    # Skewness & Kurtosis side by side
    if result["skewness"] is not None or result["kurtosis"] is not None:
        col1, col2 = st.columns(2)
        if result["skewness"] is not None:
            with col1:
                st.markdown("### Skewness")
                st.dataframe(result["skewness"].rename("skewness").to_frame(), use_container_width=True)
        if result["kurtosis"] is not None:
            with col2:
                st.markdown("### Kurtosis")
                st.dataframe(result["kurtosis"].rename("kurtosis").to_frame(), use_container_width=True)

    # Correlation matrix
    if result["correlation"] is not None:
        st.markdown("### Correlation Matrix")
        st.dataframe(result["correlation"].style.background_gradient(cmap="coolwarm", axis=None),
                     use_container_width=True)

    # Covariance matrix
    if result["covariance"] is not None:
        with st.expander("Covariance Matrix"):
            st.dataframe(result["covariance"], use_container_width=True)
