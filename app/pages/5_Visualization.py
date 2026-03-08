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

# Clear cache if it holds the old 2-tuple format
if "viz_figures" in st.session_state:
    sample = st.session_state["viz_figures"]
    if sample and len(sample[0]) == 2:
        del st.session_state["viz_figures"]

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
        st.stop()

    st.subheader(f"Charts for: {stem}")

    SECTIONS = [
        ("ratings",      "⭐ Ratings"),
        ("trends",       "📅 Trends Over Time"),
        ("genres",       "🎬 Genres"),
        ("people",       "🎥 Directors, Languages & Countries"),
        ("technical",    "⏱ Technical"),
        ("correlations", "🔗 Correlations"),
    ]

    for category, heading in SECTIONS:
        section_figs = [(t, f) for cat, t, f in figures if cat == category]
        if not section_figs:
            continue

        st.markdown(f"### {heading}")

        if category == "correlations" or len(section_figs) == 1:
            for title, fig in section_figs:
                st.pyplot(fig)
        else:
            cols = st.columns(2)
            for i, (title, fig) in enumerate(section_figs):
                cols[i % 2].pyplot(fig)
