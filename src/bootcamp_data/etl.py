import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import pandas as pd

from bootcamp_data.io import read_orders_csv, read_users_csv, write_parquet
from bootcamp_data.transforms import (
    enforce_schema, normalize_text, add_missing_flags, 
    parse_datetime, add_time_parts, winsorize, outlier_flag
)
from bootcamp_data.quality import require_columns, assert_unique_key
from bootcamp_data.joins import safe_left_join

log = logging.getLogger(__name__)

@dataclass(frozen=True)
class ETLConfig:
    root: Path
    raw_orders: Path
    raw_users: Path
    out_users_clean: Path
    out_analytics: Path
    run_meta: Path

    @classmethod
    def from_root(cls, root: Path):
        data = root / "data"
        return cls(
            root=root,
            raw_orders=data / "raw" / "orders.csv",
            raw_users=data / "raw" / "users.csv",
            out_users_clean=data / "processed" / "users_clean.parquet",
            out_analytics=data / "processed" / "analytics_table.parquet",
            run_meta=data / "processed" / "_run_meta.json",
        )

def load_inputs(cfg: ETLConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    log.info("Loading inputs...")
    orders = read_orders_csv(cfg.raw_orders)
    users = read_users_csv(cfg.raw_users)
    return orders, users

def transform(orders: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    log.info("Starting transformation pipeline")
    
   
    require_columns(orders, ["order_id", "user_id", "amount", "status", "created_at"])
    require_columns(users, ["user_id", "country"])
    assert_unique_key(users, "user_id")

   
    orders = enforce_schema(orders)
    users = enforce_schema(users)
    orders['status'] = normalize_text(orders['status'])
    
   
    orders = add_missing_flags(orders, cols=['amount', 'user_id'])
    orders = parse_datetime(orders, col="created_at")
    orders = add_time_parts(orders, ts_col="created_at")
    orders['amount_winsorized'] = winsorize(orders['amount'])
    orders = outlier_flag(orders, col="amount")

    
    analytics_table = safe_left_join(orders, users, on="user_id", validate="many_to_one")
    
    log.info(f"Transformation complete. Shape: {analytics_table.shape}")
    return analytics_table

def load_outputs(analytics: pd.DataFrame, users: pd.DataFrame, cfg: ETLConfig):
    log.info("Writing outputs...")
    write_parquet(analytics, cfg.out_analytics)
    write_parquet(users, cfg.out_users_clean)

  
    match_rate = analytics["country"].notna().mean()
    
    run_meta = {
        "run_at": datetime.now().isoformat(),
        "row_counts": {
            "input_users": len(users),
            "output_analytics": len(analytics)
        },
        "quality_metrics": {
            "country_match_rate": round(float(match_rate), 4)
        },
        "config_paths": {
            "analytics": str(cfg.out_analytics.relative_to(cfg.root))
        }
    }

    with open(cfg.run_meta, "w") as f:
        json.dump(run_meta, f, indent=4)

def run_etl(cfg: ETLConfig):
    orders_raw, users_raw = load_inputs(cfg)
    analytics_table = transform(orders_raw, users_raw)
    load_outputs(analytics_table, users_raw, cfg)
    log.info("ETL Run Finished.")