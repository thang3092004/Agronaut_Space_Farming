import streamlit as st
from logic.difficulty import set_difficulty, get_difficulty, debug_difficulty_info

st.title("Part 2 — Slide 00: Select Difficulty")

st.markdown(
    """
### Choose Your Challenge
Select the desired difficulty level. This will determine which interpolated dataset the simulation uses:

- **Medium**: Uses Iowa interpolated data.
- **Hard**: Uses Texas interpolated data.

You can proceed anytime; the choice is stored in session state.
"""
)

col = st.columns(2)
with col[0]:
    if st.button("Medium Difficulty", key="diff_medium"):
        set_difficulty("medium")
with col[1]:
    if st.button("Hard Difficulty", key="diff_hard"):
        set_difficulty("hard")

current = get_difficulty()
with st.expander("Current selection (debug / can hide later)"):
    st.write(debug_difficulty_info())
    st.info("You can change the difficulty and then continue; downstream pages will read the active dataset.")

st.divider()

if st.button("Continue ➜", type="primary"):
    st.switch_page("pages/2_🌱_Phần_2_Slide_01.py")
