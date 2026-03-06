import streamlit as st

st.set_page_config(page_title="Movie Recommender (ETL)", layout="wide")

st.title("🎬 Movie Recommender with ETL Pipeline")
st.write("""
This project follows:
- Extract (API / upload CSV)
- Transform (generic cleaning + mapping)
- Load (processed dataset)
- Recommend (TF-IDF + cosine similarity)
""")

st.info("Go to **ETL_Run** page first to transform your CSV, then open **Recommender** page.")