import streamlit as st
import numpy as np

def _rand_weights(rng, k):
    w = rng.random(k)
    w /= w.sum()
    return w.tolist()

def default_random_profiles(seed=1234):
    rng = np.random.default_rng(seed)
    def make_profile(temp_base):
        rain_levels = np.round(np.sort(rng.uniform(0, 3.0, 4)), 2).tolist()
        rain_probs = _rand_weights(rng, len(rain_levels))
        states = [0,1,2]
        T = []
        for _ in states:
            row = rng.random(len(states))
            row /= row.sum()
            T.append(row.tolist())
        rain_relief = [0.0, -float(rng.uniform(0.1,0.4)), -float(rng.uniform(0.2,0.5))]
        metric_w = _rand_weights(rng, 4)  # soil_moisture, rainfall, temperature, drought (for reference)
        return {
            "seed": int(rng.integers(1, 10_000)),
            "metrics_weight": {
                "soil_moisture": metric_w[0],
                "rainfall": metric_w[1],
                "temperature": metric_w[2],
                "drought": metric_w[3]
            },
            "temp": {"base": temp_base, "daily_sigma": float(rng.uniform(3,6)), "ar1": float(rng.uniform(0.4,0.8))},
            "rain": {"levels": rain_levels, "probs": rain_probs},
            "drought": {"states": states, "transition": T, "rain_relief": rain_relief}
        }
    return {"iowa": make_profile(23), "texas": make_profile(28)}

class WeatherSim:
    def __init__(self, profile: dict):
        self.profile = profile
        self.rng = np.random.default_rng(profile.get("seed", 7))
        self.temp_cfg = profile["temp"]
        self.rain_cfg = profile["rain"]
        self.dr_cfg = profile["drought"]
        self.metrics_w = profile.get("metrics_weight", {
            "soil_moisture": 0.25, "rainfall": 0.25, "temperature": 0.25, "drought": 0.25
        })
        self.temp = self.temp_cfg["base"]
        self.dr_state = 0
        self.soil_m = 0.4
        self._last_noise = 0.0

    def step(self):
        levels = np.array(self.rain_cfg["levels"], dtype=float)
        probs  = np.array(self.rain_cfg["probs"], dtype=float); probs /= probs.sum()
        rain = float(self.rng.choice(levels, p=probs))

        trans = np.array(self.dr_cfg["transition"], dtype=float)
        relief = np.array(self.dr_cfg.get("rain_relief", [0.0]*len(self.dr_cfg["states"])))
        row = trans[self.dr_state].copy()
        row[0] += max(0.0, min(0.5, rain * -relief[self.dr_state]))
        row = np.clip(row, 0, None)
        row = row / row.sum()
        self.dr_state = int(self.rng.choice(len(row), p=row))

        ar1 = float(self.temp_cfg.get("ar1", 0.5))
        sigma = float(self.temp_cfg.get("daily_sigma", 4))
        shock = float(self.rng.normal(0, sigma))
        self._last_noise = ar1 * self._last_noise + (1 - ar1) * shock

        drought_heat = 1.5 * self.dr_state
        rain_cool    = 0.3 * rain
        temp = float(self.temp_cfg["base"] + self._last_noise + drought_heat - rain_cool)

        self.soil_m += 0.15*rain - 0.05*max(0, temp-26) * 0.05 - 0.05*self.dr_state
        self.soil_m = float(np.clip(self.soil_m, 0.0, 1.0))
        self.temp = temp

        return {
            "temp": round(self.temp,1),
            "rain": round(rain,2),
            "drought": self.dr_state,
            "soil_moisture": round(self.soil_m,2),
            "weights": self.metrics_w
        }

def ensure_weather_profile_ui():
    st.subheader("🌦️ Khí hậu giả lập (random weights)")
    
    # Hiển thị icon thời tiết
    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            st.image("assets/asset part 2/effects/rain.png", width=80)
            st.caption("Mưa")
        except:
            st.caption("🌧️ Mưa")
    with col2:
        try:
            st.image("assets/asset part 2/effects/heatwave.png", width=80)
            st.caption("Sóng nhiệt")
        except:
            st.caption("🌡️ Sóng nhiệt")
    with col3:
        try:
            st.image("assets/asset part 2/effects/dust.png", width=80)
            st.caption("Bão bụi")
        except:
            st.caption("💨 Bão bụi")
    
    if "weather_profiles" not in st.session_state:
        st.session_state.weather_profiles = default_random_profiles()
    profiles = list(st.session_state.weather_profiles.keys())
    choice = st.selectbox("Chọn tiểu vùng", profiles, index=0, key="climate_choice")
    if st.button("Áp dụng profile"):
        prof = st.session_state.weather_profiles[choice]
        st.session_state.weather_sim = WeatherSim(prof)
        st.toast(f"Đã áp dụng profile: {choice}")
