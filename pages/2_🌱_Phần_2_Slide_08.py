import streamlit as st
from pathlib import Path
import base64
from logic.farm import ensure_farm_state, purchase_equipment
from typing import Callable

st.title("Part 2 — Slide 08: 🛒 Shop & Equipment")

ensure_farm_state()

# Defensive: if farm.py was reverted and seed inventories missing, initialize here
if 'seed_inventory' not in st.session_state:
    st.session_state.seed_inventory = {k: 5 for k in st.session_state.CROPS.keys()}
if 'seed_max' not in st.session_state:
    st.session_state.seed_max = {k: 25 for k in st.session_state.CROPS.keys()}

def _b64(p:str)->str:
    path = Path(p)
    if not path.exists(): return ""
    return base64.b64encode(path.read_bytes()).decode()

shop_imgs = {
    'fertilizer_lab': 'assets/asset part 2/shop/fertilizer_lab.png',
    'greenhouse': 'assets/asset part 2/shop/greenhouse.png',  # will auto swap to greenhouse_new.png if present
    'soil_filter': 'assets/asset part 2/shop/soil_filter.png',
    'water_condensor': 'assets/asset part 2/shop/water_condensor.png'
}

def show_image(col, img_path:str):
    """Display image (old/new Streamlit compatible). Prefer greenhouse_new.png if available."""
    if not img_path:
        return
    p = Path(img_path)
    if 'greenhouse.png' in img_path:
        # Kiểm tra ảnh mới
        new_p = Path(img_path.replace('greenhouse.png', 'greenhouse_new.png'))
        if new_p.exists():
            p = new_p
    if not p.exists():
        return
    try:
    # Try new API first (future-proof)
        col.image(str(p), use_container_width=True)  # type: ignore[arg-type]
    except TypeError:
    # Fallback to legacy param
        col.image(str(p), use_column_width=True)

st.markdown(f"**Credits:** {st.session_state.money} | ⭐ XP: {st.session_state.xp}")

items = st.session_state.SHOP_ITEMS
owned = st.session_state.equipment_owned

# Display items dynamically in rows of 3
keys = list(items.keys())
for i in range(0, len(keys), 3):
    row = st.columns(3)
    for key, col in zip(keys[i:i+3], row):
        data = items[key]
        with col:
            img = shop_imgs.get(key)
            if img:
                show_image(col, img)
            col.markdown(f"### {data['label']}")
            col.caption(data['desc'])
            if owned.get(key):
                col.success("OWNED ✔")
            else:
                disabled = st.session_state.money < data['cost']
                if col.button(f"Buy ({data['cost']})", key=f"buy_{key}", disabled=disabled):
                    purchase_equipment(key)

st.markdown("---")
st.subheader("Quick Buy (resources / seeds)")
q1,q2,q3 = st.columns(3)
with q1:
    if st.button("+5 water (2💰)"):
        if st.session_state.money>=2:
            st.session_state.money-=2; st.session_state.inventory["water"]+=5
    else: st.error("Not enough credits")
with q2:
    if st.button("+2 nutrient (3💰)"):
        if st.session_state.money>=3:
            st.session_state.money-=3; st.session_state.inventory["nutrient"]+=2
    else: st.error("Not enough credits")
with q3:
    if st.button("+3 random seeds (4💰)"):
        import random as _r
        if st.session_state.money>=4:
            st.session_state.money-=4; pick=_r.choice(list(st.session_state.CROPS.keys())); st.session_state.seed_inventory[pick]+=3; st.success(f"+3 seed {pick}")
    else: st.error("Not enough credits")
st.caption("Seeds: " + ", ".join([f"{k}:{st.session_state.seed_inventory.get(k,0)}/{st.session_state.seed_max.get(k,'?')}" for k in st.session_state.CROPS.keys()]))

st.markdown("---")
col_nav = st.columns([1,1,1,1])
with col_nav[0]:
    if st.button("⬅️ Farm", use_container_width=True):
        st.switch_page("pages/2_🌱_Phần_2_Slide_06.py")
with col_nav[1]:
    # 'Mua xong' now returns to farm instead of just rerun (fix broken behavior)
    if st.button("✅ Done", use_container_width=True):
        st.switch_page("pages/2_🌱_Phần_2_Slide_06.py")
with col_nav[2]:
    if st.button("📊 Achievements", use_container_width=True):
        st.switch_page("pages/2_🌱_Phần_2_Slide_09.py")
with col_nav[3]:
    if st.button("📜 Rules", use_container_width=True):
        st.switch_page("pages/2_🌱_Phần_2_Slide_05.py")

# Optional hint if user hasn't purchased anything and clicks reload / revisit
if not any(owned.values()):
    st.info("No equipment owned yet – each item grants passive advantages (growth, drought protection, moisture retention).")
