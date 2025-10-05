import streamlit as st
from pathlib import Path
import base64
import time

st.title("Part 1 — Slide 10: Initiating Transit")

def _b64(p: str) -> str:
    path = Path(p)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()

warp_b64 = _b64("assets/asset part 1/background/warp.png")

st.markdown(
        f"""
<style>
.warp-stage {{position:relative; width:100%; height:520px; display:flex; align-items:center; justify-content:center; overflow:hidden;}}
.warp-stage::before {{content:""; position:absolute; inset:0; background:#000 url(data:image/png;base64,{warp_b64}) center/cover no-repeat; filter:brightness(1); animation:zoomWarp 12s linear infinite alternate; opacity:0.9;}}
@keyframes zoomWarp {{from {{transform:scale(1);}} to {{transform:scale(1.12);}} }}
.warp-overlay {{position:relative; z-index:2; text-align:center; max-width:880px; padding:28px 34px; background:rgba(5,12,25,0.55); backdrop-filter:blur(6px); border:1px solid rgba(0,255,255,.25); border-radius:18px; box-shadow:0 0 22px rgba(0,180,255,.35), 0 0 60px rgba(90,40,160,.25) inset;}}
.warp-overlay h2 {{margin:0 0 14px; font-size:30px; letter-spacing:.5px; background:linear-gradient(90deg,#9be9ff,#fff); -webkit-background-clip:text; color:transparent;}}
.warp-line {{font-size:20px; line-height:1.6; color:#d9f6ff; animation:fadeIn 1.2s ease;}}
@keyframes fadeIn {{from {{opacity:0; transform:translateY(14px);}} to {{opacity:1; transform:translateY(0);}} }}
.auto-msg {{margin-top:18px; font-size:14px; color:#9ad7ff; opacity:.85;}}
@media (max-width:800px){{.warp-stage{{height:480px;}} .warp-overlay h2{{font-size:24px;}} .warp-line{{font-size:17px;}} }}
</style>
<div class=\"warp-stage\">
    <div class=\"warp-overlay\">
        <h2>Stellar Transfer Engaged</h2>
        <div class=\"warp-line\">You have begun your journey toward the hopeful planet.<br/>Preparing surface deployment protocols...</div>
        <div class=\"auto-msg\">Auto-transitioning to difficulty selection...</div>
        <div id=\"nav-btn-slot\" style=\"margin-top:26px;\"></div>
    </div>
</div>
""",
        unsafe_allow_html=True,
)

col = st.columns([1,1])
with col[0]:
    if st.button("⬅️ Back"):
        st.switch_page("pages/1_🔭_Phần_1_Slide_09.py")
with col[1]:
    if st.button("Skip Now ➡️"):
        st.switch_page("pages/2_🌱_Phần_2_Slide_00.py")

# Auto redirect after short delay (client-side)
st.markdown(
    """
<script>
setTimeout(function(){
  window.location.href = window.location.origin + '/?page=pages/2_%F0%9F%8C%B1_Ph%E1%BA%A7n_2_Slide_00.py';
}, 4200);
</script>
""",
    unsafe_allow_html=True,
)
