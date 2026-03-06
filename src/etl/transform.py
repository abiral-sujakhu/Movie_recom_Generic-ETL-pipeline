import pandas as pd
import numpy as np
import re

COLUMN_ALIASES = {
    "title": ["title", "movie_title", "name", "original_title"],
    "release_date": ["release_date", "released", "date", "premiere"],
    "genres": ["genres", "genre", "genre_names", "genres_tmdb", "genres_omdb"],
    "overview": ["overview", "plot", "description", "summary", "synopsis", "plot_omdb", "overview_tmdb"],
    "runtime": ["runtime", "duration", "runtime_minutes"],
    "imdb_id": ["imdb_id", "imdbid"],
    "tmdb_id": ["tmdb_id", "id"],
    "imdb_rating": ["imdb_rating", "imdbrating"],
    "imdb_votes": ["imdb_votes", "imdbvotes", "votes"],
    "tmdb_rating": ["tmdb_rating", "vote_average", "rating"],
    "tmdb_vote_count": ["tmdb_vote_count", "vote_count"],
    "popularity": ["popularity"],
    "director": ["director", "directors"],
    "cast": ["cast", "top_cast", "actors"],
    "language": ["language", "original_language"],
    "country": ["country", "production_countries"],
    "poster_url": ["poster_url", "poster", "posterpath", "poster_path"]
}

CANONICAL = [
    "title","year","release_date","genres","overview","runtime",
    "imdb_id","tmdb_id","imdb_rating","imdb_votes","tmdb_rating","tmdb_vote_count",
    "popularity","director","cast","language","country","poster_url"
]

def _clean_text(x):
    if pd.isna(x):
        return np.nan
    x = re.sub(r"\s+", " ", str(x)).strip()
    return x if x else np.nan

def _normalize_genres(val):
    if pd.isna(val):
        return np.nan
    s = str(val)
    if "|" in s:
        items = s.split("|")
    elif "," in s:
        items = s.split(",")
    else:
        items = [s]
    items = [(_clean_text(x) or "").title() for x in items if _clean_text(x)]
    items = sorted(set([i for i in items if i]))
    return ", ".join(items) if items else np.nan

def _clean_votes(v):
    if pd.isna(v):
        return np.nan
    return pd.to_numeric(str(v).replace(",", "").strip(), errors="coerce")

def _clean_runtime(v):
    if pd.isna(v):
        return np.nan
    m = re.search(r"(\d+)", str(v))
    return pd.to_numeric(m.group(1), errors="coerce") if m else np.nan

def _parse_year(row):
    for col in ["year","release_year"]:
        if col in row and pd.notna(row[col]):
            y = pd.to_numeric(row[col], errors="coerce")
            if pd.notna(y) and 1800 <= y <= 2100:
                return int(y)

    for col in ["release_date","released","date"]:
        if col in row and pd.notna(row[col]):
            m = re.search(r"(\d{4})", str(row[col]))
            if m:
                y = int(m.group(1))
                if 1800 <= y <= 2100:
                    return y

    if "title" in row and pd.notna(row["title"]):
        m = re.search(r"\((\d{4})\)", str(row["title"]))
        if m:
            y = int(m.group(1))
            if 1800 <= y <= 2100:
                return y
    return np.nan

def apply_aliases(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()
    for canonical, aliases in COLUMN_ALIASES.items():
        if canonical in df2.columns:
            continue
        for a in aliases:
            if a in df2.columns:
                df2[canonical] = df2[a]
                break
    return df2

def transform_movies(df: pd.DataFrame) -> pd.DataFrame:
    df = apply_aliases(df).copy()

    for col in ["title","overview","director","cast","language","country","poster_url","imdb_id"]:
        if col in df.columns:
            df[col] = df[col].apply(_clean_text)

    if "genres" in df.columns:
        df["genres"] = df["genres"].apply(_normalize_genres)

    if "runtime" in df.columns:
        df["runtime"] = df["runtime"].apply(_clean_runtime)

    for col in ["imdb_rating","tmdb_rating","popularity","tmdb_vote_count"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "imdb_votes" in df.columns:
        df["imdb_votes"] = df["imdb_votes"].apply(_clean_votes)

    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    df["year"] = df.apply(_parse_year, axis=1)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    if "title" in df.columns:
        df["title"] = df["title"].astype(str).str.replace(r"\(\d{4}\)", "", regex=True).str.strip()
        df["title"] = df["title"].replace({"nan": np.nan})

    keep = [c for c in CANONICAL if c in df.columns]
    out = df[keep].copy()

    if "imdb_id" in out.columns and out["imdb_id"].notna().any():
        out = out.drop_duplicates(subset=["imdb_id"])
    elif "title" in out.columns and "year" in out.columns:
        out = out.drop_duplicates(subset=["title","year"])
    elif "title" in out.columns:
        out = out.drop_duplicates(subset=["title"])

    return out.reset_index(drop=True)