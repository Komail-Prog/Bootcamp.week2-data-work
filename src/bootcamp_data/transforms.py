import pandas as pd
import re

def enforce_schema(df: pd.DataFrame) -> pd.DataFrame:
 return df.assign(
    order_id=df["order_id"].astype("string"),
    user_id=df["user_id"].astype("string"),
    amount=pd.to_numeric(df["amount"], errors="coerce").astype("Float64"),
    quantity=pd.to_numeric(df["quantity"], errors="coerce").astype("Int64"),
)


def missingness_report(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.isna().sum()
        .rename("n_missing")
        .to_frame()
        .assign(p_missing=lambda t: t["n_missing"] / len(df))
        .sort_values("p_missing", ascending=False)
    )

def add_missing_flags(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        out[f"{c}__isna"] = out[c].isna()
    return out


_ws = re.compile(r"\s+")

def normalize_text(s):
    return (
        s.astype("string")
        .str.strip()
        .str.casefold()
        .str.replace(_ws, " ", regex=True)
    )

def apply_mapping(s, mapping):
    return s.map(lambda x: mapping.get(x, x))

def parse_datetime(
    df: pd.DataFrame,
    col: str,
    *,
    utc: bool = True,
) -> pd.DataFrame:
    # Parse a timestamp column safely.
    # - invalid strings become NA (errors="coerce")
    # - utc=True gives timezone-aware timestamps (recommended default)
    dt = pd.to_datetime(df[col], errors="coerce", utc=utc)
    return df.assign(**{col: dt})

def add_time_parts(df: pd.DataFrame, ts_col: str) -> pd.DataFrame:
    # Add common time grouping keys (month, day-of-week, hour, etc.).
    ts = df[ts_col]
    return df.assign(
    date=ts.dt.date,
    year=ts.dt.year,
    month=ts.dt.to_period("M").astype("string"),
    dow=ts.dt.day_name(),
    hour=ts.dt.hour,
    )

def iqr_bounds(s: pd.Series, k: float = 1.5) -> tuple[float, float]:
    # Return (lo, hi) IQR bounds for outlier flagging.
    x = s.dropna()
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1
    return float(q1 - k * iqr), float(q3 + k * iqr)

def winsorize(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    # Cap values to [p_lo, p_hi] (helpful for visualization, not deletion).
    x = s.dropna()
    a, b = x.quantile(lo), x.quantile(hi)
    return s.clip(lower=a, upper=b)

def outlier_flag(df: pd.DataFrame, col: str, *, k: float = 1.5) -> pd.DataFrame:
    lo, hi = iqr_bounds(df[col], k=k)
    return df.assign(**{f"{col}__is_outlier": (df[col] < lo) | (df[col] > hi)})