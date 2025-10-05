import streamlit as st
from pathlib import Path
import base64

st.title("Part 1 — Slide 05: Clusters & Classification")

def _b64(path: str) -> str:
        p = Path(path)
        if not p.exists():
                return ""
        return base64.b64encode(p.read_bytes()).decode()

bg_b64 = _b64("assets/asset part 1/background/space_dark.png")
cockpit_b64 = _b64("assets/asset part 1/background/cockpit.png")
cluster_b64 = _b64("assets/asset part 1/charts/cluster.png")

text_html = (
    '🧬 <b>Cluster and Classification in Data</b><br/>'
    'When clustering, something interesting appears:<br/>'
    'The group of planets with a higher chance of life tends to be the one with an average distance from their host star and moderate sunlight exposure.'
)

html = f"""
<style>
.hero-container {{position:relative; width:100%; height:640px; overflow:hidden;}}
.hero-container::before {{content:""; position:absolute; inset:0; background:url(data:image/png;base64,{bg_b64}) center/cover no-repeat; filter:brightness(.95); z-index:1;}}
.hero-container img.cockpit {{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:clamp(680px,75vw,1050px); max-width:96%; height:auto; z-index:2; pointer-events:none;}}
.hero-container .overlay-text {{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:min(760px,75%); z-index:3; text-align:center; color:#e7e8ff;}}
.hero-container .overlay-text p {{margin:0; font-size:17px; line-height:1.55;}}
.pairplot-wrapper {{margin-top:15px; display:flex; justify-content:center;}}
.pairplot-wrapper img {{max-width:308px; width:59%; border:1px solid rgba(0,255,255,.35); border-radius:14px; box-shadow:0 0 14px rgba(0,255,255,.3), 0 0 34px rgba(120,60,200,.35) inset;}}
.nav-slot {{margin-top:46px;}}
@media (max-width: 900px) {{
    .hero-container {{height:560px;}}
    .hero-container img.cockpit {{width:clamp(600px,80vw,960px);}}
        .hero-container .overlay-text {{top:52%;}}
    .hero-container .overlay-text p {{font-size:15px;}}
}}
@media (max-width: 600px) {{
    .hero-container {{height:520px;}}
    .hero-container img.cockpit {{width:clamp(520px,88vw,860px);}}
        .hero-container .overlay-text {{top:53%;}}
    .hero-container .overlay-text p {{font-size:14px; line-height:1.48;}}
}}
</style>
<div class=\"hero-container\">
    <img class=\"cockpit\" src=\"data:image/png;base64,{cockpit_b64}\" alt=\"cockpit\" />
    <div class=\"overlay-text\">
        <p>{text_html}</p>
        <div class=\"pairplot-wrapper\">
            {f'<img src="data:image/png;base64,{cluster_b64}" alt="Cluster Visualization" />' if cluster_b64 else '<div style="color:#9fd7ff;font-size:14px; padding:8px 12px; border:1px dashed rgba(0,255,255,.4); border-radius:10px; background:rgba(10,50,80,.35);">(Missing cluster.png)</div>'}
        </div>
        <div id=\"nav-btn-slot\" class=\"nav-slot\"></div>
    </div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

col = st.columns([1,1])
with col[0]:
        back = st.button("⬅️ Back", key="_back_s5")
with col[1]:
        nxt = st.button("Continue ➡️", key="_next_s5")

if back:
        st.switch_page("pages/1_🔭_Phần_1_Slide_04.py")
if nxt:
        st.switch_page("pages/1_🔭_Phần_1_Slide_06.py")

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
