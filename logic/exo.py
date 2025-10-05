import numpy as np
import pandas as pd

def mark_candidates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["prob_label"] = np.where(df["probability"]>0.6, "green",
                         np.where(df["probability"]<0.2, "gray", "yellow"))
    df["cluster"] = np.where((df["distance"].between(0.8,1.6)) & (df["surface_temp"].between(250,330)),
                              "balanced", "other")
    return df

def regression_predict(df: pd.DataFrame) -> pd.DataFrame:
    a, b = 300, -20
    xs = np.linspace(df["distance"].min(), df["distance"].max(), 100)
    return pd.DataFrame({"distance": xs, "pred_temp": a + b*xs})
