import streamlit as st

st.title("Part 1 — Slide 07: Choose a Candidate Planet")

st.markdown(
    """
Select ONE of the three candidate planets below. Only one has promising metrics; the other two are unlikely to sustain life.
<br><br>
<b>Metrics shown:</b> Temperature (K), log10(Period), log10(Flux), Radius (R⊕)
""",
    unsafe_allow_html=True,
)

# Fabricated planet metrics based on earlier slides (good ranges: moderate temp ~250-300K, balanced flux, moderate period, radius ~0.8–1.6 R⊕)
planets = [
    {
        "code": "PX-199",
        "img": "assets/asset part 1/planets/planet_unknown.png",
        "temp": 640,  # too hot
        "logP": 0.35,
        "logF": 1.15,  # high flux
        "radius": 2.8,  # too large (gas-like)
        "good": False,
        "reason": "High flux & oversized radius – likely a hot mini-Neptune."
    },
    {
        "code": "HL-482",
        "img": "assets/asset part 1/planets/planet_unknown.png",
        "temp": 274,  # near Earth-like
        "logP": 1.02,
        "logF": 0.05,  # moderate flux
        "radius": 1.12,
        "good": True,
        "reason": "Balanced temp, moderate flux, rocky radius in habitable range."
    },
    {
        "code": "QS-071",
        "img": "assets/asset part 1/planets/planet_unknown.png",
        "temp": 155,  # too cold
        "logP": -0.2,
        "logF": -0.6,  # low flux
        "radius": 0.55,  # very small (possibly airless)
        "good": False,
        "reason": "Cold, low stellar flux and too small to retain atmosphere."
    },
]

if 'candidate_choice' not in st.session_state:
    st.session_state.candidate_choice = None

cols = st.columns(3)
for i, planet in enumerate(planets):
    with cols[i]:
        try:
            st.image(planet["img"], width=140)
        except Exception:
            st.write("(missing image)")
        st.markdown(f"**{planet['code']}**")
        st.caption(planet['reason'])
        st.metric("Temp (K)", planet['temp'])
        st.metric("log₁₀ Period", planet['logP'])
        st.metric("log₁₀ Flux", planet['logF'])
        st.metric("Radius (R⊕)", planet['radius'])
        if st.button(f"Select {planet['code']}", key=f"pick_{planet['code']}"):
            st.session_state.candidate_choice = planet

st.divider()

choice = st.session_state.candidate_choice
if choice is None:
    st.info("Pick a planet to proceed.")
else:
    if choice['good']:
        st.success(f"{choice['code']} shows strong potential. Proceed to confirmation.")
        if st.button("Confirm and Continue ➜", key="go_good"):
            st.session_state.chosen_planet = choice['code']
            st.switch_page("pages/1_🔭_Phần_1_Slide_09.py")  # will become Slide 09 success page
    else:
        st.error(f"{choice['code']} has low predicted habitability. Please pick another candidate or insist.")
        if st.button("Proceed anyway (not recommended)", key="go_bad_override"):
            st.session_state.chosen_planet = choice['code']
            st.switch_page("pages/1_🔭_Phần_1_Slide_11.py")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("⬅️ Back to Regression"):
    st.switch_page("pages/1_🔭_Phần_1_Slide_06.py")
