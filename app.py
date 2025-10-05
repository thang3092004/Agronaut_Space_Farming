import streamlit as st
from pathlib import Path

st.set_page_config(page_title="COSMOS EYE — Space Farm", page_icon="🚀", layout="wide")

css_path = Path("theme.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.title("🚀 COSMOS EYE — Space Farm")
st.write("Mỗi **slide** là **một file riêng** trong `pages/`. Hãy mở sidebar để chọn.")

st.markdown("**Gợi ý:** Bắt đầu từ _1️⃣ Phần 1 — Slide 01_ trong sidebar.")
