import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
from pathlib import Path
from src.recommender.build_features import build_feature_text
from src.recommender.recommend import MovieRecommender

st.title("🍿 Movie Recommender")

PROCESSED_DIR = ROOT / "data" / "processed"

csv_files = sorted(PROCESSED_DIR.glob("*.csv"))
if not csv_files:
    st.warning("No processed datasets found. Run **ETL** first to generate one.")
    st.stop()

selected_csv = st.selectbox("Select a dataset", csv_files, format_func=lambda p: p.name)

@st.cache_resource
def load_model(path: str, _mtime: float):
    df = pd.read_csv(path)
    df["feature_text"] = build_feature_text(df)
    return MovieRecommender(df, feature_col="feature_text"), df

try:
    mtime = selected_csv.stat().st_mtime
    model, df = load_model(str(selected_csv), mtime)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

movie_list = df["title"].dropna().astype(str).sort_values().unique().tolist()
selected = st.selectbox("Choose a movie", movie_list)

top_n = st.slider("How many recommendations?", 5, 20, 10)

if st.button("Recommend"):
    recs = model.recommend(selected, top_n=top_n)

    st.subheader("Recommended Movies")
    st.dataframe(recs, use_container_width=True)

    if "poster_url" in df.columns:
        st.subheader("Posters")
        cols = st.columns(5)

        for i, row in recs.head(10).iterrows():
            with cols[i % 5]:
                st.write(row["title"])
                url = row.get("poster_url")
                if isinstance(url, str) and url.startswith("http"):
                    st.image(url, use_container_width=True)