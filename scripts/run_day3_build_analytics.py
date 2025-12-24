import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from bootcamp_data.config import make_paths
from bootcamp_data.io import read_parquet,write_parquet
from bootcamp_data.quality import require_columns, assert_non_empty, assert_unique_key
from bootcamp_data.transforms import parse_datetime, add_time_parts, winsorize
from bootcamp_data.joins import safe_left_join

pa = make_paths(ROOT)

orders = read_parquet(pa.processed / "orders_clean.parquet")
users = read_parquet(pa.processed / "users_clean.parquet")


assert_non_empty(orders)
assert_unique_key(users, "user_id")

orders = parse_datetime(orders, "created_at")
orders = add_time_parts(orders, "created_at")

df_analytics = safe_left_join(
    left=orders, 
    right=users, 
    on="user_id", 
    validate="many_to_one"
)


df_analytics["amount_winsor"] = winsorize(df_analytics["amount"], lo=0.05, hi=0.95)
df_analytics["amount_is_outlier"] = df_analytics["amount"] != df_analytics["amount_winsor"]

write_parquet(df_analytics, pa.processed / "analytics_table.parquet")


country_stats = (
    df_analytics.groupby("country")
    .agg(
        total_revenue=("amount", "sum"),
        order_count=("order_id", "count")
    )
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)


print("\n--- Revenue by Country ---")
print(country_stats)


country_stats.to_csv(pa.reports / "revenue_by_country.csv", index=False)

print("Day 3: Analytics table built successfully!")
