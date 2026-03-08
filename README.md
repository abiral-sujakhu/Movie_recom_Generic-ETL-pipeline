# 🎬 Movie Recommender System with ETL Pipeline

A content-based movie recommendation system built with Python and Streamlit, featuring a complete ETL (Extract, Transform, Load) pipeline and machine learning-powered recommendations.

## 📋 Overview

This project demonstrates the full workflow of building a recommendation system, from data processing to delivering personalized movie suggestions. It combines modern data engineering practices with machine learning algorithms to provide intelligent recommendations based on content similarity.

## ✨ Features

- **ETL Pipeline**: Complete data extraction, transformation, and loading workflow
- **Content-Based Recommendations**: TF-IDF vectorization with cosine similarity
- **Interactive Web Interface**: Built with Streamlit for easy interaction
- **Exploratory Data Analysis**: Comprehensive data insights and statistics
- **Interactive Visualizations**: Charts and plots using Plotly, Matplotlib, and Seaborn
- **Automated Reports**: Generate detailed analysis reports
- **Scheduled Tasks**: Automated ETL runs with scheduling support

## 🛠️ Technology Stack

### Core Libraries
- **Python 3.x** - Programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning algorithms
- **NLTK** - Natural language processing

### Visualization & UI
- **Streamlit** - Interactive web framework
- **Plotly** - Interactive visualizations
- **Matplotlib** - Static plotting
- **Seaborn** - Statistical visualizations
- **Altair** - Declarative visualizations

## 📁 Project Structure

```
movie-recommender/
│
├── app/
│   ├── home.py                 # Home page
│   └── pages/
│       ├── 1_About.py          # About page
│       ├── 2_ETL_run.py        # ETL execution page
│       ├── 3_Recommender.py    # Recommendation page
│       ├── 4_EDA.py            # Exploratory data analysis
│       ├── 5_Visualization.py  # Data visualizations
│       └── 6_Reports.py        # Report generation
│
├── src/
│   ├── etl/
│   │   ├── extract.py          # Data extraction logic
│   │   ├── transform.py        # Data transformation logic
│   │   └── load.py             # Data loading logic
│   │
│   ├── recommender/
│   │   ├── build_features.py   # Feature engineering
│   │   └── recommend.py        # Recommendation engine
│   │
│   ├── scheduler/
│   │   └── tasks.py            # Scheduled tasks
│   │
│   └── utils/
│       ├── eda.py              # EDA utilities
│       ├── report.py           # Report generation
│       └── env.py              # Environment configuration
│
├── data/
│   ├── raw/                    # Raw data files
│   └── processed/              # Processed data files
│
├── notebooks/
│   └── modify1.ipynb           # Jupyter notebook for experiments
│
├── requirements.txt            # Python dependencies
├── scheduler_weekly.py         # Weekly scheduler script
└── README.md                   # Project documentation
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/abiral-sujakhu/Movie_recom_system_adv_py.git
   cd movie-recommender
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app/home.py
   ```

2. **Navigate to** `http://localhost:8501` in your web browser

### Quick Start Guide

1. **ETL Run Page**: Upload or process your movie dataset
2. **Recommender Page**: Get personalized movie recommendations
3. **EDA Page**: Explore statistical insights about your data
4. **Visualization Page**: View interactive charts and plots
5. **Reports Page**: Generate detailed analysis reports

## 🔄 ETL Pipeline

The ETL pipeline consists of three main phases:

### 1. Extract
- Upload CSV files containing movie data
- Support for multiple data sources (IMDB, custom datasets)
- Automatic schema detection and validation

### 2. Transform
- Data cleaning and standardization
- Missing value handling
- Text preprocessing and normalization
- Feature engineering
- Column mapping to consistent schema

### 3. Load
- Store processed data in structured format
- Maintain data versioning
- Enable quick retrieval for recommendations

## 🎯 Recommendation Engine

The recommendation system uses **content-based filtering**:

1. **Feature Extraction**: Combines movie metadata (genre, description, cast, director)
2. **TF-IDF Vectorization**: Converts text features to numerical representations
3. **Similarity Calculation**: Computes cosine similarity between movies
4. **Recommendation Generation**: Returns top-N most similar movies

## 📊 Features in Detail

### Exploratory Data Analysis
- Statistical summaries (mean, median, std dev)
- Correlation matrices
- Covariance analysis
- Distribution analysis

### Visualizations
- Genre distribution charts
- Rating distributions
- Year-wise movie trends
- Interactive scatter plots
- Correlation heatmaps

### Automated Scheduling
- Weekly ETL runs
- Configurable schedule via `scheduler_weekly.py`
- Task automation for data updates

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Built as a practical exercise in combining data engineering principles with machine learning.

## 🙏 Acknowledgments

- IMDB for movie datasets
- Streamlit team for the amazing framework
- Scikit-learn contributors for ML tools

## 📧 Contact

For questions or feedback, please open an issue in the GitHub repository.

---

**Made with ❤️ using Python and Streamlit**
