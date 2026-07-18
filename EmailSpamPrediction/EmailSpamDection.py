import streamlit as st
import streamlit.components.v1 as components
import json
import math
import os

# =====================================================================
# Page config
# =====================================================================
st.set_page_config(
    page_title="Email Threat Scanner",
    page_icon="◉",
    layout="centered",
    initial_sidebar_state="expanded",
)

# =====================================================================
# Design tokens — console / instrument-panel theme
# =====================================================================
BG = "#0B1021"
SURFACE = "#141A33"
SURFACE_2 = "#1C2444"
BORDER = "#2A3260"
TEXT = "#E9ECFB"
TEXT_MUTE = "#8A90BF"
SAFE = "#2FD9C4"
THREAT = "#FF5D73"
AMBER = "#FFB454"

# =====================================================================
# Global CSS
# =====================================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background: {BG};
    background-image:
        radial-gradient(circle at 15% 0%, rgba(47,217,196,0.06) 0%, transparent 40%),
        radial-gradient(circle at 85% 100%, rgba(255,93,115,0.05) 0%, transparent 40%);
    color: {TEXT};
}}

.block-container {{
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 720px;
}}

.eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.18em;
    color: {SAFE};
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.6rem;
}}
.eyebrow .dot {{
    width: 7px; height: 7px; border-radius: 50%;
    background: {SAFE};
    box-shadow: 0 0 8px {SAFE};
    animation: pulse 2s ease-in-out infinite;
}}
@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.35; }}
}}
h1.title {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.15rem;
    letter-spacing: -0.01em;
    color: {TEXT};
    margin: 0 0 0.35rem 0;
}}
.subtitle {{
    font-family: 'Inter', sans-serif;
    color: {TEXT_MUTE};
    font-size: 0.98rem;
    margin-bottom: 2.2rem;
}}

.panel {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1.3rem;
}}
.panel-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {TEXT_MUTE};
    margin-bottom: 1rem;
}}

div[data-testid="stNumberInput"] label {{
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.04em;
    color: {TEXT_MUTE} !important;
    text-transform: uppercase;
}}
div[data-testid="stNumberInput"] input {{
    background: {SURFACE_2} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.05rem !important;
}}
div[data-testid="stNumberInput"] input:focus {{
    border-color: {SAFE} !important;
    box-shadow: 0 0 0 1px {SAFE} !important;
}}
div[data-testid="stNumberInput"] button {{
    background: {SURFACE_2} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT_MUTE} !important;
}}

div[data-testid="stButton"] button {{
    width: 100%;
    background: linear-gradient(135deg, {SAFE} 0%, #21B8A6 100%);
    color: #0B1021;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1rem;
    letter-spacing: 0.02em;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 4px 20px rgba(47,217,196,0.25);
}}
div[data-testid="stButton"] button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 26px rgba(47,217,196,0.35);
}}
div[data-testid="stButton"] button:focus-visible {{
    outline: 2px solid {SAFE};
    outline-offset: 2px;
}}

section[data-testid="stSidebar"] {{
    background: {SURFACE};
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] .block-container {{
    padding-top: 2rem;
}}
.spec-row {{
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid {BORDER};
    color: {TEXT_MUTE};
}}
.spec-row span.val {{
    color: {TEXT};
}}
.spec-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    color: {TEXT};
    font-size: 1.02rem;
    margin-bottom: 0.3rem;
}}
.spec-desc {{
    font-family: 'Inter', sans-serif;
    color: {TEXT_MUTE};
    font-size: 0.85rem;
    line-height: 1.5;
    margin-bottom: 1.3rem;
}}

[data-testid="stExpander"] {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
::-webkit-scrollbar {{ width: 10px; }}
::-webkit-scrollbar-thumb {{ background: {SURFACE_2}; border-radius: 6px; }}

@media (prefers-reduced-motion: reduce) {{
    * {{ animation: none !important; transition: none !important; }}
}}
</style>
""", unsafe_allow_html=True)

# =====================================================================
# Load model
# =====================================================================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "spam_logistic_model.json")

@st.cache_resource
def load_model(path):
    with open(path, "r") as f:
        return json.load(f)

try:
    model = load_model(MODEL_PATH)
except FileNotFoundError:
    st.error(
        "Model file not found: `spam_logistic_model.json`. "
        "Place it in the same folder as this app."
    )
    st.stop()


def predict_spam(email_length: float, num_links: int, num_special_chars: int):
    x = [email_length, num_links, num_special_chars]
    coefficients = model["coefficients"]
    intercept = model["intercept"][0]
    z = sum(c * xi for c, xi in zip(coefficients, x)) + intercept
    prob = 1 / (1 + math.exp(-z))
    return (1 if prob >= 0.5 else 0), prob


# =====================================================================
# Sidebar — model spec sheet
# =====================================================================
with st.sidebar:
    st.markdown('<div class="spec-title">Model Spec</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="spec-desc">Logistic Regression classifier, exported as portable JSON. '
        'No pickle, no joblib — just weights and an intercept.</div>',
        unsafe_allow_html=True
    )
    acc = model.get("accuracy", 0) * 100
    rows = [
        ("type", model.get("model_type", "LogisticRegression")),
        ("accuracy", f"{acc:.2f}%"),
        ("features", str(len(model.get("features", [])))),
        ("target", model.get("target", "Spam")),
    ]
    for k, v in rows:
        st.markdown(
            f'<div class="spec-row"><span>{k}</span><span class="val">{v}</span></div>',
            unsafe_allow_html=True
        )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="spec-title" style="font-size:0.9rem;">Inputs</div>', unsafe_allow_html=True)
    for feat in model.get("features", []):
        st.markdown(
            f'<div class="spec-row"><span>—</span><span class="val">{feat}</span></div>',
            unsafe_allow_html=True
        )

# =====================================================================
# Header
# =====================================================================
st.markdown('<div class="eyebrow"><span class="dot"></span>SCANNER ONLINE</div>', unsafe_allow_html=True)
st.markdown('<h1 class="title">Email Threat Scanner</h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Score an email\'s spam signals in real time. '
    'Three numbers in, one verdict out.</div>',
    unsafe_allow_html=True
)

# =====================================================================
# Input panel
# =====================================================================
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown('<div class="panel-label">Signal Input</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    email_length = st.number_input("Email length", min_value=0, max_value=5000, value=100, step=1)
with col2:
    num_links = st.number_input("Num links", min_value=0, max_value=50, value=1, step=1)
with col3:
    num_special_chars = st.number_input("Special chars", min_value=0, max_value=100, value=3, step=1)

scan = st.button("▶  Run Scan")
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================
# Result — radial gauge (signature element)
# =====================================================================
if scan:
    prediction, probability = predict_spam(email_length, num_links, num_special_chars)
    pct = probability * 100

    if probability < 0.5:
        ring_color = SAFE
        verdict = "CLEAN"
        verdict_sub = "No significant spam signal detected"
    elif probability < 0.75:
        ring_color = AMBER
        verdict = "SUSPICIOUS"
        verdict_sub = "Elevated spam signal — review before trusting"
    else:
        ring_color = THREAT
        verdict = "SPAM"
        verdict_sub = "High-confidence spam signal detected"

    radius = 70
    circumference = 2 * math.pi * radius
    offset = circumference * (1 - probability)

    gauge_html = f"""
    <div style="font-family:'Inter',sans-serif; background:{SURFACE}; border:1px solid {BORDER};
                border-radius:14px; padding:2rem 1.5rem; display:flex; flex-direction:column;
                align-items:center; gap:0.4rem;">
      <svg width="180" height="180" viewBox="0 0 180 180">
        <circle cx="90" cy="90" r="{radius}" fill="none" stroke="{SURFACE_2}" stroke-width="14"/>
        <circle cx="90" cy="90" r="{radius}" fill="none" stroke="{ring_color}" stroke-width="14"
                stroke-linecap="round"
                stroke-dasharray="{circumference}" stroke-dashoffset="{circumference}"
                transform="rotate(-90 90 90)">
          <animate attributeName="stroke-dashoffset" from="{circumference}" to="{offset}"
                   dur="0.9s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>
        </circle>
        <text x="90" y="84" text-anchor="middle" fill="{TEXT}"
              font-family="'Space Grotesk', sans-serif" font-weight="700" font-size="30">
              {pct:.0f}%
        </text>
        <text x="90" y="106" text-anchor="middle" fill="{TEXT_MUTE}"
              font-family="'JetBrains Mono', monospace" font-size="11" letter-spacing="1">
              SPAM SCORE
        </text>
      </svg>
      <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.3rem;
                  color:{ring_color}; letter-spacing:0.03em; margin-top:0.2rem;">
        {verdict}
      </div>
      <div style="font-family:'Inter', sans-serif; font-size:0.85rem; color:{TEXT_MUTE};
                  text-align:center; max-width:280px;">
        {verdict_sub}
      </div>
    </div>
    """
    components.html(gauge_html, height=330)

    with st.expander("Raw scan data"):
        st.json({
            "input": {
                "Email_Length": email_length,
                "Num_Links": num_links,
                "Num_Special_Chars": num_special_chars
            },
            "prediction": prediction,
            "spam_probability": round(probability, 4)
        })

st.markdown(
    f'<div style="text-align:center; color:{TEXT_MUTE}; font-family:JetBrains Mono, monospace; '
    f'font-size:0.72rem; margin-top:2rem; letter-spacing:0.05em;">'
    f'MODEL SERVED FROM JSON · NO PICKLE DEPENDENCY</div>',
    unsafe_allow_html=True
)