import pandas as pd
import numpy as np

def load_exoplanets_demo(n=200, seed=7):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "name": [f"Planet {i}" for i in range(n)],
        "distance": rng.uniform(0.2, 3.0, n),   # AU
        "surface_temp": rng.uniform(150, 500, n), # Kelvin
        "esi": rng.uniform(0, 1, n)
    })
    p = 1 - np.clip(np.abs(df["distance"]-1.2)/1.5 + np.abs(df["surface_temp"]-290)/250, 0, 1)
    df["probability"] = p
    return df
