import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
from src.utils.eda import run_visualizations

PROCESSED_DIR = ROOT / "data" / "processed"

st.title("📊 Visualization")

# ── Dataset selector ──────────────────────────────────────────────────────────
csv_files = sorted(PROCESSED_DIR.glob("*.csv"))
if not csv_files:
    st.warning("No processed datasets found. Run **ETL** first to generate one.")
    st.stop()

selected = st.selectbox("Select a processed dataset", csv_files, format_func=lambda p: p.name)

if st.button("Generate Visualizations"):
    with st.spinner("Generating charts..."):
        try:
            df = pd.read_csv(selected)
            figures = run_visualizations(df)
            st.session_state["viz_figures"] = figures
            st.session_state["viz_stem"]    = selected.stem
        except Exception as e:
            st.error(f"Visualization failed: {e}")
            st.exception(e)

# ── Display charts ────────────────────────────────────────────────────────────
if "viz_figures" in st.session_state:
    figures = st.session_state["viz_figures"]
    stem    = st.session_state.get("viz_stem", "")

    if not figures:
        st.info("No charts — dataset may have no numeric or categorical columns.")
    else:
        st.subheader(f"Charts for: {stem}")

        heatmap_figs = [(t, f) for t, f in figures if t == "Correlation Heatmap"]
        hist_figs    = [(t, f) for t, f in figures if "Distribution" in t]
        bar_figs     = [(t, f) for t, f in figures if t.startswith("Top 10:")]

        for title, fig in heatmap_figs:
            st.markdown("### Correlation Heatmap")
            st.pyplot(fig)

        if hist_figs:
            st.markdown("### Distributions")
            cols = st.columns(3)
            for i, (title, fig) in enumerate(hist_figs):
                cols[i % 3].pyplot(fig)

        if bar_figs:
            st.markdown("### Top-10 Categories")
            for title, fig in bar_figs:
                st.pyplot(fig)
