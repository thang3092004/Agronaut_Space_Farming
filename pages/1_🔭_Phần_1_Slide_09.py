import streamlit as st

st.title("Part 1 — Slide 09: Successful Candidate")

st.markdown(
    """
### Congratulations! 🎉
You have identified a planet with strong indicators for potential habitability.

The metrics (temperature, stellar flux, orbital period, and radius) align with ranges typical of temperate, rocky worlds.
"""
)

try:
    st.image("assets/asset part 1/planets/planet_green.png", width=220)
except Exception:
    pass

st.divider()

col = st.columns([1,1])
with col[0]:
    if st.button("⬅️ Back"):
        st.switch_page("pages/1_🔭_Phần_1_Slide_07.py")
with col[1]:
    if st.button("Continue ➡️"):
        st.switch_page("pages/1_🔭_Phần_1_Slide_10.py")
