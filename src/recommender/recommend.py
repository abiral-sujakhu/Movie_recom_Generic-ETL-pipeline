import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _norm_title(t: str) -> str:
    t = t.lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t

class MovieRecommender:
    def __init__(self, df: pd.DataFrame, feature_col: str = "feature_text"):
        if "title" not in df.columns:
            raise ValueError("Dataset must have a 'title' column.")

        self.df = df.copy()
        self.df["title_norm"] = self.df["title"].astype(str).apply(_norm_title)

        self.tfidf = TfidfVectorizer(stop_words="english", max_features=50000)
        self.X = self.tfidf.fit_transform(self.df[feature_col].fillna(""))

    def _find_index(self, query: str) -> int:
        q = _norm_title(query)

        exact = self.df.index[self.df["title_norm"] == q].tolist()
        if exact:
            return exact[0]

        contains = self.df.index[self.df["title_norm"].str.contains(re.escape(q), na=False)].tolist()
        if contains:
            return contains[0]

        q_tokens = set(q.split())
        best_i, best_score = 0, -1
        for i, t in enumerate(self.df["title_norm"].values):
            score = len(q_tokens & set(t.split()))
            if score > best_score:
                best_score = score
                best_i = i
        return best_i

    def recommend(self, title: str, top_n: int = 10) -> pd.DataFrame:
        idx = self._find_index(title)
        sims = cosine_similarity(self.X[idx], self.X).flatten()

        order = sims.argsort()[::-1]
        order = [i for i in order if i != idx][: top_n * 5]

        recs = self.df.iloc[order].copy()
        recs["similarity"] = sims[order]

        for score_col in ["imdb_rating","tmdb_rating","popularity"]:
            if score_col in recs.columns:
                recs = recs.sort_values(["similarity", score_col], ascending=[False, False])
                break
        else:
            recs = recs.sort_values("similarity", ascending=False)

        show = ["title","similarity"]
        for c in ["year","genres","imdb_rating","tmdb_rating","popularity","poster_url"]:
            if c in recs.columns:
                show.append(c)

        return recs[show].head(top_n).reset_index(drop=True)