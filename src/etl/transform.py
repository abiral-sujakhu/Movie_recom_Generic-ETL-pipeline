import pandas as pd
import numpy as np
import re

COLUMN_ALIASES = {
    "title": ["title", "series_title", "movie_title", "name", "original_title", "film_title", "show_title"],
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
    import pandas as pd
    import numpy as np
    import re

    # Convert list -> string
    if isinstance(x, list):
        x = ", ".join(str(i) for i in x if pd.notna(i))

    # Convert Series -> string
    elif isinstance(x, pd.Series):
        x = ", ".join(str(i) for i in x.dropna().values)

    # Convert DataFrame -> string
    elif isinstance(x, pd.DataFrame):
        x = ", ".join(str(i) for i in x.values.flatten() if pd.notna(i))

    # Now x is scalar, safe to check
    if x is None:
        return np.nan
    if isinstance(x, float) and np.isnan(x):
        return np.nan

    # Clean whitespace
    x = re.sub(r"\s+", " ", str(x)).strip()
    return x if x else np.nan



def _normalize_genres(val):
    import pandas as pd
    import numpy as np

    if pd.isna(val):
        return np.nan
    s = str(val)
    if "|" in s:
        items = s.split("|")
    elif "," in s:
        items = s.split(",")
    else:
        items = [s]

    cleaned = [_clean_text(x) for x in items]
    items = [c.title() for c in cleaned if c]
    items = sorted(set(items))
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
    # Normalize column names to lowercase + strip whitespace
    df2.columns = [c.strip().lower() for c in df2.columns]

    # Step 1: exact alias matching
    for canonical, aliases in COLUMN_ALIASES.items():
        if canonical in df2.columns:
            continue
        for a in aliases:
            if a in df2.columns:
                df2 = df2.rename(columns={a: canonical})
                break

    # Step 2: keyword-based matching for still-unmapped columns
    mapping = {}
    for col in df2.columns:
        if col in CANONICAL or col in mapping.values():
            continue
        if "imdb_id" in col or "imdbid" in col:
            mapping[col] = "imdb_id"
        elif "tmdb_id" in col or "tmdbid" in col:
            mapping[col] = "tmdb_id"
        elif "imdb" in col and ("rating" in col or "score" in col):
            mapping[col] = "imdb_rating"
        elif "imdb" in col and ("vote" in col or "count" in col):
            mapping[col] = "imdb_votes"
        elif "tmdb" in col and ("rating" in col or "score" in col or "average" in col):
            mapping[col] = "tmdb_rating"
        elif "tmdb" in col and ("vote" in col or "count" in col):
            mapping[col] = "tmdb_vote_count"
        elif "vote" in col or "count" in col:
            mapping[col] = "tmdb_vote_count"
        elif "rating" in col or "score" in col:
            mapping[col] = "imdb_rating"
        elif "poster" in col:
            mapping[col] = "poster_url"
        elif "overview" in col or "plot" in col or "synopsis" in col or "description" in col or "summary" in col:
            mapping[col] = "overview"
        elif "genre" in col or "category" in col or "type" in col:
            mapping[col] = "genres"
        elif "runtime" in col or "duration" in col:
            mapping[col] = "runtime"
        elif "director" in col:
            mapping[col] = "director"
        elif "cast" in col or "actor" in col or "star" in col:
            mapping[col] = "cast"
        elif "language" in col or "lang" in col:
            mapping[col] = "language"
        elif "country" in col or "nation" in col:
            mapping[col] = "country"
        elif "popularity" in col or "popular" in col:
            mapping[col] = "popularity"
        elif "release" in col or "date" in col or "premiere" in col:
            mapping[col] = "release_date"
        elif "year" in col:
            mapping[col] = "year"
        elif "title" in col or "name" in col or "film" in col or "movie" in col:
            mapping[col] = "title"
    df2 = df2.rename(columns=mapping)
    return df2

def transform_movies(df: pd.DataFrame) -> pd.DataFrame:
    import pandas as pd
    import numpy as np

    df = apply_aliases(df).copy()

    # If alias mapping caused duplicate column names, keep only the first occurrence
    df = df.loc[:, ~df.columns.duplicated(keep="first")]

    # Clean text columns
    for col in ["title","overview","director","cast","language","country","poster_url","imdb_id"]:
        if col in df.columns:
            df[col] = df[col].apply(_clean_text)

    # Normalize genres
    if "genres" in df.columns:
        df["genres"] = df["genres"].apply(_normalize_genres)

    # Clean runtime
    if "runtime" in df.columns:
        df["runtime"] = df["runtime"].apply(_clean_runtime)

    # Safe numeric columns
    for col in ["imdb_rating","tmdb_rating","popularity","tmdb_vote_count","imdb_votes"]:
        if col in df.columns:
            c = df[col]
            # If duplicate column names produced a DataFrame, take the first column
            if isinstance(c, pd.DataFrame):
                c = c.iloc[:, 0]
            # Flatten any list/array stored in a cell to its first scalar
            c = c.apply(lambda x: x[0] if isinstance(x, (list, np.ndarray)) and len(x) > 0 else x)
            df[col] = pd.to_numeric(c, errors="coerce")

    # Clean release_date
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # Parse year
    df["year"] = df.apply(_parse_year, axis=1)
    df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # Clean title
    if "title" in df.columns:
        df["title"] = df["title"].astype(str).str.replace(r"\(\d{4}\)", "", regex=True).str.strip()
        df["title"] = df["title"].replace({"nan": np.nan})

    # Keep only canonical columns
    keep = [c for c in CANONICAL if c in df.columns]
    out = df[keep].copy()

    # Drop duplicates
    if "imdb_id" in out.columns and out["imdb_id"].notna().any():
        out = out.drop_duplicates(subset=["imdb_id"])
    elif "title" in out.columns and "year" in out.columns:
        out = out.drop_duplicates(subset=["title","year"])
    elif "title" in out.columns:
        out = out.drop_duplicates(subset=["title"])

    # Drop ID columns — not needed downstream
    out = out.drop(columns=[c for c in ["imdb_id", "tmdb_id"] if c in out.columns])

    return out.reset_index(drop=True)
