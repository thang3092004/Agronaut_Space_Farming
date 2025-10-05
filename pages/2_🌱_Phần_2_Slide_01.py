import streamlit as st
from pathlib import Path
import base64

st.title("Part 2 — Slide 01: Landing")

def _b64(p: str) -> str:
    path = Path(p)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()

surface_b64 = _b64("assets/asset part 2/background/planet_surface.png")

text_html = (
    "We have landed! 🚀<br/>"
    "This is the planet you chose to explore.<br/><br/>"
    "Its surface glows with mystic violet patches, with a few remaining pools of water — early signs this place may sustain life."
)

html = f"""
<style>
.landing-wrap {{position:relative; width:100%; max-width:1200px; margin:0 auto;}}
.landing-wrap img.surface {{width:100%; border-radius:10px; box-shadow:0 0 18px rgba(120,60,200,.45); opacity:0; animation:fadeInSurface 1.2s ease-out .05s forwards;}}
.landing-text {{position:absolute; top:6%; left:50%; transform:translateX(-50%); width:min(880px,92%); color:#f1efff; background:rgba(40,10,70,.42); padding:18px 26px; border:1px solid rgba(160,110,255,.35); border-radius:18px; backdrop-filter:blur(4px); -webkit-backdrop-filter:blur(4px); font-size:18px; line-height:1.55; box-shadow:0 0 12px rgba(150,90,255,.35) inset, 0 0 24px rgba(90,40,150,.35); opacity:0; animation:fadeInPanel 1.1s ease-out .35s forwards;}}
@keyframes fadeInSurface {{0% {{opacity:0; transform:scale(1.015);}} 100% {{opacity:1; transform:scale(1);}}}}
@keyframes fadeInPanel {{0% {{opacity:0; transform:translate(-50%,-4%) scale(.97);}} 100% {{opacity:1; transform:translate(-50%,0) scale(1);}}}}
@media (max-width:900px) {{
    .landing-text {{font-size:16px; top:5%; padding:16px 20px;}}
}}
@media (max-width:600px) {{
    .landing-text {{font-size:15px; top:4%; line-height:1.48;}}
}}
</style>
<div class="landing-wrap">
  {f'<img class="surface" src="data:image/png;base64,{surface_b64}" alt="planet surface" />' if surface_b64 else '<div style="padding:60px;text-align:center;color:#ccc;border:1px dashed #666;">(Missing planet_surface.png)</div>'}
  <div class="landing-text">{text_html}</div>
</div>
<div id="btn-slot" style="text-align:center; margin-top:32px;"></div>
"""

st.markdown(html, unsafe_allow_html=True)

col = st.columns([1,1])
with col[0]:
    back = st.button("⬅️ Back", key="_back_p2_s1")
with col[1]:
    nxt = st.button("Deploy Recon Robot", key="_next_p2_s1")

if back:
    st.switch_page("pages/1_🔭_Phần_1_Slide_10.py")
if nxt:
    st.switch_page("pages/2_🌱_Phần_2_Slide_02.py")
