import streamlit as st

st.set_page_config(page_title="Movie Recommender (ETL)", layout="wide", page_icon="🎬")

# Header
st.title("🎬 Movie Recommender System")
st.markdown("Intelligent movie recommendations powered by ETL pipeline and machine learning")
st.markdown("---")

# Welcome message
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Welcome!")
    st.markdown("""
    Discover your next favorite movie with this intelligent recommendation system. 
    The application combines powerful ETL pipelines with machine learning to provide 
    personalized movie recommendations based on content similarity.
    """)
    
    st.subheader("Quick Start Guide")
    st.markdown("""
    **Step 1:** Navigate to **ETL Run** page to process your movie dataset
    
    **Step 2:** Visit the **Recommender** page to get personalized suggestions
    
    **Step 3:** Explore **EDA** and **Visualization** for insights
    """)

with col2:
    st.info("**Features**\n\n- Smart Recommendations\n- ETL Pipeline\n- Data Analytics\n- Interactive Visualizations\n- Automated Reports")

# ETL Pipeline Overview
st.markdown("---")
st.header("ETL Pipeline Architecture")

st.markdown("""
The system follows a complete Extract, Transform, Load (ETL) workflow with an integrated 
recommendation engine.
""")

col_e, col_t, col_l, col_r = st.columns(4)

with col_e:
    st.warning("""
    **📥 Extract**
    
    Upload CSV files or connect to APIs to ingest movie data
    """)

with col_t:
    st.warning("""
    **⚙️ Transform**
    
    Clean and map data fields for consistency
    """)

with col_l:
    st.warning("""
    **💾 Load**
    
    Store processed datasets for quick access
    """)

with col_r:
    st.warning("""
    **🎯 Recommend**
    
    TF-IDF + Cosine Similarity engine
    """)

# Technology Stack
st.markdown("---")
st.header("Technology Stack")

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
    **Python**  
    Core programming language for data processing and ML
    """)
    
with tech_col2:
    st.markdown("""
    **Machine Learning**  
    TF-IDF vectorization & cosine similarity for recommendations
    """)
    
with tech_col3:
    st.markdown("""
    **Streamlit**  
    Interactive web interface and visualizations
    """)

# Footer
st.markdown("---")
st.success("💡 **Ready to get started?** Head to the ETL Run page to process your dataset, then check out the Recommender for personalized movie suggestions!")
st.caption("Built with Python and Streamlit | 2026")
