import streamlit as st
from pathlib import Path
import base64

st.title("Part 1 — Slide 06: Regression Insight")

def _b64(path: str) -> str:
		p = Path(path)
		if not p.exists():
				return ""
		return base64.b64encode(p.read_bytes()).decode()

bg_b64 = _b64("assets/asset part 1/background/space_dark.png")
cockpit_b64 = _b64("assets/asset part 1/background/cockpit.png")

text_html = (
	'<b>Thanks to those fascinating observations</b>, scientists used regression to predict which planets might host life — just by looking at their special traits, such as:<br/><br/>'
	'🌞 <b>Star light received</b> — how much sunlight the planet gets<br/>'
	'🌡️ <b>Temperature</b> — whether it’s cozy or too extreme<br/>'
	'🌍 <b>Planet size</b> — tiny rocky world or giant gas ball<br/>'
	'🪐 <b>Orbit period</b> — how long it takes to circle its star<br/><br/>'
	'This helps us choose the right planets to explore and save fuel on every journey. 🚀'
)

html = f"""
<style>
.hero-container {{position:relative; width:100%; height:640px; overflow:hidden;}}
.hero-container::before {{content:""; position:absolute; inset:0; background:url(data:image/png;base64,{bg_b64}) center/cover no-repeat; filter:brightness(.95); z-index:1;}}
.hero-container img.cockpit {{position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:clamp(680px,75vw,1050px); max-width:96%; height:auto; z-index:2; pointer-events:none;}}
.hero-container .overlay-text {{position:absolute; top:48%; left:50%; transform:translate(-50%,-50%); width:min(780px,75%); z-index:3; text-align:left; color:#e7e8ff;}}
.hero-container .overlay-text p {{margin:0; font-size:14.2px; line-height:1.47;}}
.nav-slot {{margin-top:44px; text-align:center;}}
@media (max-width: 900px) {{
	.hero-container {{height:560px;}}
	.hero-container img.cockpit {{width:clamp(600px,80vw,960px);}}
	.hero-container .overlay-text {{top:50%;}}
	.hero-container .overlay-text p {{font-size:12.7px;}}
}}
@media (max-width: 600px) {{
	.hero-container {{height:520px;}}
	.hero-container img.cockpit {{width:clamp(520px,88vw,860px);}}
	.hero-container .overlay-text {{top:51%;}}
	.hero-container .overlay-text p {{font-size:12.3px; line-height:1.44;}}
}}
</style>
<div class="hero-container">
	<img class="cockpit" src="data:image/png;base64,{cockpit_b64}" alt="cockpit" />
	<div class="overlay-text">
		<p>{text_html}</p>
		<div id="nav-btn-slot" class="nav-slot"></div>
	</div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

col = st.columns([1,1])
with col[0]:
		back = st.button("⬅️ Back", key="_back_s6")
with col[1]:
		nxt = st.button("Continue ➡️", key="_next_s6")

if back:
		st.switch_page("pages/1_🔭_Phần_1_Slide_05.py")
if nxt:
		st.switch_page("pages/1_🔭_Phần_1_Slide_07.py")

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
