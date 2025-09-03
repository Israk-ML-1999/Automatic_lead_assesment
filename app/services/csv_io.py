# CSV read/write utilities
import pandas as pd
from pathlib import Path

COLUMNS = [
    "first_name","last_name","email","company","job_title","linkedin_url","notes",
    "persona","priority","status","email_subject","email_body","score","response_category","email_sent_at"
]

def read_leads(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(p)
    for c in COLUMNS:
        if c not in df.columns:
            df[c] = "" if c not in ("score",) else 0
    return df[COLUMNS]

def write_leads(df: pd.DataFrame, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    out_path = Path(path).with_name("lead_out.csv")
    df.to_csv(out_path, index=False)


def write_leads(df: pd.DataFrame, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
