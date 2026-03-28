import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.risk_engine import assess_vendor
from src.recommendation_engine import generate_recommendations

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDORS_PATH = os.path.join(BASE_DIR, "data", "sample_vendors.csv")


def load_vendors() -> pd.DataFrame:
    return pd.read_csv(VENDORS_PATH)


def score_all_vendors(df: pd.DataFrame) -> pd.DataFrame:
    """Run risk engine over all vendors and return enriched DataFrame."""
    records = []
    for _, row in df.iterrows():
        vendor = row.to_dict()
        result = assess_vendor(vendor)
        recs = generate_recommendations(result)
        records.append({
            "vendor_name": result["vendor_name"],
            "country": vendor["country"],
            "data_sensitivity": vendor["data_sensitivity"],
            "access_level": vendor["access_level"],
            "compliance_status": vendor["compliance_status"],
            "business_criticality": vendor["business_criticality"],
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "recommendations": " | ".join(recs),
        })
    return pd.DataFrame(records).sort_values("risk_score", ascending=False).reset_index(drop=True)
