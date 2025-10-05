import streamlit as st
from pathlib import Path
import base64

st.title("Part 2 — Slide 04: Crop Introduction")

def _b64(p: str) -> str:
    path = Path(p)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()

bg_b64 = _b64("assets/asset part 2/background/planet_surface.png")
eco_b64 = _b64("assets/asset part 2/plants/eco_moss.png")
hydro_b64 = _b64("assets/asset part 2/plants/hydro_corn.png")
luxi_b64 = _b64("assets/asset part 2/plants/luxi_berry.png")

css = """
<style>
.slide4-wrap {position:relative; width:100%; max-width:1200px; margin:0 auto;}
.slide4-wrap img.surface {width:100%; border-radius:14px; box-shadow:0 0 22px rgba(120,60,200,.45);}
.crop-icons {position:absolute; top:24%; left:50%; transform:translate(-50%,-50%); display:flex; gap:90px; justify-content:center; width:92%; flex-wrap:nowrap;}
.crop-icons .item {text-align:center; color:#f0ecff;}
.crop-icons img {width:180px; height:auto; filter:drop-shadow(0 0 12px rgba(160,120,255,.55));}
.crop-icons .name {margin-top:10px; font-size:20px; font-weight:600; letter-spacing:.5px;}
.desc-box {position:absolute; top:56%; left:50%; transform:translate(-50%,0); width:92%; max-width:1120px; background:rgba(15,10,35,0.60); padding:24px 30px 26px; color:#f5f4ff; font-size:14.2px; line-height:1.38; border:1px solid rgba(150,120,255,.35); border-radius:14px; box-shadow:0 0 18px rgba(80,40,140,.45), 0 0 0 1px rgba(255,255,255,0.04); backdrop-filter:blur(3px);}
.desc-box h3 {margin:0 0 10px; font-size:19px; letter-spacing:.6px;}
.desc-box p {margin:0 0 12px;}
.desc-box ul {margin:0 0 12px 20px; padding:0;}
.desc-box li {margin-bottom:6px;}
@media (max-width:1150px) { .crop-icons {gap:70px;} }
@media (max-width:1000px) { .crop-icons img {width:150px;} .crop-icons {gap:60px;} }
@media (max-width:860px)  { .crop-icons img {width:125px;} .crop-icons {gap:46px; top:26%;} }
@media (max-width:760px)  { .crop-icons {flex-wrap:wrap; gap:40px; top:28%;} .desc-box {top:60%;} }
@media (max-width:600px)  { .crop-icons img {width:105px;} .crop-icons {gap:34px;} .desc-box {top:60%; font-size:13.4px;} }
@media (max-width:520px)  { .crop-icons img {width:90px;} .crop-icons {gap:26px;} .crop-icons .name {font-size:15px;} .desc-box {padding:18px 18px 20px; top:60%;} }
</style>
"""

icons_html = f"""
<div class='slide4-wrap'>
  {f'<img class="surface" src="data:image/png;base64,{bg_b64}" alt="planet surface" />' if bg_b64 else '<div style="padding:60px;text-align:center;color:#bbb;border:1px dashed #666;">(Missing planet_surface.png)</div>'}
  <div class='crop-icons'>
    <div class='item'>
      {f'<img src="data:image/png;base64,{eco_b64}" alt="EcoMoss" />' if eco_b64 else '<div style="color:#ccc">(missing eco_moss.png)</div>'}
      <div class='name'>EcoMoss</div>
    </div>
    <div class='item'>
      {f'<img src="data:image/png;base64,{hydro_b64}" alt="HydroCorn" />' if hydro_b64 else '<div style="color:#ccc">(missing hydro_corn.png)</div>'}
      <div class='name'>HydroCorn</div>
    </div>
    <div class='item'>
      {f'<img src="data:image/png;base64,{luxi_b64}" alt="LuxiBerry" />' if luxi_b64 else '<div style="color:#ccc">(missing luxi_berry.png)</div>'}
      <div class='name'>LuxiBerry</div>
    </div>
  </div>
  <div class='desc-box'>
    <h3>Interstellar Bio‑Engineered Crops</h3>
    <p><em>Three engineered species designed for survival in off-world habitats:</em></p>
    <ul>
      <li><strong>EcoMoss</strong> – resilient moss that humidifies soil and stabilizes the micro-climate.</li>
      <li><strong>HydroCorn</strong> – reliable hydroponic maize providing steady food yield.</li>
      <li><strong>LuxiBerry</strong> – glowing berry rich in nutrients but fragile and high-value.</li>
    </ul>
    <p><strong>Combine strategically:</strong> EcoMoss supports LuxiBerry, while HydroCorn sustains your colony.</p>
  </div>
</div>
"""

st.markdown(css + icons_html, unsafe_allow_html=True)

nav = st.columns([1,1])
with nav[0]:
  if st.button("⬅️ Back"):
    st.switch_page("pages/2_🌱_Phần_2_Slide_03.py")
with nav[1]:
  if st.button("Continue ➡️"):
    st.switch_page("pages/2_🌱_Phần_2_Slide_05.py")
