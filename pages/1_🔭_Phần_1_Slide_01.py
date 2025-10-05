import streamlit as st
import altair as alt
import pandas as pd
from pathlib import Path
import base64
from logic.data import load_exoplanets_demo
from logic.exo import mark_candidates, regression_predict
from logic.farm import ensure_farm_state, render_grid, sidebar_actions, next_day
from logic.weather import ensure_weather_profile_ui

st.title("Part 1 — Slide 01: Mission Start")

# === Giải thích nhanh ===
# Bạn không nên dùng đường dẫn tuyệt đối kiểu C:\Users\... trong thuộc tính src của <img>
# vì trình duyệt không thể truy cập trực tiếp hệ thống tập tin local theo đường đó qua HTTP.
# Thay vào đó: (1) dùng đường dẫn tương đối tới file trong thư mục làm việc của app, hoặc (2) nhúng base64.
# Ở đây mình chuyển sang nhúng base64 để chắc chắn hiển thị kể cả khi trình duyệt không resolve được đường dẫn có khoảng trắng.

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
.fade-in {{animation:fadeInHero .9s ease-out .15s both;}}
@keyframes fadeInHero {{
    0% {{opacity:0; transform:translate(-50%,-46%) scale(.97);}}
    100% {{opacity:1; transform:translate(-50%,-50%) scale(1);}}
}}
.next-mp-btn {{
    margin:48px auto 0; display:inline-block; cursor:pointer; border:1px solid rgba(0,255,255,.45); color:#e7e8ff; font-weight:600; font-size:15px;
    padding:11px 34px; border-radius:28px; background:radial-gradient(circle at 30% 20%, rgba(0,90,140,.55), rgba(120,40,180,.55));
    backdrop-filter:blur(5px); -webkit-backdrop-filter:blur(5px);
    box-shadow:0 0 8px rgba(0,255,255,.35), 0 0 22px rgba(130,60,200,.35) inset;
    transition:.28s ease;
    animation:btnPulse 5s ease-in-out 1.2s infinite;
    transform:translateX(4%);
}}
.next-mp-btn:hover {{box-shadow:0 0 14px rgba(0,255,255,.7), 0 0 30px rgba(150,70,255,.55) inset; border-color:rgba(0,255,255,.8); transform:translateX(4%) translateY(-2px) scale(1.02);}}
.next-mp-btn:active {{transform:translateX(4%) translateY(0) scale(.99); box-shadow:0 0 10px rgba(0,255,255,.55), 0 0 22px rgba(150,70,255,.45) inset;}}
@keyframes btnPulse {{
    0% {{box-shadow:0 0 8px rgba(0,255,255,.35), 0 0 22px rgba(130,60,200,.35) inset; filter:brightness(1);}}
    50% {{box-shadow:0 0 16px rgba(0,255,255,.55), 0 0 34px rgba(150,70,255,.55) inset; filter:brightness(1.07);}}
    100% {{box-shadow:0 0 8px rgba(0,255,255,.35), 0 0 22px rgba(130,60,200,.35) inset; filter:brightness(1);}}
}}
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
            Hello, astronaut! 🚀<br><br>
            We are aboard the Agronaut, and this mission is truly special: find a planet capable of sustaining life.<br><br>
            Out there the universe is vast with billions of worlds—yet only a tiny fraction could become a second home for humanity.
        </p>
                <div id="btn-slot" style="margin-top:46px;"></div>
    </div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)

# Nút thật (render sau để có thể relocate vào cockpit)
_go = st.button("Continue ➡️")

# Nếu click (trước khi relocate JS) vẫn chuyển trang
if _go:
    st.switch_page("pages/1_🔭_Phần_1_Slide_02.py")

# JS relocate (dùng retries để chắc chắn tìm thấy)
st.markdown(
        """
<script>
(function(){
    const attempts=[30,120,300];
    function move(){
        const slot=document.getElementById('btn-slot');
        if(!slot) return false;
        const btnWrap=[...document.querySelectorAll('div.stButton')]
            .find(el => (el.innerText||'').trim()==='Continue ➡️');
        if(btnWrap && !slot.contains(btnWrap)){
             slot.appendChild(btnWrap);
             btnWrap.style.margin='0 auto';
             return true;
        }
        return false;
    }
    if(!move()) attempts.forEach(t=>setTimeout(move,t));
})();
</script>
""",
        unsafe_allow_html=True,
)
