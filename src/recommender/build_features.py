import pandas as pd
import re

def _clean(x):
    if pd.isna(x):
        return ""
    x = str(x).lower()
    x = re.sub(r"\s+", " ", x).strip()
    return x

def build_feature_text(df: pd.DataFrame) -> pd.Series:
    parts = []

    for col in ["overview","overview_tmdb","plot_omdb","plot","summary","synopsis"]:
        if col in df.columns:
            parts.append(df[col].fillna("").astype(str))
            break

    for col in ["genres","director","cast","title","year"]:
        if col in df.columns:
            parts.append(df[col].fillna("").astype(str))

    if not parts:
        return pd.Series([""] * len(df), index=df.index)

    joined = parts[0]
    for p in parts[1:]:
        joined = joined + " " + p

    return joined.apply(_clean)