from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/anomalies",
    tags=["Anomalies"]
)


# --------------------------------------------------
# CSV PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

CSV_PATH = BASE_DIR / "results" / "water_anomaly_results.csv"


# --------------------------------------------------
# Load anomaly data
# --------------------------------------------------

def load_anomaly_data():

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Anomaly results file not found: {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    return df


# --------------------------------------------------
# GET ALL ANOMALIES
# --------------------------------------------------

@router.get("/")
def get_anomalies():

    try:

        df = load_anomaly_data()

        # Consider anything other than Normal as a flagged anomaly
        anomalies = df[
            df["Leakage_Risk"].str.lower() != "normal"
        ].copy()

        # Convert datetime to string
        anomalies["Datetime"] = anomalies["Datetime"].astype(str)

        # Convert pandas/numpy values to normal Python values
        records = anomalies.to_dict(orient="records")

        return {
            "status": "success",
            "total_anomalies": len(records),
            "anomalies": records
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# GET ANOMALY SUMMARY
# --------------------------------------------------

@router.get("/summary")
def get_anomaly_summary():

    try:

        df = load_anomaly_data()

        total_records = len(df)

        normal_count = int(
            (df["Leakage_Risk"].str.lower() == "normal").sum()
        )

        anomaly_count = int(
            (df["Leakage_Risk"].str.lower() != "normal").sum()
        )

        risk_counts = (
            df["Leakage_Risk"]
            .value_counts()
            .to_dict()
        )

        # Convert NumPy integers to Python integers
        risk_counts = {
            str(key): int(value)
            for key, value in risk_counts.items()
        }

        return {
            "status": "success",
            "total_records": total_records,
            "normal_records": normal_count,
            "anomaly_records": anomaly_count,
            "risk_distribution": risk_counts
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# GET CRITICAL ANOMALIES
# --------------------------------------------------

@router.get("/critical")
def get_critical_anomalies():

    try:

        df = load_anomaly_data()

        critical = df[
            df["Leakage_Risk"].str.lower() == "critical"
        ].copy()

        critical["Datetime"] = critical["Datetime"].astype(str)

        records = critical.to_dict(
            orient="records"
        )

        return {
            "status": "success",
            "total_critical": len(records),
            "anomalies": records
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )