import streamlit as st
from pathlib import Path
import base64

st.title("Part 2 — Slide 05: Rules")

def _b64(p: str) -> str:
    path = Path(p)
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode()

bg_b64 = _b64("assets/asset part 2/background/planet_surface.png")

RAW_RULES_TEXT = """⚙️ Rules

1🌱 Planting
You can sow a seed in any empty cell. Each crop type has distinct growth rate, water demand, and yield.

2💧 Water & Nutrients
Maintain moisture and health levels for all planted cells.
🌧️ Rain replenishes soil moisture.
🔥 Heat and 🌵 Drought cause rapid evaporation and soil degradation.
When moisture or health reaches zero, the crop withers.

3🌿 Growth
Each day, healthy crops advance one stage.
Low moisture or drought conditions slow or stop growth.
Fully grown crops become ripe and can be harvested.

4🧺 Harvesting & Trading
Harvesting a ripe crop yields food units.
You can trade crops with Earth to earn credits (money).
Some crops may also provide bonus resources or income.
Harvested cells become empty and can be replanted.

5🏪 Shop & Equipment
Use your credits to buy advanced equipment in the Shop:

🧪 Fertilizer Lab — boosts growth speed and crop health recovery.

🌱 Greenhouse — protects crops from drought and heat damage.

⚙️ Soil Filter — stabilizes moisture levels and prevents soil decay.

Purchased items are marked with a check symbol in the shop panel and remain active for the rest of the cycle.

6🍽️ Hunger & Survival
Your colony’s hunger decreases each day.
Eating food restores hunger.
If hunger remains at zero for too long, the mission fails.

7🌦️ Weather System

🌧️ Rain: increases soil moisture and supports growth.

🔥 Heat: accelerates evaporation and increases crop stress.

🌵 Drought: persistent dry periods drastically reduce moisture gain and slow recovery.

✨ Special Traits: certain plants (e.g., EcoMoss) humidify nearby tiles and reduce drought impact.

8⭐ Experience (XP)
Earn XP as your colony progresses:

🌾 Gain XP from selling crops to Earth.

🏗️ Gain a large XP bonus when purchasing equipment from the shop.
Your total XP represents your mission rank and success level — the higher your XP, the closer you are to becoming a Master Colonist.

9🎯 Objective
Survive until the end of the cycle by maintaining stable food production, resource sustainability, and technological upgrades.
Optimize your crop selection, irrigation timing, and equipment investment to endure harsh weather and secure your colony’s future."""

rules_html = f"""
<style>
.rules-stage {{position:relative; width:100%; max-width:1200px; margin:0 auto;}}
.rules-stage img.bg {{width:100%; border-radius:10px; box-shadow:0 0 18px rgba(120,60,200,.45); filter:brightness(.97);}}
.rules-box {{position:absolute; top:54%; left:50%; transform:translate(-50%,-50%); width:min(940px,90%); max-height:500px; overflow:auto; padding:38px 44px 46px; background:linear-gradient(135deg, rgba(28,16,64,.62), rgba(54,26,96,.55)); backdrop-filter:blur(7px); border:1px solid rgba(160,120,255,.42); border-radius:28px; color:#f4efff; font-size:15.8px; line-height:1.62; letter-spacing:.25px; box-shadow:0 0 22px rgba(130,80,240,.45), 0 0 55px rgba(70,30,140,.35) inset;}}
.rules-box pre {{margin:0; white-space:pre-wrap; font-family:inherit; font-size:inherit; line-height:inherit;}}
.rules-box pre b {{color:#fff;}}
.rules-box::-webkit-scrollbar {{width:10px;}}
.rules-box::-webkit-scrollbar-thumb {{background:linear-gradient(180deg,#a77bff,#6d41c9); border-radius:10px;}}
.rules-box::-webkit-scrollbar-track {{background:rgba(255,255,255,.08); border-radius:10px;}}
@media (max-width:980px) {{ .rules-box {{top:58%; max-height:470px; padding:32px 34px 40px; font-size:15px;}} }}
@media (max-width:640px) {{ .rules-box {{top:60%; max-height:430px; padding:26px 26px 34px; font-size:14px; border-radius:22px;}} }}
</style>
<div class='rules-stage'>
  {f"<img class='bg' src='data:image/png;base64,{bg_b64}' alt='surface background' />" if bg_b64 else '<div style=\"padding:60px;text-align:center;color:#ccc;border:1px dashed #666;\">(Missing planet_surface.png)</div>'}
  <div class='rules-box'>
    <pre>{RAW_RULES_TEXT}</pre>
  </div>
</div>
"""

st.markdown(rules_html, unsafe_allow_html=True)

nav = st.columns([1,1])
with nav[0]:
    if st.button("⬅️ Back"):
        st.switch_page("pages/2_🌱_Phần_2_Slide_04.py")
with nav[1]:
    if st.button("Continue ➡️"):
        st.switch_page("pages/2_🌱_Phần_2_Slide_06.py")
