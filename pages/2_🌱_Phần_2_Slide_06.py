import streamlit as st
"""SLIDE 06 REBUILD — Core Gameplay Screen
Features implemented fresh per rules: Planting, Water/Nutrients, Growth, Harvest/Trade, Hunger, Weather snapshot, XP, Equipment status, Loss condition.
"""

import streamlit as st
from logic.farm import ensure_farm_state, next_day, purchase_equipment, reset_game

ensure_farm_state()

# ---- Layout & Style ----
st.markdown(
    """
    <style>
      .top-bar {display:flex; flex-wrap:wrap; gap:14px; align-items:center; margin-bottom:10px;}
      .badge {background:#21213a; padding:6px 14px; border-radius:30px; color:#ecebff; font-size:14px; border:1px solid #3f3f68; box-shadow:0 2px 4px rgba(20,20,40,.4) inset;}
      .badge.critical {background:#4a1220; border-color:#ff5470; color:#ffd6df;}
      .main-grid-wrap {display:grid; grid-template-columns: minmax(460px, 1fr) 300px; gap:26px;}
      @media (max-width:1150px){ .main-grid-wrap {grid-template-columns:1fr;} }
      .panel {background:#1e1d33; border:1px solid #3e3c63; border-radius:18px; padding:18px 20px 24px; box-shadow:0 4px 14px rgba(0,0,0,.35);}
      .panel h3 {margin:0 0 10px; font-size:20px; color:#dcd7ff;}
      .res-grid {display:grid; grid-template-columns:repeat(3,1fr); gap:10px 14px; margin-bottom:10px;}
      .res-item {background:#272744; border:1px solid #454573; border-radius:12px; padding:6px 10px; font-size:13px; line-height:1.35; color:#eee;}
      .grid-board {width:100%; margin:4px auto 10px; display:grid; grid-template-columns:repeat(5, 1fr); gap:8px; max-width:480px;}
      .grid-board button {width:100%; aspect-ratio:1/1; font-size:30px; line-height:1; padding:0;}
      @media (max-width:760px){ .grid-board {gap:6px;} .grid-board button {font-size:26px;} }
    /* (Old selected-cell-wrapper removed: replaced by .cell-highlight without glow) */
      .equip-list {display:flex; flex-direction:column; gap:6px; margin:6px 0 14px;}
      .equip-item {background:#24243e; border:1px solid #41406a; padding:8px 10px; border-radius:10px; font-size:13px; color:#ddd; display:flex; justify-content:space-between; align-items:center;}
      .equip-item.owned {border-color:#4caf50; box-shadow:0 0 6px rgba(76,175,80,.5);}
      .actions-grid {display:grid; grid-template-columns:repeat(auto-fill,minmax(120px,1fr)); gap:8px 10px; margin-top:4px;}
      .loss-banner {background:#4a1220; border:1px solid #ff5470; padding:14px 16px; border-radius:14px; color:#ffd8e0; margin-top:14px; text-align:center;}
      .note {font-size:12.5px; color:#aaa; margin-top:6px;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---- Helper: draw grid with red highlight ----
def draw_grid():
    ss = st.session_state
    sel_i, sel_j = ss.selected
    # CSS for square 5x5 layout
    st.markdown("""
        <style>
      .grid-wrapper-5x5 {max-width:520px; margin:0 auto 10px;}
      .grid-wrapper-5x5 .stButton>button {width:100%; aspect-ratio:1/1; font-size:30px; padding:0; line-height:1; border-radius:14px;}
      @media (max-width:820px){ .grid-wrapper-5x5 {max-width:420px;} .grid-wrapper-5x5 .stButton>button {font-size:26px;} }
      @media (max-width:600px){ .grid-wrapper-5x5 {max-width:100%;} }
      .cell-highlight {margin-top:-62px; height:0; pointer-events:none; display:flex; justify-content:center;}
            .cell-highlight > div {position:absolute; width:56px; height:56px; border:3px solid #ff3d3d; border-radius:16px;} 
      @media (max-width:820px){ .cell-highlight > div {width:48px; height:48px;} }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="grid-wrapper-5x5">', unsafe_allow_html=True)
    for i in range(5):
        row = st.columns(5, gap="small")
        for j in range(5):
            cell = ss.farm_grid[i][j]
            if not cell["crop"]:
                emoji = "🟪"
            else:
                if cell.get("ripe"): emoji = "🟩"
                elif cell["stage"]==0: emoji = "🟦"
                elif cell["stage"]==1: emoji = "🟨"
                else: emoji = "🟧"
            with row[j]:
                if st.button(emoji, key=f"cell_{i}_{j}"):
                    ss.selected = (i,j)
                if (i,j)==(sel_i,sel_j):
                    # highlight overlay
                    st.markdown("<div class='cell-highlight'><div></div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Legend: 🟦 sprout • 🟨 juvenile • 🟧 mature • 🟩 ripe • 🟪 empty")
    si, sj = ss.selected
    cell = ss.farm_grid[si][sj]
    st.write(f"Selected: ({si+1},{sj+1}) | crop={cell['crop']} | stage={cell['stage']:.1f} | water={cell['water']:.2f} | health={cell['health']:.2f} | ripe={cell['ripe']}")

# ---- Top status bar ----
ss = st.session_state
hun_streak = ss.get("hunger_zero_streak",0)
with st.container():
    top_cols = st.columns([1,3,1])
    with top_cols[0]:
        st.markdown(f"<div class='badge'>Day: <b>{ss.day}</b></div>", unsafe_allow_html=True)
    with top_cols[1]:
        st.markdown(
            f"""
            <div class='top-bar'>
              <div class='badge'>💧 {ss.inventory.get('water',0)}</div>
              <div class='badge'>🍎 {ss.inventory.get('food',0)}</div>
              <div class='badge'>💰 {ss.money}</div>
              <div class='badge'>⭐ {ss.xp}</div>
              <div class='badge {'critical' if ss.hunger==0 else ''}'>🍽️ {ss.hunger}/{ss.hunger_max}</div>
              <div class='badge'>🌵 Drought: {ss.weather_today.get('drought',0)}</div>
              <div class='badge'>🌡️ {ss.weather_today.get('temp','?')}°C</div>
              <div class='badge'>🌧️ {ss.weather_today.get('rain','?')}</div>
              <div class='badge'>🟫 Soil {ss.weather_today.get('soil_moisture','?')}</div>
            </div>
            """, unsafe_allow_html=True
        )
    with top_cols[2]:
        if st.button("📜 Rules", use_container_width=True):
            st.switch_page("pages/2_🌱_Phần_2_Slide_05.py")

st.divider()

col_main, col_side = st.columns([1.2,0.8], gap="large")

with col_main:
    st.subheader("Farm Plot")
    draw_grid()
    # Day progression / Game over controls
    if ss.get("game_over"):
        st.error(f"GAME OVER: {ss.game_over_reason}")
        cgo = st.columns([1,1,1])
        with cgo[1]:
            if st.button("🔄 Restart", type="primary"):
                reset_game(); st.rerun()
    else:
        nxt_cols = st.columns([1,1,1])
        with nxt_cols[0]:
            if st.button("➡️ Next Day", use_container_width=True):
                next_day()
        with nxt_cols[1]:
            if st.button("🛒 Shop", use_container_width=True):
                st.switch_page("pages/2_🌱_Phần_2_Slide_08.py")
        with nxt_cols[2]:
            if st.button("📊 Achievements", use_container_width=True):
                st.switch_page("pages/2_🌱_Phần_2_Slide_09.py")
        # Hunger progress bar
        st.progress(min(1.0, ss.hunger/ss.hunger_max))
    if hun_streak>0 and not ss.get("game_over"):
        st.info(f"⚠️ Hunger 0 for {hun_streak} consecutive day(s) (>=3 = loss)")

with col_side:
    st.subheader("Resources & Actions")
    # Planting controls
    st.selectbox("Select crop", list(ss.CROPS.keys()), key="chosen_crop")
    if st.button("🌱 Plant", use_container_width=True):
        si,sj = ss.selected
        cell = ss.farm_grid[si][sj]
        if not cell["crop"]:
            from logic.farm import _new_cell  # internal helper
            cell.update(_new_cell())
            cell["crop"] = ss.chosen_crop
            st.success("Planted!")
        else:
            st.warning("Cell occupied")
    a1,a2 = st.columns(2)
    with a1:
        if st.button("💧 Water", use_container_width=True):
            if ss.inventory["water"]>0:
                si,sj=ss.selected; ss.farm_grid[si][sj]["water"] +=1; ss.inventory["water"]-=1; st.toast("Watered")
            else: st.error("Out of water")
    with a2:
        if st.button("🧪 Fertilize", use_container_width=True):
            if ss.inventory["nutrient"]>0:
                si,sj=ss.selected; ss.farm_grid[si][sj]["health"] = float(min(1.0, ss.farm_grid[si][sj]["health"]+0.2)); ss.inventory["nutrient"]-=1; st.toast("Fertilized")
            else: st.error("No nutrients")
    a3,a4 = st.columns(2)
    with a3:
        if st.button("🧺 Harvest", use_container_width=True):
            si,sj=ss.selected; c=ss.farm_grid[si][sj]
            if c.get("ripe"):
                gain = ss.CROPS[c["crop"]]["yield"]; ss.inventory["food"]+=gain; from logic.farm import _new_cell; c.update(_new_cell()); ss.xp+=1; st.success(f"+{gain} food")
            else: st.warning("Not ripe")
    with a4:
        if st.button("💸 Sell 1", use_container_width=True):
            if ss.inventory.get("food",0)>0:
                ss.inventory["food"]-=1; price=ss.CROPS[ss.chosen_crop]["price"]; ss.money+=price; ss.xp+=2; st.success(f"+{price} credits")
            else: st.error("No food to sell")
    a5,a6 = st.columns(2)
    with a5:
        if st.button("🍽️ Eat 1 (+25)", use_container_width=True):
            if ss.inventory.get("food",0)>0:
                ss.inventory["food"] -= 1
                cap = ss.get("hunger_max", 200)
                before = ss.hunger
                ss.hunger = min(cap, ss.hunger + 25)
                gained = ss.hunger - before
                st.success(f"Ate (+{gained} hunger)")
            else:
                st.error("No food")
    with a6:
        st.metric("XP", ss.xp)

    st.markdown("---")
    st.caption("Owned Equipment")
    for k,v in ss.SHOP_ITEMS.items():
        owned = ss.equipment_owned.get(k)
        st.markdown(f"{'✅' if owned else '⬜'} {v['label']}")

    st.markdown("---")
    st.caption("Objective: maintain production & survive to cycle end.")

st.divider()
st.caption("Slide 06 features: Planting • Water/Nutrients • Growth • Harvest/Trading • Shop Effects • Hunger • Weather • XP")
