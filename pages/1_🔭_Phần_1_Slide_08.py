import streamlit as st

st.title("Part 1 — Slide 08: Low Habitability Warning")

st.markdown(
    """
### The planet you selected is predicted to have a low probability of supporting life.

Its metrics suggest extreme or unsuitable conditions. Consider going back and choosing another candidate with more balanced temperature, flux, period, and radius.
"""
)

try:
    st.image("assets/asset part 1/planets/planet_gray.png", width=220)
except Exception:
    pass

st.divider()

col = st.columns([1,1])
with col[0]:
    if st.button("⬅️ Back to Candidates"):
        st.switch_page("pages/1_🔭_Phần_1_Slide_07.py")
with col[1]:
    if st.button("Continue Anyway ➡️"):
        st.switch_page("pages/1_🔭_Phần_1_Slide_09.py")
