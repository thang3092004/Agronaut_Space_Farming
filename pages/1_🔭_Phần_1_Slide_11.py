import streamlit as st
from pathlib import Path
import base64

st.title("Part 1 — Slide 11: A Wrong Turn")

def _b64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode()

img_b64 = _b64("assets/asset part 1/wrong_turn/wrong_turn.png")

st.markdown(
    """
### This is the fate of a stubborn predecessor who ignored the warning.
You chose a planet with poor metrics. Turn back and reconsider a more balanced candidate.
    """
)

if img_b64:
    st.image(f"data:image/png;base64,{img_b64}")
else:
    st.warning("Missing image: wrong_turn.png")

st.divider()

if st.button("⬅️ Back to Candidate Selection"):
    st.switch_page("pages/1_🔭_Phần_1_Slide_07.py")
