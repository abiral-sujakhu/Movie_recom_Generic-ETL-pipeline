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

data_path = Path("data/processed/movies_transformed.csv")
if not data_path.exists():
    st.warning("No transformed dataset found. Go to **ETL_Run** and generate it first.")
    st.stop()

df = pd.read_csv(data_path)
df["feature_text"] = build_feature_text(df)

@st.cache_resource
def load_model(df_cached: pd.DataFrame):
    return MovieRecommender(df_cached, feature_col="feature_text")

model = load_model(df)

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