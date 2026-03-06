from pathlib import Path
import pandas as pd

def load_csv(df: pd.DataFrame, out_path: str) -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path