import pandas as pd

def extract_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )
    return df