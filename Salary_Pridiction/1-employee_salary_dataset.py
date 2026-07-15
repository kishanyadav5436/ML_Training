import pandas as pd
import xgboost as xgb
import streamlit as st

st.set_page_config(
    page_title="Employee Salary Prediction",
    page_icon="💼",
    layout="centered",
)


def inject_css():
    css = """
    <style>
    /* Page background */
    .stApp {
        background: linear-gradient(180deg, #eef2ff 0%, #ffffff 100%);
    }

    /* Center column width + padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 720px;
    }

    /* Keyframe animations */
    @keyframes fadeSlideIn {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.45); }
        70% { box-shadow: 0 0 0 12px rgba(37, 99, 235, 0); }
        100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
    }
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }

    /* Header card */
    .header-card {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 24px;
        box-shadow: 0 18px 50px rgba(15, 23, 42, 0.1);
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        animation: fadeSlideIn 0.6s ease-out;
    }
    .header-icon {
        display: block;
        text-align: center;
        font-size: 2.4rem;
        animation: bounce 2.2s ease-in-out infinite;
    }
    .app-heading {
        color: #1d4ed8;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 2.4rem;
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .app-subtitle {
        color: #334155;
        text-align: center;
        margin-top: 0;
        margin-bottom: 0;
        font-size: 1rem;
    }

    /* Section titles inside the form */
    .section-title {
        color: #1e3a8a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1.25rem 0 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: fadeSlideIn 0.5s ease-out;
    }
    .section-title .icon {
        font-size: 1.2rem;
    }

    /* Style every Streamlit "vertical block" that wraps widgets like a card.
       This targets Streamlit's real DOM so the styling actually applies
       (unlike a raw <div> in st.markdown, which does not contain later widgets). */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 24px;
        box-shadow: 0 18px 50px rgba(15, 23, 42, 0.1);
        padding: 2rem;
        border: 1px solid rgba(148, 163, 184, 0.2);
        animation: fadeSlideIn 0.7s ease-out;
    }

    /* Labels */
    label, .stMarkdown p {
        color: #1e293b !important;
        font-weight: 500;
    }

    /* Inputs */
    div[data-baseweb="select"] > div,
    .stNumberInput input,
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }
    div[data-baseweb="select"] > div:focus-within,
    .stNumberInput input:focus,
    .stTextInput input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    /* Button */
    .stButton>button, .stFormSubmitButton>button {
        background-color: #2563eb;
        color: #ffffff;
        border-radius: 12px;
        border: none;
        padding: 0.85rem 1rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s ease-in-out, transform 0.15s ease-in-out;
        animation: pulseGlow 2.5s infinite;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background-color: #1d4ed8;
        color: #ffffff;
        transform: translateY(-2px) scale(1.01);
    }
    .stButton>button:active, .stFormSubmitButton>button:active {
        transform: translateY(0) scale(0.99);
    }

    /* Success box */
    div[data-testid="stAlert"] {
        border-radius: 14px;
        font-size: 1.05rem;
        font-weight: 600;
        animation: popIn 0.45s ease-out;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header():
    st.markdown(
        """
        <div class='header-card'>
            <span class='header-icon'>💼</span>
            <h1 class='app-heading'>Employee Salary Prediction</h1>
            <p class='app-subtitle'>This app will help you predict employee salary in LPA.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    inject_css()
    render_header()

    # Load Model
    model = xgb.XGBRegressor()
    model.load_model("xgb_model.json")

    with st.form("salary_form"):
        st.markdown("<div class='section-title'><span class='icon'>🧑</span>Personal Details</div>", unsafe_allow_html=True)
        p1 = st.number_input(
            "🎂 Please enter age",
            min_value=18,
            max_value=70,
            value=28,
            step=1,
        )

        s1 = st.selectbox("⚧ Select Gender", ("Male", "Female"))
        p2 = 1 if s1 == "Male" else 0

        s2 = st.selectbox("🎓 Select Education", ("Diploma", "Bachelor", "Master", "PhD"))
        education_map = {"Diploma": 0, "Bachelor": 1, "Master": 2, "PhD": 3}
        p3 = education_map[s2]

        st.markdown("<div class='section-title'><span class='icon'>💼</span>Role & Experience</div>", unsafe_allow_html=True)
        p4 = st.number_input(
            "📈 Please enter experience years",
            min_value=0,
            max_value=40,
            value=5,
            step=1,
        )

        s3 = st.selectbox(
            "🏢 Select Department",
            ("Operations", "IT", "Finance", "Sales", "HR", "Marketing"),
        )
        department_map = {"Operations": 0, "IT": 1, "Finance": 2, "Sales": 3, "HR": 4, "Marketing": 5}
        p5 = department_map[s3]

        s4 = st.selectbox(
            "🪜 Select Job Level",
            ("Junior", "Mid", "Senior", "Lead", "Manager"),
        )
        job_level_map = {"Junior": 1, "Mid": 2, "Senior": 3, "Lead": 4, "Manager": 5}
        p6 = job_level_map[s4]

        p7 = st.selectbox("⭐ Select Performance Rating", (1, 2, 3, 4, 5))

        st.markdown("<div class='section-title'><span class='icon'>🚀</span>Performance & Work Style</div>", unsafe_allow_html=True)
        p8 = st.number_input(
            "📜 Please enter certifications count",
            min_value=0,
            max_value=20,
            value=3,
            step=1,
        )

        p9 = st.number_input(
            "⏱️ Please enter overtime hours",
            min_value=0,
            max_value=200,
            value=10,
            step=1,
        )

        s5 = st.selectbox("🏠 Remote Work", ("Yes", "No"))
        p10 = 1 if s5 == "Yes" else 0

        st.markdown("<div class='section-title'><span class='icon'>📍</span>Location & Tenure</div>", unsafe_allow_html=True)
        s6 = st.selectbox(
            "🌆 Select City",
            ("Hyderabad", "Mumbai", "Pune", "Chennai", "Bangalore", "Delhi"),
        )
        city_map = {"Hyderabad": 0, "Mumbai": 1, "Pune": 2, "Chennai": 3, "Bangalore": 4, "Delhi": 5}
        p11 = city_map[s6]

        p12 = st.number_input(
            "🏢 Please enter company tenure (years)",
            min_value=0,
            max_value=40,
            value=3,
            step=1,
        )

        p13 = st.number_input(
            "✅ Please enter projects completed",
            min_value=0,
            max_value=50,
            value=5,
            step=1,
        )

        p14 = st.number_input(
            "🧠 Please enter skill score (0-100)",
            min_value=0,
            max_value=100,
            value=75,
            step=1,
        )

        submitted = st.form_submit_button("🔮 Predict")

    if submitted:
        data_new = pd.DataFrame({
            "Age": [p1],
            "Gender": [p2],
            "Education": [p3],
            "Experience_Years": [p4],
            "Department": [p5],
            "Job_Level": [p6],
            "Performance_Rating": [p7],
            "Certifications": [p8],
            "Overtime_Hours": [p9],
            "Remote_Work": [p10],
            "City": [p11],
            "Company_Tenure": [p12],
            "Projects_Completed": [p13],
            "Skill_Score": [p14],
        })
        with st.spinner("🔮 Crunching the numbers..."):
            pred = model.predict(data_new)
        st.success(f"💰 Estimated annual salary: {pred[0]:.2f} LPA")
        st.balloons()


if __name__ == "__main__":
    main()