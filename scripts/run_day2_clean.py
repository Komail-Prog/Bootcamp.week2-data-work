import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from bootcamp_data.config import make_paths
from bootcamp_data.io import read_orders_csv, read_users_csv, write_parquet
from bootcamp_data.transforms import enforce_schema,missingness_report, add_missing_flags, normalize_text, apply_mapping
from bootcamp_data.quality import require_columns, assert_non_empty, assert_in_range


pa = make_paths(ROOT)




orders = read_orders_csv(pa.raw / "orders.csv")
users = read_users_csv(pa.raw / "users.csv")



require_columns(orders, ["order_id", "status", "amount", "quantity"])
assert_non_empty(orders)

require_columns(users, ["user_id", "1 country","signup_date"])
assert_non_empty(users)


df = enforce_schema(orders)


report_df = missingness_report(df)
report_df.to_csv(pa.reports / "missingness_report.csv", index=False)


df["status_clean"] = normalize_text(df["status"]) 


df = add_missing_flags(df, ["amount", "quantity"])

assert_in_range(df["amount"], lo=0, name="amount")
assert_in_range(df["quantity"], lo=0, name="quantity")

write_parquet(df, pa.processed / "orders_clean.parquet")

print("Day 2 finished successfully!")



