import streamlit as st
import numpy as np
from pathlib import Path
import pandas as pd
import random

# Configuration constants
HUNGER_FAIL_STREAK = 3  # number of consecutive zero‑hunger days that causes a loss

def _new_cell():
    return {"crop": None, "stage": 0, "water": 0.0, "health": 1.0, "ripe": False}

def ensure_farm_state():
    """Initialize persistent game state variables if not already present."""
    ss = st.session_state
    if ss.get("farm_grid") is None:
        ss.farm_grid = [[_new_cell() for _ in range(5)] for _ in range(5)]
        ss.selected = (0,0)
    ss.setdefault("chosen_crop", "HydroCorn")
    ss.setdefault("inventory", {"water": 10, "nutrient": 3, "pesticide": 2, "food": 0})
    # Seed inventory for each crop type (initial values)
    if "seed_inventory" not in ss:
        ss.seed_inventory = {"HydroCorn": 8, "EcoMoss": 10, "LuxiBerry": 6}
    ss.setdefault("seed_max", {"HydroCorn": 25, "EcoMoss": 30, "LuxiBerry": 20})
    ss.setdefault("money", 5)  # starting credits
    ss.setdefault("hunger_max", 200)
    ss.setdefault("hunger", 200)
    ss.setdefault("day", 1)
    ss.setdefault("xp", 0)
    ss.setdefault("harvested_total", 0)
    ss.setdefault("hunger_zero_streak", 0)
    ss.setdefault("game_over", False)
    ss.setdefault("game_over_reason", "")
    ss.setdefault("weather_today", {"temp": 25, "rain": 0.0, "drought": 0, "soil_moisture": 0.4})
    # Owned equipment flags
    ss.setdefault("equipment_owned", {"fertilizer_lab": False, "greenhouse": False, "soil_filter": False})
    # Crop metadata
    ss.setdefault("CROPS", {
        "HydroCorn": {"water_need": 2, "yield": 3, "price": 1, "grow_days": 4},
        "EcoMoss":   {"water_need": 1, "yield": 1, "price": 1, "grow_days": 3, "humidify": 0.2},
        "LuxiBerry": {"water_need": 2, "yield": 1, "price": 4, "grow_days": 5}
    })
    # Shop catalog (balanced costs)
    ss.setdefault("SHOP_ITEMS", {
        "fertilizer_lab": {"label": "Fertilizer Lab", "cost": 7, "desc": "Moderate boost to growth & small health recovery"},
        "greenhouse": {"label": "Greenhouse", "cost": 7, "desc": "Reduces drought & heat damage"},
        "soil_filter": {"label": "Soil Filter", "cost": 6, "desc": "Reduces moisture loss & soil decay"},
        "water_condensor": {"label": "Water Condensor", "cost": 6, "desc": "Generates +1 water every 2 days"}
    })
    # Forecast data cache
    ss.setdefault("forecast_cache", {})
    ss.setdefault("forecast_region", ss.get("forecast_region", None))

def render_grid():
    ss = st.session_state
    sel_i, sel_j = ss.selected
    # Map cell state to emoji for grid
    def cell_label(c):
        if not c["crop"]: return "🟪"
        if c.get("ripe"): return "🟩"
        if c["stage"]==0: return "🟦"
        if c["stage"]==1: return "🟨"
        return "🟧"
    # Inline CSS for grid scale (60%) and button sizing; remove custom yellow outline so default focus/red stays
    st.markdown("""
    <style>
      .grid-wrapper {width:60%; margin:0 auto 6px;}
      .grid-wrapper .stButton>button {font-size:30px; padding:4px 2px; line-height:1;}
      @media (max-width:900px){ .grid-wrapper {width:80%;} .grid-wrapper .stButton>button {font-size:26px;} }
      @media (max-width:600px){ .grid-wrapper {width:100%;} }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<div class='grid-wrapper'>", unsafe_allow_html=True)
    for i in range(5):
        row_cols = st.columns(5, gap="small")
        for j in range(5):
            c = ss.farm_grid[i][j]
            label = cell_label(c)
            btn_key = f"cell_{i}_{j}"
            with row_cols[j]:
                if st.button(label, key=btn_key):
                    ss.selected = (i,j)
    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Legend: 🟦 sprout • 🟨 juvenile • 🟧 mature • 🟩 ripe • 🟪 empty")
    i,j = ss.selected
    st.info(f"Selected cell: ({i+1},{j+1}) → {ss.farm_grid[i][j]}")

def sidebar_actions():
    # Resource / action sidebar
    st.subheader("🎒 Resources")
    col1, col2 = st.columns(2)
    with col1:
        try:
            st.image("assets/asset part 2/icons/icon_water.png", width=30)
        except:
            pass
    st.metric("💧 Water", st.session_state.inventory["water"])
    with col2:
        try:
            st.image("assets/asset part 2/icons/icon_fertilizer.png", width=30)
        except:
            pass
    st.metric("🧪 Nutrient", st.session_state.inventory["nutrient"])
    
    st.markdown('---')
    st.selectbox("Select crop", list(st.session_state.CROPS.keys()), key="chosen_crop")
    # Show seed counts
    seed_line = ", ".join([f"{k}:{st.session_state.seed_inventory.get(k,0)}/{st.session_state.seed_max.get(k,'?')}" for k in st.session_state.CROPS.keys()])
    st.caption(f"Seeds: {seed_line}")
    if st.button("🌱 Plant (selected cell)"):
        i,j = st.session_state.selected
        cell = st.session_state.farm_grid[i][j]
        crop = st.session_state.chosen_crop
        if st.session_state.seed_inventory.get(crop,0) <= 0:
            st.error("Out of seeds!")
        elif cell["crop"]:
            st.warning("Cell already occupied.")
        else:
            cell.update(_new_cell())
            cell["crop"] = crop
            st.session_state.seed_inventory[crop] -= 1
            st.toast("Planted (seed -1)")

    if st.button("💧 Water (cost 1)"):
        if st.session_state.inventory["water"]>0:
            i,j = st.session_state.selected
            cell = st.session_state.farm_grid[i][j]
            cell["water"] += 1.0
            st.session_state.inventory["water"] -= 1
            st.toast("Watered")
        else:
            st.error("Out of water!")

    if st.button("🧪 Fertilize"):
        if st.session_state.inventory["nutrient"]>0:
            i,j = st.session_state.selected
            cell = st.session_state.farm_grid[i][j]
            cell["health"] = float(min(1.0, cell["health"]+0.2))
            st.session_state.inventory["nutrient"] -= 1
            st.toast("Health boosted")
        else:
            st.error("No nutrients left!")

    if st.button("🧺 Harvest (if ripe)"):
        i,j = st.session_state.selected
        cell = st.session_state.farm_grid[i][j]
        if cell.get("ripe"):
            crop = cell["crop"]
            gain = st.session_state.CROPS[crop]["yield"]
            st.session_state.inventory["food"] = st.session_state.inventory.get("food",0)+gain
            st.session_state.harvested_total += gain
            cell.update(_new_cell())
            st.toast(f"Harvested {gain} units")
            # XP for harvesting ripe crops (small)
            st.session_state.xp += 1
            # Seed return chance (K) differing by crop
            import random as _r
            base_min, base_max = 0,0
            if crop == "EcoMoss":
                base_min, base_max = 1,2
            elif crop == "HydroCorn":
                base_min, base_max = 0,2
            else: # LuxiBerry rarer seeds
                base_min, base_max = 0,1
            raw_return = _r.randint(base_min, base_max)
            if raw_return>0:
                cap = st.session_state.seed_max.get(crop, 9999)
                current = st.session_state.seed_inventory.get(crop,0)
                addable = max(0, cap - current)
                gained = min(raw_return, addable)
                if gained>0:
                    st.session_state.seed_inventory[crop] = current + gained
                    st.info(f"+{gained} {crop} seed(s){' (cap reached)' if current+gained>=cap else ''}")
                else:
                    st.warning("Seed storage full (no gain)")
        else:
            st.warning("Not ripe.")

    st.markdown('---')
    if st.button("🍽️ Eat 1 (+15 hunger)"):
        food = st.session_state.inventory.get("food",0)
        if food>0:
            st.session_state.inventory["food"] = food-1
            st.session_state.hunger = min(100, st.session_state.hunger+15)
            st.toast("Hunger restored")
        else:
            st.error("No food available.")

    if st.button("💸 Sell 1 (gain price)"):
        food = st.session_state.inventory.get("food",0)
        if food>0:
            st.session_state.inventory["food"] = food-1
            price = st.session_state.CROPS[st.session_state.chosen_crop]["price"]
            st.session_state.money += price
            st.toast(f"+{price} credits")
            st.session_state.xp += 2  # selling gives XP
        else:
            st.error("Nothing to sell.")

    st.markdown('---')
    st.metric("⭐ XP", st.session_state.xp)
    # Resource purchase (A) simple shop inline
    st.markdown("**Buy resources**")
    b1,b2,b3 = st.columns(3)
    with b1:
        if st.button("+5 water (2💰)"):
            if st.session_state.money>=2:
                st.session_state.money-=2
                st.session_state.inventory["water"] +=5
            else: st.error("Not enough credits")
    with b2:
        if st.button("+2 nutrient (3💰)"):
            if st.session_state.money>=3:
                st.session_state.money-=3
                st.session_state.inventory["nutrient"] +=2
            else: st.error("Not enough credits")
    with b3:
        if st.button("+3 random seeds (4💰)"):
            if st.session_state.money>=4:
                import random as _r
                st.session_state.money-=4
                pick = _r.choice(list(st.session_state.CROPS.keys()))
                cap = st.session_state.seed_max.get(pick, 9999)
                cur = st.session_state.seed_inventory.get(pick,0)
                addable = max(0, cap-cur)
                gain = min(3, addable)
                if gain>0:
                    st.session_state.seed_inventory[pick] = cur + gain
                    st.success(f"+{gain} {pick} seed(s){' (cap reached)' if cur+gain>=cap else ''}")
                else:
                    st.warning("Seed storage for this type full")
            else: st.error("Not enough credits")

def _weather_step():
    sim = st.session_state.get("weather_sim", None)
    if sim is None:
        st.session_state.weather_today = {"temp": 25, "rain": 0.0, "drought": 0, "soil_moisture": 0.4}
        return
    st.session_state.weather_today = sim.step()

def _tick_cell(cell):
    if not cell["crop"]: return
    meta = st.session_state.CROPS[cell["crop"]]
    wt = st.session_state.weather_today
    rain = wt["rain"]
    temp = wt["temp"]
    drought = wt["drought"]
    soil_moisture = wt.get("soil_moisture", 0.4)

    humidify = meta.get("humidify", 0.0)
    # Equipment modifiers
    eq = st.session_state.equipment_owned
    # Rebalanced bonuses (nerf fertilizer lab, slight buff synergy overall)
    growth_bonus = 0.0        # additive to stage per day
    health_recover = 0.0      # passive health regen each tick
    drought_protect = 0.0     # subtract from drought damage
    moisture_stabilize = 0.0  # percentage reduction factor of water loss
    if eq.get("fertilizer_lab"):
        growth_bonus = 0.25
        health_recover = 0.03
    if eq.get("greenhouse"):
        drought_protect = 0.12  # buff effect (C)
    if eq.get("soil_filter"):
        moisture_stabilize = 0.10
    # Water condensor passive (G) handled in next_day

    evap = max(0, (temp-26))*0.05
    base_loss = meta["water_need"]*0.7 + evap
    cell["water"] += rain + humidify + (soil_moisture-0.4)*0.5
    cell["water"] -= base_loss * (1 - moisture_stabilize)

    if cell["water"] < 0:
        cell["health"] -= 0.2 * (1 - health_recover)
        cell["water"] = 0.0
    else:
        # passive small health recovery if lab
        if health_recover>0:
            cell["health"] = float(min(1.0, cell["health"] + health_recover))

    # Growth progression
    if cell["health"] > 0.6:
        cell["stage"] += 1 + growth_bonus

    if cell["stage"] >= meta["grow_days"]:
        cell["ripe"] = True

    if drought >= 1:
        # drought damage reduced by greenhouse
        cell["health"] -= max(0.0, 0.1 - drought_protect)

    cell["health"] = float(np.clip(cell["health"], 0.0, 1.0))

def _load_forecast_row():
    """Pick a random forecast row for the configured region and update weather_today."""
    region = st.session_state.get("forecast_region")
    if not region:
        return
    path = Path(f"data/interpolated/{region}_2026_Forecast.csv")
    if not path.exists():
        return
    try:
        df = st.session_state.forecast_cache.get(region)
        if df is None:
            df = pd.read_csv(path)
            st.session_state.forecast_cache[region] = df
        if df.empty:
            return
        row = df.sample(1, random_state=random.randint(0, 999999)).iloc[0]
        # Attempt to map columns
        def find(col_keywords):
            for c in df.columns:
                lower = c.lower()
                if any(k in lower for k in col_keywords):
                    return row[c]
            return None
        soil = find(["soil","moist"])
        rain = find(["rain","precip"]) or 0.0
        temp = find(["temp"]) or 25
        drought = find(["drought","dry"]) or 0
        st.session_state.weather_today = {
            "temp": float(temp) if isinstance(temp,(int,float)) else 25,
            "rain": float(rain) if isinstance(rain,(int,float)) else 0.0,
            "drought": int(drought) if isinstance(drought,(int,float)) else 0,
            "soil_moisture": float(soil) if isinstance(soil,(int,float)) else 0.4
        }
    except Exception:
        pass

def next_day():
    if st.session_state.get("game_over"):
        return
    # Pull new forecast-based weather
    _load_forecast_row()
    for i in range(5):
        for j in range(5):
            _tick_cell(st.session_state.farm_grid[i][j])
    # Hunger decay
        st.session_state.hunger = max(0, st.session_state.hunger - 8)
    # Rain to water conversion (B) - if rain high add inventory water
    rain_amount = st.session_state.weather_today.get("rain",0)
    if rain_amount >= 0.6:
        st.session_state.inventory["water"] += 1
    # Equipment passive water generation (G)
    if st.session_state.equipment_owned.get("water_condensor") and st.session_state.day % 2 == 0:
        st.session_state.inventory["water"] += 1
    # Track consecutive zero-hunger days
    if st.session_state.hunger == 0:
        st.session_state.hunger_zero_streak += 1
    else:
        st.session_state.hunger_zero_streak = 0
    if st.session_state.hunger_zero_streak >= HUNGER_FAIL_STREAK:
        st.session_state.game_over = True
        st.session_state.game_over_reason = f"Hunger at 0 for {st.session_state.hunger_zero_streak} consecutive days"
    st.session_state.day += 1

def purchase_equipment(key: str):
    """Attempt to purchase equipment item and apply XP bonus."""
    items = st.session_state.SHOP_ITEMS
    owned = st.session_state.equipment_owned
    if key not in items or owned.get(key):
        return
    cost = items[key]["cost"]
    if st.session_state.money < cost:
        st.warning("Not enough credits")
        return
    st.session_state.money -= cost
    owned[key] = True
    st.session_state.xp += 5  # big XP bonus per rules
    st.toast(f"Purchased {items[key]['label']} (+XP)")

def reset_game():
    """Reset core gameplay state after game over or manual restart."""
    to_del = [
        "farm_grid","selected","inventory","money","hunger","day","xp",
        "hunger_zero_streak","game_over","game_over_reason","equipment_owned"
    ]
    for k in to_del:
        if k in st.session_state:
            del st.session_state[k]
    ensure_farm_state()

def compute_rank(xp: int) -> str:
    if xp >= 80: return "S"
    if xp >= 55: return "A"
    if xp >= 35: return "B"
    if xp >= 15: return "C"
    return "D"
