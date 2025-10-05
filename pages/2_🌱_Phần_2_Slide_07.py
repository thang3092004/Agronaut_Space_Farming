import streamlit as st
import altair as alt
import pandas as pd
from logic.data import load_exoplanets_demo
from logic.exo import mark_candidates, regression_predict
from logic.farm import ensure_farm_state, render_grid, sidebar_actions, next_day
from logic.weather import ensure_weather_profile_ui

st.title("Phần 2 — Slide 07: Hoàn tất chu kỳ 10 ngày")

# Hiển thị hiệu ứng dữ liệu và thu hoạch
col1, col2 = st.columns(2)
with col1:
    try:
        st.image("assets/asset part 2/effects/data_glow.png", width=200)
        st.caption("Dữ liệu thu thập")
    except:
        st.caption("📊 Dữ liệu thu thập")
with col2:
    try:
        st.image("assets/asset part 2/icons/icon_xp.png", width=100)
        st.caption("Kinh nghiệm tích lũy")
    except:
        st.caption("⭐ Kinh nghiệm tích lũy")

st.markdown("""Nếu thành công: thu hoạch, tiền/exp; Nếu thất bại: cây héo.""")


if st.button("⬅️ Quay lại"): st.switch_page("pages/2_🌱_Phần_2_Slide_06.py")
if st.button("Tiếp tục ➡️"): st.switch_page("pages/2_🌱_Phần_2_Slide_08.py")
