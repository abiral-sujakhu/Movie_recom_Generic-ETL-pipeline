import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import streamlit as st
import pandas as pd
from datetime import datetime
from src.utils.report import generate_html_report

PROCESSED_DIR = ROOT / "data" / "processed"
REPORTS_DIR   = ROOT / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

st.title("📑 Reports")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Generate a new report
# ═══════════════════════════════════════════════════════════════════════════════
st.header("Generate Report")

csv_files = sorted(PROCESSED_DIR.glob("*.csv"))
if not csv_files:
    st.warning("No processed datasets found. Run **ETL** first.")
else:
    selected_csv = st.selectbox("Select a dataset", csv_files, format_func=lambda p: p.name)

    if st.button("Generate Report"):
        with st.spinner("Building report..."):
            try:
                df = pd.read_csv(selected_csv)
                html = generate_html_report(df, selected_csv.stem)
                ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
                out_path = REPORTS_DIR / f"{selected_csv.stem}_report_{ts}.html"
                out_path.write_text(html, encoding="utf-8")
                st.session_state["new_report_html"] = html
                st.session_state["new_report_name"] = out_path.name
                st.success(f"Report saved: {out_path.name}")
            except Exception as e:
                st.error(f"Failed: {e}")
                st.exception(e)

    # Show newly generated report
    if "new_report_html" in st.session_state:
        html  = st.session_state["new_report_html"]
        fname = st.session_state["new_report_name"]
        st.download_button("⬇ Download HTML Report", data=html.encode("utf-8"),
                           file_name=fname, mime="text/html")
        st.components.v1.html(html, height=900, scrolling=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Browse existing reports
# ═══════════════════════════════════════════════════════════════════════════════
st.header("Existing Reports")

all_reports = sorted(REPORTS_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)
if not all_reports:
    st.info("No reports yet. Generate one above.")
else:
    # Group by stem so HTML / PDF / Excel stay together
    stems: dict = {}
    for f in all_reports:
        stems.setdefault(f.stem, []).append(f)

    st.caption(f"{len(stems)} report(s) found")

    for i, (stem, files) in enumerate(stems.items()):
        with st.expander(stem, expanded=(i == 0)):
            btn_cols = st.columns(len(files))
            for col, f in zip(btn_cols, sorted(files, key=lambda p: p.suffix)):
                label = {".html": "⬇ HTML", ".pdf": "⬇ PDF",
                         ".xlsx": "⬇ Excel"}.get(f.suffix, f"⬇ {f.suffix}")
                mime  = {".html": "text/html", ".pdf": "application/pdf",
                         ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                         }.get(f.suffix, "application/octet-stream")
                col.download_button(label, data=f.read_bytes(),
                                    file_name=f.name, mime=mime,
                                    key=f"dl_{f.name}")

            html_file = next((f for f in files if f.suffix == ".html"), None)
            if html_file:
                st.components.v1.html(html_file.read_text(encoding="utf-8"),
                                      height=800, scrolling=True)

