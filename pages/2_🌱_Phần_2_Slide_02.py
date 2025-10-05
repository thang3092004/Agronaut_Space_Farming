import streamlit as st
from pathlib import Path
import base64

st.title("Part 2 — Slide 02: Surface Scan")

def _b64(p: str) -> str:
    path = Path(p)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()

surface_b64 = _b64("assets/asset part 2/background/planet_surface.png")
robot_b64 = _b64("assets/asset part 2/effects/scanner_robot.png")

html = f"""
<style>
.landing-wrap {{position:relative; width:100%; max-width:1200px; margin:0 auto;}}
.landing-wrap img.surface {{width:100%; border-radius:10px; box-shadow:0 0 18px rgba(120,60,200,.45);}}
.robot-center {{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:clamp(140px,24vw,240px); opacity:0; animation:fadeInRobot 1.2s ease-out .15s forwards;}}
.scan-caption {{position:absolute; bottom:5%; left:50%; transform:translateX(-50%); background:rgba(25,10,55,.55); padding:14px 24px; border:1px solid rgba(150,110,240,.35); border-radius:16px; color:#f1f1ff; font-size:17px; line-height:1.48; width:min(760px,85%); text-align:center; opacity:0; animation:fadeInPanel .9s ease-out .6s forwards; box-shadow:0 0 12px rgba(140,90,240,.35) inset, 0 0 22px rgba(80,40,140,.35);}}
@keyframes fadeInRobot {{0% {{opacity:0; transform:translate(-50%,-54%) scale(.82); filter:blur(3px);}} 55% {{opacity:.85; filter:blur(.4px);}} 100% {{opacity:1; transform:translate(-50%,-50%) scale(1);}}}}
@keyframes fadeInPanel {{0% {{opacity:0; transform:translate(-50%,14%) scale(.96);}} 100% {{opacity:1; transform:translate(-50%,0) scale(1);}}}}
@media (max-width:900px) {{
  .scan-caption {{font-size:15px;}}
}}
@media (max-width:600px) {{
  .scan-caption {{font-size:14px; line-height:1.42;}}
}}
</style>
<div class="landing-wrap">
  {f'<img class="surface" src="data:image/png;base64,{surface_b64}" alt="planet surface" />' if surface_b64 else '<div style="padding:60px;text-align:center;color:#ccc;border:1px dashed #666;">(Missing planet_surface.png)</div>'}
  {f'<img class="robot-center" src="data:image/png;base64,{robot_b64}" alt="scanner robot" />' if robot_b64 else ''}
  <div class="scan-caption">Robot is scanning planetary surface and atmosphere...</div>
</div>
<div style="height:30px;"></div>
"""

st.markdown(html, unsafe_allow_html=True)

col = st.columns([1,1])
with col[0]:
    back = st.button("⬅️ Back", key="_back_p2_s2")
with col[1]:
    nxt = st.button("Receive Analysis", key="_next_p2_s2")

if back:
    st.switch_page("pages/2_🌱_Phần_2_Slide_01.py")
if nxt:
    st.switch_page("pages/2_🌱_Phần_2_Slide_03.py")
