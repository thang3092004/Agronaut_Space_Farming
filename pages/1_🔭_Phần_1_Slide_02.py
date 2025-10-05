import streamlit as st
from pathlib import Path
import base64

st.title("Part 1 — Slide 02: The Analysis Core")

def _b64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode()

bg_b64 = _b64("assets/asset part 1/background/space_dark.png")
cockpit_b64 = _b64("assets/asset part 1/background/cockpit.png")

html = f"""
<style>
.hero-container {{position:relative; width:100%; height:640px; overflow:hidden;}}
.hero-container::before {{content:""; position:absolute; inset:0; background:url(data:image/png;base64,{bg_b64}) center/cover no-repeat; filter:brightness(.95); z-index:1;}}
.hero-container img.cockpit {{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:clamp(680px,75vw,1050px); max-width:96%; height:auto; z-index:2; pointer-events:none;}}
.hero-container .overlay-text {{position:absolute; top:46%; left:50%; transform:translate(-50%,-50%); width:min(780px,75%); z-index:3; text-align:center;}}
.hero-container .overlay-text p {{margin:0; color:#e7e8ff; font-size:18px; line-height:1.6; text-align:center;}}
@media (max-width: 900px) {{
    .hero-container {{height:560px;}}
    .hero-container img.cockpit {{width:clamp(600px,80vw,960px);}}
                .hero-container .overlay-text {{top:48%;}}
        .hero-container .overlay-text p {{font-size:16px;}}
}}
@media (max-width: 600px) {{
    .hero-container {{height:520px;}}
    .hero-container img.cockpit {{width:clamp(520px,88vw,860px);}}
                .hero-container .overlay-text {{top:49%;}}
        .hero-container .overlay-text p {{font-size:15px; line-height:1.5;}}
}}
</style>
<div class="hero-container">
    <img class="cockpit" src="data:image/png;base64,{cockpit_b64}" alt="cockpit" />
    <div class="overlay-text fade-in">
        <p>
            I am <strong>COSMOS EYE</strong> – the ship's artificial intelligence.<br><br>
            Using data from NASA's <em>PHL Exoplanet Catalog</em>, I'll guide you to identify:<br>
            which planets burn like a furnace 🔥, which freeze like ice ❄️,<br>
            and which might retain <u>liquid water</u> – the key condition for life.
        </p>
        <div id="nav-btn-slot" style="margin-top:44px;"></div>
    </div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

col = st.columns([1,1])
with col[0]:
    back = st.button("⬅️ Back", key="_back_s2")
with col[1]:
    nxt = st.button("Continue ➡️", key="_next_s2")

if back:
    st.switch_page("pages/1_🔭_Phần_1_Slide_01.py")
if nxt:
    st.switch_page("pages/1_🔭_Phần_1_Slide_03.py")

st.markdown(
    """
<script>
(function(){
  const tries=[30,120,300];
  function move(label){
    const slot=document.getElementById('nav-btn-slot');
    if(!slot) return false;
    const wrap=[...document.querySelectorAll('div.stButton')].filter(d => (d.innerText||'').trim()===label);
    if(!wrap.length) return false;
    wrap.forEach(w=>{ if(!slot.contains(w)) slot.appendChild(w); });
    return true;
  }
    function attempt(){ return move('⬅️ Back') & move('Continue ➡️'); }
  if(!attempt()) tries.forEach(t=>setTimeout(attempt,t));
})();
</script>
""",
    unsafe_allow_html=True,
)
