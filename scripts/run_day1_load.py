from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from bootcamp_data.config import make_paths
from bootcamp_data.io import read_orders_csv, write_parquet
from bootcamp_data.transforms import enforce_schema

pa = make_paths(ROOT)

rows = read_orders_csv(pa.raw / "orders.csv")

enforced_data = enforce_schema(rows)

out_path = ROOT / "data" / "processed" / "orders.parquet"


write_parquet(enforced_data, out_path)

print(f"Processed data saved to {out_path}")