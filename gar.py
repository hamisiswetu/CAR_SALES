import streamlit as st
import joblib
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Car Sales – Bei ya Gari",
    page_icon="🚗",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@300;400;600&display=swap');

/* ── Root variables ── */
:root {
    --midnight:  #0A0E1A;
    --deepblue:  #0D1B2A;
    --steel:     #1C2D40;
    --accent:    #00C4FF;
    --gold:      #F5A623;
    --white:     #F0F4FF;
    --muted:     #8899AA;
}

/* ── Full-page background with car image ── */
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(135deg, rgba(5,10,20,.82) 0%, rgba(10,20,40,.75) 50%, rgba(5,10,20,.88) 100%),
        url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=1600&q=85') center/cover no-repeat fixed !important;
    color: var(--white) !important;
}

html, body {
    background: #0A0E1A !important;
}

[data-testid="stHeader"] {
    background: rgba(5,10,20,.6) !important;
    backdrop-filter: blur(10px) !important;
}

/* Sidebar / main block background transparent */
[data-testid="stMain"] {
    background: transparent !important;
}
section[data-testid="stSidebar"] {
    background: rgba(10,20,40,.85) !important;
    backdrop-filter: blur(12px) !important;
}

/* ── Hero banner ── */
.hero {
    background:
        linear-gradient(to bottom, rgba(10,14,26,.15) 0%, rgba(10,14,26,.92) 100%),
        url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1200&q=80') center/cover no-repeat;
    border-radius: 16px;
    padding: 56px 40px 40px;
    margin-bottom: 32px;
    text-align: center;
    border: 1px solid rgba(0,196,255,.18);
    box-shadow: 0 8px 40px rgba(0,196,255,.12);
}
.hero-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 12px;
}
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(28px, 5vw, 52px);
    font-weight: 900;
    color: var(--white);
    line-height: 1.1;
    margin: 0 0 10px;
    text-shadow: 0 0 40px rgba(0,196,255,.4);
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    color: var(--muted);
    margin: 0;
}

/* ── Card — glassmorphism ── */
.card {
    background: rgba(10, 20, 40, 0.55);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(0,196,255,.22);
    border-radius: 14px;
    padding: 28px 28px 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,.5);
}
.card-label {
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 18px;
}

/* ── Streamlit widget overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(15, 30, 55, 0.7) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid rgba(0,196,255,.30) !important;
    border-radius: 8px !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,196,255,.15) !important;
}

/* Labels */
label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    letter-spacing: .5px !important;
}

/* ── Predict button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--accent) 0%, #007BB5 100%) !important;
    color: #000 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 1.5px !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    margin-top: 8px !important;
    cursor: pointer !important;
    transition: transform .15s, box-shadow .15s !important;
    box-shadow: 0 4px 20px rgba(0,196,255,.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(0,196,255,.55) !important;
}

/* ── Result box ── */
.result-box {
    background: linear-gradient(135deg, rgba(0,196,255,.12), rgba(245,166,35,.08));
    border: 1px solid var(--accent);
    border-radius: 14px;
    padding: 32px;
    text-align: center;
    margin-top: 24px;
}
.result-label {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
}
.result-price {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(30px, 6vw, 52px);
    font-weight: 900;
    color: var(--accent);
    text-shadow: 0 0 30px rgba(0,196,255,.5);
}
.result-note {
    font-family: 'Inter', sans-serif;
    font-size: 13px;
    color: var(--muted);
    margin-top: 8px;
}

/* ── Status messages ── */
[data-testid="stSuccess"], [data-testid="stError"], [data-testid="stWarning"] {
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid rgba(0,196,255,.12);
    margin: 24px 0;
}

/* ── Footer ── */
.footer {
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: var(--muted);
    margin-top: 36px;
    padding-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-eyebrow">🚗 Powered by Machine Learning</p>
    <h1 class="hero-title">CAR SALES<br>PRICE PREDICTOR</h1>
    <p class="hero-sub">Jaza taarifa za gari kupata makadirio ya bei kwa sekunde moja</p>
</div>
""", unsafe_allow_html=True)


# ── Load model ─────────────────────────────────────────────────────────────────
model = None
try:
    model = joblib.load("CAR_SALES.joblib")
    st.success("✅ Modeli imepakiwa vizuri")
except FileNotFoundError:
    st.warning("⚠️ Faili 'CAR_SALES.joblib' haijapatikana. Tafadhali weka faili katika folda moja na app hii.")
except Exception as e:
    st.error(f"❌ Hitilafu: {e}")


# ── Input form ─────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><p class="card-label">📋 Taarifa za Gari</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    manufacturer = st.text_input("Mtengenezaji (Manufacturer)", placeholder="Toyota, Honda, BMW…")

with col2:
    model_name = st.text_input("Mfano wa Gari (Model)", placeholder="Corolla, Civic, X5…")

col3, col4 = st.columns(2)

with col3:
    engine_size = st.number_input(
        "Ukubwa wa Injini (Engine Size / L)",
        min_value=0.5, max_value=10.0, value=1.5, step=0.1,
        format="%.1f"
    )

with col4:
    fuel_type = st.selectbox(
        "Aina ya Mafuta (Fuel Type)",
        ["Petrol", "Diesel", "Hybrid", "Electric"]
    )

col5, col6 = st.columns(2)

with col5:
    year = st.number_input(
        "Mwaka wa Utengenezaji",
        min_value=1980, max_value=2030, value=2020, step=1
    )

with col6:
    mileage = st.number_input(
        "Umbali Uliofanywa (Mileage / km)",
        min_value=0, value=50000, step=1000
    )

st.markdown('</div>', unsafe_allow_html=True)


# ── Predict ────────────────────────────────────────────────────────────────────
if st.button("🔍 KADIRIA BEI", use_container_width=True):
    if model is None:
        st.error("❌ Modeli haipo. Hakikisha 'CAR_SALES.joblib' ipo kwenye folda sahihi.")
    elif not manufacturer.strip() or not model_name.strip():
        st.warning("⚠️ Tafadhali jaza Mtengenezaji na Mfano wa Gari.")
    else:
        with st.spinner("Inakokotoa bei…"):
            input_data = pd.DataFrame({
                "Manufacturer":       [manufacturer.strip()],
                "Model":              [model_name.strip()],
                "Engine size":        [engine_size],
                "Fuel type":          [fuel_type],
                "Year of manufacture":[int(year)],
                "Mileage":            [int(mileage)],
            })
            try:
                prediction = model.predict(input_data)[0]
                st.markdown(f"""
                <div class="result-box">
                    <p class="result-label">Makadirio ya Bei</p>
                    <div class="result-price">TZS {prediction:,.0f}</div>
                    <p class="result-note">
                        {manufacturer} {model_name} · {int(year)} · {fuel_type} · {mileage:,} km
                    </p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"❌ Hitilafu wakati wa kukokotoa: {e}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    🚗 Car Sales Price Predictor &nbsp;|&nbsp; Powered by Machine Learning &nbsp;|&nbsp; Tanzania
</div>
""", unsafe_allow_html=True)