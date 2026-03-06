import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
from src.etl.transform import transform_movies
from src.etl.load import load_csv

st.title("🧪 Run ETL on Any Movie CSV")

uploaded = st.file_uploader("Upload a movie CSV file", type=["csv"])

if uploaded:
    df_raw = pd.read_csv(uploaded)

    df_raw.columns = (
        df_raw.columns.astype(str)
        .str.strip().str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    st.subheader("Preview: Raw Data")
    st.dataframe(df_raw.head(25), use_container_width=True)

    if st.button("Run Transform (Generic Cleaning)"):
        df_clean = transform_movies(df_raw)

        out_path = "data/processed/movies_transformed.csv"
        load_csv(df_clean, out_path)

        st.success(f"Saved transformed dataset to: {out_path}")

        st.subheader("Preview: Transformed Data")
        st.dataframe(df_clean.head(25), use_container_width=True)

        st.download_button(
            "Download Transformed CSV",
            data=df_clean.to_csv(index=False).encode("utf-8"),
            file_name="movies_transformed.csv",
            mime="text/csv"
        )