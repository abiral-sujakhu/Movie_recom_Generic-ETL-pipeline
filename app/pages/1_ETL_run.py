import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
from src.etl.extract import extract_csv
from src.etl.transform import transform_movies
from src.etl.load import load_csv

RAW_DIR       = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

st.title("🧪 Run ETL on Any Movie CSV")

# ── Source selection ─────────────────────────────────────────────────────────
source = st.radio("Choose data source", ["Select from raw folder", "Upload a CSV file"], horizontal=True)

df_raw = None

if source == "Select from raw folder":
    raw_files = sorted(RAW_DIR.glob("*.csv"))
    if not raw_files:
        st.warning("No CSV files found in data/raw/")
    else:
        selected = st.selectbox("Select a dataset", raw_files, format_func=lambda p: p.name)
        if st.button("Load selected file"):
            df_raw = extract_csv(str(selected))
            st.session_state["df_raw"] = df_raw
            st.session_state["df_raw_name"] = selected.stem
    if "df_raw" in st.session_state:
        df_raw = st.session_state["df_raw"]

else:
    uploaded = st.file_uploader("Upload a movie CSV file", type=["csv"])
    if uploaded:
        df_raw = pd.read_csv(uploaded)
        df_raw.columns = (
            df_raw.columns.astype(str)
            .str.strip().str.lower()
            .str.replace(r"\s+", "_", regex=True)
        )
        st.session_state["df_raw"] = df_raw
        st.session_state["df_raw_name"] = Path(uploaded.name).stem
    if "df_raw" in st.session_state:
        df_raw = st.session_state["df_raw"]

# ── Preview & Transform ──────────────────────────────────────────────────────
if df_raw is not None:
    st.subheader("Preview: Raw Data")
    st.dataframe(df_raw.head(25), use_container_width=True)

    if st.button("Run Transform (Generic Cleaning)"):
        df_clean = transform_movies(df_raw)

        stem = st.session_state.get("df_raw_name", "movies")
        out_path = PROCESSED_DIR / f"{stem}_transformed.csv"
        load_csv(df_clean, str(out_path))

        st.session_state["df_clean"]      = df_clean
        st.session_state["df_clean_stem"] = stem
        st.session_state["df_clean_path"] = str(out_path)
        st.success(f"Saved {len(df_clean)} rows to: {out_path.name}")

# ── Transformed preview ───────────────────────────────────────────────────────
if "df_clean" in st.session_state:
    df_clean = st.session_state["df_clean"]
    stem     = st.session_state.get("df_clean_stem", "movies")

    st.subheader("Preview: Transformed Data")
    st.dataframe(df_clean.head(25), use_container_width=True)

    st.download_button(
        "Download Transformed CSV",
        data=df_clean.to_csv(index=False).encode("utf-8"),
        file_name=f"{stem}_transformed.csv",
        mime="text/csv"
    )

    st.info("👉 Go to **EDA** or **Visualization** in the sidebar to analyse this dataset.")