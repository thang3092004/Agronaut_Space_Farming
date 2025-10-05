import streamlit as st
from logic.farm import ensure_farm_state, compute_rank

ensure_farm_state()
ss = st.session_state
rank = compute_rank(ss.xp)
owned = [v["label"] for k,v in ss.SHOP_ITEMS.items() if ss.equipment_owned.get(k)]
owned_text = ", ".join(owned) if owned else "(No equipment owned)"

st.title("Part 2 — Slide 09: Current Achievements")

st.markdown("""
<style>
.achv-wrap {max-width:900px; margin:0 auto; background:#1e1d33; padding:30px 38px 40px; border:1px solid #3e3c63; border-radius:24px; box-shadow:0 8px 28px rgba(0,0,0,.45);} 
.achv-grid {display:grid; grid-template-columns:repeat(auto-fit, minmax(180px,1fr)); gap:22px; margin-top:18px;} 
.achv-card {background:#272744; border:1px solid #454573; padding:14px 16px 18px; border-radius:18px; color:#e9e7ff; box-shadow:0 4px 14px rgba(0,0,0,.35);} 
.achv-card h3 {margin:0 0 8px; font-size:18px; color:#fff;} 
.rank-badge {display:inline-block; padding:10px 24px; font-size:40px; font-weight:700; background:linear-gradient(145deg,#ffcf4d,#ff9f1c); color:#2a1b00; border-radius:18px; box-shadow:0 6px 18px rgba(255,160,60,.3);} 
.equip-box {background:#22213a; border:1px solid #3d3c60; padding:12px 16px; border-radius:16px; margin-top:8px; font-size:14px; line-height:1.5; color:#ddd;} 
@media (max-width:640px){ .achv-wrap {padding:24px 22px 34px;} .rank-badge {font-size:34px;} }
</style>
<div class='achv-wrap'>
    <h2 style='margin-top:0;'>📊 Mission Summary</h2>
    <div class='achv-grid'>
        <div class='achv-card'>
            <h3>🌾 Harvested</h3>
            <div style='font-size:30px; font-weight:600;'>""" + str(ss.harvested_total) + """</div>
            <div style='font-size:12px; opacity:.75;'>Total food units harvested</div>
        </div>
        <div class='achv-card'>
            <h3>⭐ XP</h3>
            <div style='font-size:30px; font-weight:600;'>""" + str(ss.xp) + """</div>
            <div style='font-size:12px; opacity:.75;'>Accumulated experience</div>
        </div>
        <div class='achv-card'>
            <h3>💰 Credits</h3>
            <div style='font-size:30px; font-weight:600;'>""" + str(ss.money) + """</div>
            <div style='font-size:12px; opacity:.75;'>Current credits</div>
        </div>
        <div class='achv-card'>
            <h3>🎯 Rank</h3>
            <div class='rank-badge'>""" + rank + """</div>
            <div style='font-size:12px; opacity:.75; margin-top:6px;'>Based on XP</div>
        </div>
    </div>
    <div style='margin-top:28px;'>
    <h3 style='margin:0 0 8px;'>⚙️ Owned Equipment</h3>
        <div class='equip-box'>""" + owned_text + """</div>
    </div>
</div>
""", unsafe_allow_html=True)

nav = st.columns([1,1,1,1])
with nav[0]:
        if st.button("⬅️ Shop", use_container_width=True):
                st.switch_page("pages/2_🌱_Phần_2_Slide_08.py")
with nav[1]:
        if st.button("🏗 Farm", use_container_width=True):
                st.switch_page("pages/2_🌱_Phần_2_Slide_06.py")
with nav[2]:
    if st.button("📜 Rules", use_container_width=True):
                st.switch_page("pages/2_🌱_Phần_2_Slide_05.py")
with nav[3]:
    if st.button("🔁 Restart", use_container_width=True):
                from logic.farm import reset_game
                reset_game(); st.rerun()
