import streamlit as st
from pathlib import Path
import base64
import pandas as pd
import random
from logic.difficulty import get_difficulty

st.title("Part 2 — Slide 03: Planet Condition Report")

def _b64(p: str) -> str:
    path = Path(p)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()

bg_b64 = _b64("assets/asset part 2/background/planet_surface.png")

# Decide dataset file based on difficulty (Iowa / Texas) forecast naming pattern
diff = get_difficulty()  # 'medium' or 'hard'
region_name = 'Iowa' if diff == 'medium' else 'Texas'
forecast_filename = f"data/interpolated/{region_name}_2026_Forecast.csv"

def load_random_row(path: str) -> pd.Series:
    if not Path(path).exists():
        return pd.Series({
            'soil': 'NA', 'rain': 'NA', 'temp': 'NA', 'drought': 'NA'
        })
    try:
        df = pd.read_csv(path)
        if df.empty:
            return pd.Series({
                'soil': 'NA', 'rain': 'NA', 'temp': 'NA', 'drought': 'NA'
            })
        row = df.sample(1, random_state=random.randint(0, 999999)).iloc[0]
        # Attempt to map likely column names (flexible naming)
        col_map = {
            'soil': [c for c in df.columns if 'soil' in c.lower() or 'moist' in c.lower()],
            'rain': [c for c in df.columns if 'rain' in c.lower() or 'precip' in c.lower()],
            'temp': [c for c in df.columns if 'temp' in c.lower()],
            'drought': [c for c in df.columns if 'drought' in c.lower() or 'dry' in c.lower()],
        }
        def pick(key, default):
            cols = col_map[key]
            return row[cols[0]] if cols else default
        return pd.Series({
            'soil': pick('soil', 'NA'),
            'rain': pick('rain', 'NA'),
            'temp': pick('temp', 'NA'),
            'drought': pick('drought', 'NA'),
        })
    except Exception:
        return pd.Series({
            'soil': 'ERR', 'rain': 'ERR', 'temp': 'ERR', 'drought': 'ERR'
        })

metrics = load_random_row(forecast_filename)

# Round numeric values to 3 decimals for display
def _fmt(v):
  try:
    if isinstance(v, (int, float)):
      return f"{float(v):.3f}"
    # try cast
    fv = float(str(v))
    return f"{fv:.3f}"
  except Exception:
    return v
metrics = metrics.apply(_fmt)

icons = {
    'soil': 'assets/asset part 2/icons/icon_soil.png',
    'rain': 'assets/asset part 2/icons/icon_rain.png',
    'temp': 'assets/asset part 2/icons/icon_temp.png',
    'drought': 'assets/asset part 2/icons/icon_drought.png',
}

html = f"""
<style>
.landing-wrap {{position:relative; width:100%; max-width:1200px; margin:0 auto;}}
.landing-wrap img.surface {{width:100%; border-radius:10px; box-shadow:none;}}
.metrics-grid {{position:absolute; top:30%; left:50%; transform:translateX(-50%); display:grid; grid-template-columns:repeat(4, minmax(120px, 1fr)); gap:26px; width:min(900px,90%);}}
.metric-box {{background:rgba(25,10,60,.45); border:1px solid rgba(150,110,240,.25); border-radius:12px; padding:10px 8px; text-align:center; color:#f1f1ff; font-size:13px; backdrop-filter:none; box-shadow:none;}}
.metric-box img {{width:52px; height:auto; margin-bottom:4px; filter:none;}}
.planet-note {{position:absolute; top:62%; left:50%; transform:translate(-50%, -50%); text-align:center; color:#e9e7ff; font-size:15px; line-height:1.45; background:rgba(20,10,40,.35); padding:10px 18px; border:1px solid rgba(150,110,240,.25); border-radius:12px; backdrop-filter:none; box-shadow:none; width:min(880px,88%); opacity:1;}}
@media (max-width:900px) {{
  .metrics-grid {{grid-template-columns:repeat(2, minmax(120px,1fr)); gap:18px; top:34%;}}
  .metric-box img {{width:52px;}}
}}
@media (max-width:600px) {{
  .planet-note {{font-size:14px;}}
}}
</style>
<div class="landing-wrap">
  {f'<img class="surface" src="data:image/png;base64,{bg_b64}" alt="planet surface" />' if bg_b64 else '<div style="padding:60px;text-align:center;color:#ccc;border:1px dashed #666;">(Missing planet_surface.png)</div>'}
  <div class="metrics-grid">
    <div class="metric-box">
      <img src="{_b64(icons['soil']) and f'data:image/png;base64,{_b64(icons['soil'])}' if Path(icons['soil']).exists() else ''}" alt="soil" />
      <div><b>Soil</b><br>{metrics['soil']}</div>
    </div>
    <div class="metric-box">
      <img src="{_b64(icons['rain']) and f'data:image/png;base64,{_b64(icons['rain'])}' if Path(icons['rain']).exists() else ''}" alt="rain" />
      <div><b>Rain</b><br>{metrics['rain']}</div>
    </div>
    <div class="metric-box">
      <img src="{_b64(icons['temp']) and f'data:image/png;base64,{_b64(icons['temp'])}' if Path(icons['temp']).exists() else ''}" alt="temp" />
      <div><b>Temp</b><br>{metrics['temp']}</div>
    </div>
    <div class="metric-box">
      <img src="{_b64(icons['drought']) and f'data:image/png;base64,{_b64(icons['drought'])}' if Path(icons['drought']).exists() else ''}" alt="drought" />
      <div><b>Drought</b><br>{metrics['drought']}</div>
    </div>
  </div>
  <div class="planet-note">According to the collected data, the environment here is similar to <b>{region_name}</b> in the United States. We can leverage Earth-based agricultural experience to cultivate this planet.</div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

col = st.columns([1,1])
with col[0]:
  if st.button("⬅️ Back"):
    st.switch_page("pages/2_🌱_Phần_2_Slide_02.py")
with col[1]:
  if st.button("Continue ➡️"):
    st.switch_page("pages/2_🌱_Phần_2_Slide_04.py")
