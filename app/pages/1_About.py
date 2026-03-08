import streamlit as st

st.set_page_config(page_title="About", layout="wide", page_icon="ℹ️")

# Header
st.title("About This Project")
st.markdown("A content-based movie recommendation system with full ETL pipeline")
st.markdown("---")

# Introduction
st.header("Overview")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    This is a movie recommendation system I built to explore the intersection of data engineering 
    and machine learning. The project implements a complete ETL pipeline that processes movie datasets 
    and uses content-based filtering to generate recommendations.

    What started as a learning exercise in data processing evolved into a full-featured application 
    with visualization capabilities, exploratory data analysis, and automated reporting. The system 
    uses TF-IDF vectorization and cosine similarity to find movies with similar characteristics based 
    on their metadata.
    """)

with col2:
    st.info("**Quick Facts**\n\n- Built with Python\n- ETL + ML Pipeline\n- Content-based filtering\n- Interactive visualizations\n- Automated scheduling")

st.header("What It Does")

st.markdown("""
The application handles the entire workflow from raw data to actionable insights:
""")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.warning("""
    **Data Processing**
    
    Upload CSV files containing movie information, which then goes through 
    cleaning, transformation, and standardization. The ETL pipeline is designed to be flexible 
    enough to handle different data sources and formats.
    """)

with col_b:
    st.warning("""
    **Recommendations**
    
    Once data is processed, the system analyzes movie features (genres, 
    descriptions, cast, etc.) and builds a similarity matrix. When you select a movie, it finds 
    others with comparable characteristics.
    """)

with col_c:
    st.warning("""
    **Analysis & Visualization**
    
    Beyond recommendations, the app includes tools for exploring 
    the dataset - correlation matrices, distribution plots, and statistical summaries help 
    understand patterns in the data.
    """)

st.markdown("---")

# Technical Stack
st.header("Technical Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Core Libraries**")
    st.markdown("""
    - **Pandas** for data manipulation
    - **NumPy** for numerical operations
    - **Scikit-learn** for ML algorithms
    - **NLTK** for text processing
    """)
    
    st.markdown("**Development**")
    st.markdown("""
    - **Python 3.x** as the base language
    - **Streamlit** for the web interface
    - Automated scheduling for periodic ETL runs
    """)

with col2:
    st.markdown("**Visualization**")
    st.markdown("""
    - **Plotly** for interactive charts
    - **Matplotlib** & **Seaborn** for statistical plots
    - **Altair** for declarative visualizations
    """)
    
    st.markdown("**Architecture**")
    st.markdown("""
    - Modular design with separated concerns
    - Reusable components across modules
    - Configuration-based approach
    """)

st.markdown("---")

# How It Works
st.header("How It Works")

st.markdown("""
The system follows a standard ETL (Extract, Transform, Load) pattern with an added 
recommendation layer. Each phase is designed to be modular and testable.
""")

with st.expander("Extract Phase"):
    st.markdown("""
    The data ingestion step supports CSV file uploads. The system reads the raw data and 
    performs initial validation to ensure required fields are present. Currently tested with 
    IMDB datasets, but designed to accommodate other movie data sources with minimal 
    configuration changes.
    """)

with st.expander("Transform Phase"):
    st.markdown("""
    This is where most of the data quality work happens. The transformation includes:
    - Handling missing values through imputation or removal
    - Standardizing text fields (lowercasing, removing special characters)
    - Parsing complex fields like genres and cast information
    - Creating derived features that improve recommendation quality
    - Mapping columns to a consistent schema
    """)

with st.expander("Load Phase"):
    st.markdown("""
    Processed data is stored in a structured format for quick retrieval. The system maintains 
    the transformed dataset and metadata about the transformation process. This makes it easy 
    to track what changes were applied and when.
    """)

with st.expander("Recommendation Phase"):
    st.markdown("""
    The recommendation engine uses content-based filtering:
    - Combines relevant text features (genre, description, director, cast) into a single text field
    - Applies TF-IDF vectorization to convert text into numerical representations
    - Calculates cosine similarity between all movies
    - Returns the most similar movies when given a query
    
    This approach works well when you have rich metadata but don't have user interaction data 
    for collaborative filtering.
    """)

st.markdown("---")

# Project Structure
st.header("Project Structure")

st.markdown("""
The codebase is organized into distinct modules, each with a specific responsibility:
""")

struct_col1, struct_col2 = st.columns(2)

with struct_col1:
    st.markdown("""
    - **ETL Module** (`src/etl/`)  
      Contains extract, transform, and load logic
    
    - **Recommender Module** (`src/recommender/`)  
      Implements the recommendation algorithm
    
    - **Utils** (`src/utils/`)  
      Helper functions for EDA, reporting, and configuration
    """)

with struct_col2:
    st.markdown("""
    - **Scheduler** (`src/scheduler/`)  
      Handles automated task execution
    
    - **App** (`app/`)  
      Streamlit pages and UI components
    
    - **Data** (`data/`)  
      Raw and processed datasets
    """)

st.info("Each module is self-contained and can be tested independently. This structure makes it easier to extend functionality or swap out components without affecting the rest of the system.")

st.markdown("---")

# Limitations & Future Work
st.header("Current Limitations")

st.markdown("""
Like any project, this has areas that could be improved. Being honest about limitations 
is important for understanding where the system fits in the spectrum of recommendation engines.
""")

limit_col1, limit_col2 = st.columns(2)

with limit_col1:
    st.warning("""
    **Algorithm Constraints**
    - Recommendations are purely content-based and don't learn from user preferences over time
    - The system doesn't handle collaborative filtering or hybrid approaches
    """)

with limit_col2:
    st.warning("""
    **Performance & Scale**
    - Optimized for thousands of movies, not millions
    - Text preprocessing is basic and could benefit from more sophisticated NLP techniques
    """)

st.markdown("""
These limitations are acknowledged trade-offs. The current implementation focuses on 
demonstrating core concepts rather than production-scale optimization.
""")

st.markdown("---")

# Footer
st.header("Final Notes")

st.markdown("""
This project was built as a practical exercise in combining data engineering principles 
with machine learning. The goal was to create something functional that demonstrates the 
full pipeline from data ingestion to user-facing recommendations.

The code is structured to be readable and maintainable. Comments and docstrings explain 
the reasoning behind implementation choices. Feel free to explore the codebase and adapt 
it for your own use cases.
""")

st.markdown("---")
st.caption("Built using Python and Streamlit | 2026")
