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

# ── Page header ───────────────────────────────────────────────────────────────
st.title("ETL Pipeline")
st.markdown(
    "Extract → Transform → Load your raw movie data into a clean, "
    "analysis-ready dataset. Choose a source below to get started."
)
st.divider()

# ── Pipeline steps indicator ──────────────────────────────────────────────────
def _step(number, label, active=False, done=False):
    if done:
        color = "#22c55e"
        bg    = "#052e16"
    elif active:
        color = "#38bdf8"
        bg    = "#0c1a2e"
    else:
        color = "#64748b"
        bg    = "#1e293b"
    return (
        f'<div style="flex:1;text-align:center;padding:10px 4px;border-radius:8px;'
        f'background:{bg};border:1px solid {color}">'
        f'<span style="font-size:1.4rem">{number}</span><br>'
        f'<span style="color:{color};font-weight:600;font-size:.82rem">{label}</span>'
        f'</div>'
    )

raw_loaded  = "df_raw"   in st.session_state
transformed = "df_clean" in st.session_state

s1 = _step("📂", "Extract",   active=not raw_loaded,                 done=raw_loaded)
s2 = _step("🔄", "Transform", active=raw_loaded and not transformed, done=transformed)
s3 = _step("💾", "Load",      active=transformed,                    done=transformed)
s4 = _step("🔍", "Explore",   done=False)

st.markdown(
    f'<div style="display:flex;gap:8px;margin-bottom:1rem">{s1}{s2}{s3}{s4}</div>',
    unsafe_allow_html=True,
)
st.divider()

# ── Step 1: Extract ───────────────────────────────────────────────────────────
st.subheader("Step 1 — Extract")
source = st.radio(
    "Choose data source",
    ["Select from raw folder", "Upload a CSV file"],
    horizontal=True,
    label_visibility="collapsed",
)

df_raw = None

if source == "Select from raw folder":
    raw_files = sorted(RAW_DIR.glob("*.csv"))
    if not raw_files:
        st.warning("No CSV files found in `data/raw/`. Add a file and reload the page.")
    else:
        col_sel, col_btn = st.columns([3, 1])
        with col_sel:
            selected = st.selectbox(
                "Select a dataset",
                raw_files,
                format_func=lambda p: p.name,
                label_visibility="collapsed",
            )
        with col_btn:
            load_clicked = st.button("Load", use_container_width=True, type="primary")
        if load_clicked:
            with st.spinner("Reading file…"):
                df_raw = extract_csv(str(selected))
            st.session_state["df_raw"]      = df_raw
            st.session_state["df_raw_name"] = selected.stem
            st.session_state.pop("df_clean", None)
            st.session_state.pop("df_clean_stem", None)
            st.session_state.pop("df_clean_path", None)
            st.rerun()
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
        st.session_state["df_raw"]      = df_raw
        st.session_state["df_raw_name"] = Path(uploaded.name).stem
        st.session_state.pop("df_clean", None)
    if "df_raw" in st.session_state:
        df_raw = st.session_state["df_raw"]

# ── Raw preview ───────────────────────────────────────────────────────────────
if df_raw is not None:
    raw_name = st.session_state.get("df_raw_name", "dataset")
    st.success(f"Loaded **{raw_name}** — {len(df_raw):,} rows × {df_raw.shape[1]} columns")

    m1, m2, m3 = st.columns(3)
    m1.metric("Rows",          f"{len(df_raw):,}")
    m2.metric("Columns",       df_raw.shape[1])
    m3.metric("Missing cells", f"{df_raw.isnull().sum().sum():,}")

    with st.expander("Preview raw data (first 20 rows)", expanded=False):
        st.dataframe(df_raw.head(20), use_container_width=True)

    st.divider()

    # ── Step 2: Transform ─────────────────────────────────────────────────────
    st.subheader("Step 2 — Transform")
    st.markdown(
        "Applies column standardisation, type casting, deduplication, "
        "and rating/vote consolidation."
    )

    if st.button("Run Transform", type="primary"):
        with st.spinner("Transforming data…"):
            try:
                df_clean = transform_movies(df_raw)
                stem     = st.session_state.get("df_raw_name", "movies")
                out_path = PROCESSED_DIR / f"{stem}_transformed.csv"
                load_csv(df_clean, str(out_path))
                st.session_state["df_clean"]      = df_clean
                st.session_state["df_clean_stem"] = stem
                st.session_state["df_clean_path"] = str(out_path)
            except Exception as e:
                st.error(f"Transform failed: {e}")
                st.exception(e)
        st.rerun()

# ── Step 3: Load result ───────────────────────────────────────────────────────
if "df_clean" in st.session_state:
    df_clean = st.session_state["df_clean"]
    stem     = st.session_state.get("df_clean_stem", "movies")
    out_path = st.session_state.get("df_clean_path", "")

    st.divider()
    st.subheader("Step 3 — Load")
    st.success(f"Saved to `{Path(out_path).name}`")

    raw_rows   = len(df_raw) if df_raw is not None else None
    clean_rows = len(df_clean)
    dropped    = (raw_rows - clean_rows) if raw_rows is not None else None

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Input rows",     f"{raw_rows:,}"   if raw_rows  is not None else "–")
    c2.metric("Output rows",    f"{clean_rows:,}")
    c3.metric("Rows removed",   f"{dropped:,}"    if dropped   is not None else "–")
    c4.metric("Output columns", df_clean.shape[1])

    if df_raw is not None:
        raw_cols   = set(df_raw.columns)
        clean_cols = set(df_clean.columns)
        added      = clean_cols - raw_cols
        removed    = raw_cols   - clean_cols
        if added or removed:
            with st.expander("Column changes"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Added columns**")
                    for c in sorted(added):
                        st.markdown(f"- `{c}`")
                with col_b:
                    st.markdown("**Removed / renamed columns**")
                    for c in sorted(removed):
                        st.markdown(f"- `{c}`")

    with st.expander("Preview transformed data (first 20 rows)", expanded=True):
        st.dataframe(df_clean.head(20), use_container_width=True)

    st.download_button(
        label="Download Transformed CSV",
        data=df_clean.to_csv(index=False).encode("utf-8"),
        file_name=f"{stem}_transformed.csv",
        mime="text/csv",
    )

    st.divider()

    # ── Step 4: Explore ───────────────────────────────────────────────────────
    st.subheader("Step 4 — Explore")
    st.markdown("Your dataset is ready. Head to one of the analysis pages in the sidebar:")
    st.markdown("""
    <style>
    [data-testid="stPageLink"] a {
        display: block;
        padding: 12px 20px;
        border: 1px solid #38bdf8;
        border-radius: 8px;
        background: #0c1a2e;
        color: #38bdf8 !important;
        font-weight: 600;
        text-align: center;
        text-decoration: none;
    }
    [data-testid="stPageLink"] a:hover {
        background: #1e3a5f;
        border-color: #7dd3fc;
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.page_link("pages/4_EDA.py",          label="EDA")
    col2.page_link("pages/5_Visualization.py", label="Visualization")
    col3.page_link("pages/2_Recommender.py",   label="Recommender")