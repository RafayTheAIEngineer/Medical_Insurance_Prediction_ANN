import streamlit as st
import requests
import pandas as pd

# --------------------------------------------------------------------------
# Page configuration
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Assura — Insurance Cost Estimator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------------------------------
# Custom styling
# --------------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Spectral:wght@600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        h1, h2, h3, h4, .brand-mark, [data-testid="stMetricValue"] {
            font-family: 'Spectral', serif;
        }

        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header[data-testid="stHeader"] { background: transparent; }

        .block-container {
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1080px;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background-color: #201811;
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        .brand-mark {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.15rem;
            font-weight: 700;
            color: #F5EFE6;
            margin-bottom: 6px;
        }
        .brand-mark span.dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 3px;
            background: linear-gradient(135deg, #D4A24C, #9C6F26);
        }
        .sidebar-sub {
            color: #B8A990;
            font-size: 0.85rem;
            line-height: 1.5;
            margin-bottom: 1.1rem;
        }
        section[data-testid="stSidebar"] .stButton > button {
            background: transparent;
            border: 1px solid rgba(201,151,63,0.45);
            color: #C9973F;
            box-shadow: none;
            width: 100%;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(201,151,63,0.08);
            transform: none;
            box-shadow: none;
            color: #C9973F;
        }

        /* ---------- Header ---------- */
        .app-title {
            font-size: 2.15rem;
            font-weight: 700;
            color: #F5EFE6;
            margin-bottom: 0.2rem;
        }
        .app-subtitle {
            color: #B8A990;
            font-size: 1.02rem;
            margin-bottom: 1.6rem;
        }

        /* ---------- Tabs ---------- */
        [data-baseweb="tab-list"] {
            gap: 28px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        [data-baseweb="tab"] {
            background: transparent;
            padding: 8px 2px;
            font-weight: 500;
            color: #B8A990;
        }
        [aria-selected="true"][data-baseweb="tab"] {
            color: #F5EFE6 !important;
            border-bottom: 2px solid #C9973F !important;
        }

        /* ---------- Expander ---------- */
        details {
            background-color: #201811;
            border: 1px solid rgba(255,255,255,0.06);
            border-left: 3px solid rgba(201,151,63,0.55);
            border-radius: 10px;
            margin-bottom: 14px;
        }
        summary {
            font-weight: 600;
            font-size: 0.98rem;
            color: #EFE6D8;
            padding: 4px 2px;
        }

        /* ---------- Inputs ---------- */
        .stNumberInput label, .stSelectbox label {
            color: #C7B89C;
            font-size: 0.86rem;
            font-weight: 500;
        }
        .stNumberInput input {
            background-color: #17110C;
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 8px;
            color: #F5EFE6;
        }
        .stNumberInput input:focus {
            border-color: #C9973F;
            box-shadow: 0 0 0 1px #C9973F;
        }
        .stSelectbox > div > div {
            background-color: #17110C;
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 8px;
        }

        /* ---------- Primary button ---------- */
        .stFormSubmitButton > button {
            width: 100%;
            border: none;
            border-radius: 10px;
            padding: 0.65rem 1rem;
            font-weight: 600;
            font-size: 0.98rem;
            color: #1A130C;
            background: linear-gradient(135deg, #D4A24C, #B37F2E);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(201,151,63,0.30);
            color: #1A130C;
        }
        .stFormSubmitButton > button:active {
            transform: translateY(0px);
        }

        /* ---------- Hero result panel ---------- */
        .hero-panel {
            border-radius: 10px;
            padding: 1.3rem 1.6rem;
            border-left: 4px solid #C9973F;
            background: rgba(201,151,63,0.08);
            animation: rise 0.35s ease;
        }
        .hero-label {
            color: #B8A990;
            font-size: 0.88rem;
            margin-bottom: 4px;
        }
        .hero-value {
            font-family: 'Spectral', serif;
            font-weight: 700;
            font-size: 2.7rem;
            color: #F5EFE6;
            line-height: 1.1;
        }
        @keyframes rise {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ---------- Profile snapshot card ---------- */
        .profile-card {
            background: #201811;
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 10px;
            padding: 1rem 1.2rem;
            height: 100%;
        }
        .profile-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9rem;
            color: #D9CBB0;
            padding: 6px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .profile-row:last-child { border-bottom: none; }
        .badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
        }
        .badge.smoker { background: rgba(224,121,60,0.18); color: #E0793C; }
        .badge.nonsmoker { background: rgba(127,184,138,0.18); color: #7FB88A; }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_css()


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand-mark"><span class="dot"></span>CareShield</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sidebar-sub">Estimates annual medical insurance charges from '
        "patient details, using a trained deep learning (ANN) model.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("**Backend connection**")
    base_url = st.text_input(
        "Backend base URL",
        value="http://127.0.0.1:8000",
        label_visibility="collapsed",
    )
    st.caption("Should point at your running FastAPI app (no trailing slash).")

    if st.button("Test connection"):
        try:
            root_resp = requests.get(f"{base_url}/", timeout=5)
            if root_resp.status_code == 200:
                st.success("Backend is reachable.")
            else:
                st.warning(f"Backend responded with status {root_resp.status_code}.")
        except requests.exceptions.RequestException:
            st.error("Backend is not reachable.")

    st.markdown("---")
    st.caption("For educational use only — not financial or insurance advice.")

predict_url = f"{base_url}/predict"


# --------------------------------------------------------------------------
# Header
# --------------------------------------------------------------------------
st.markdown('<div class="app-title">Insurance Cost Estimator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Estimate a patient\'s annual insurance charges from a few basic details.</div>',
    unsafe_allow_html=True,
)

tab_estimate, tab_about = st.tabs(["Estimate", "About the model"])


# --------------------------------------------------------------------------
# Tab 1 — Estimate
# --------------------------------------------------------------------------
with tab_estimate:
    with st.form("insurance_form"):
        with st.expander("Personal details", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                age = st.number_input(
                    "Age", min_value=18, max_value=100, value=30, step=1,
                    help="Age of patient, between 18 and 100",
                )
            with c2:
                sex = st.selectbox("Sex", options=["male", "female"], index=0)
            with c3:
                bmi = st.number_input(
                    "BMI", min_value=10.1, max_value=59.9, value=25.0, step=0.1,
                    format="%.1f", help="Body Mass Index, between 10 and 60",
                )

        with st.expander("Lifestyle & location", expanded=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                children = st.number_input(
                    "Children", min_value=0, max_value=10, value=2, step=1,
                    help="Number of children, between 0 and 10",
                )
            with c2:
                smoker = st.selectbox("Smoker", options=["no", "yes"], index=0)
            with c3:
                region = st.selectbox(
                    "Region",
                    options=["northeast", "northwest", "southeast", "southwest"],
                    index=0,
                )

        st.caption("Tip: after typing a value, press Enter or Tab before clicking Estimate — otherwise the last edited field may not register.")
        submitted = st.form_submit_button("Estimate cost")

    if submitted:
        payload = {
            "age": int(age),
            "sex": sex,
            "bmi": float(bmi),
            "children": int(children),
            "smoker": smoker,
            "region": region,
        }

        with st.expander("Request payload sent to the API", expanded=False):
            st.json(payload)

        response = None
        with st.spinner("Calculating estimate..."):
            try:
                response = requests.post(predict_url, json=payload, timeout=10)
                response.raise_for_status()
                result = response.json()

                charge = result.get("predicted_insurance_charges")
                charge_display = f"${charge:,.2f}" if charge is not None else "—"

                st.markdown("<br>", unsafe_allow_html=True)
                res_col1, res_col2 = st.columns([1.4, 1])

                with res_col1:
                    st.markdown(
                        f"""
                        <div class="hero-panel">
                            <div class="hero-label">Estimated annual insurance charge</div>
                            <div class="hero-value">{charge_display}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with res_col2:
                    badge_class = "smoker" if smoker == "yes" else "nonsmoker"
                    badge_text = "Smoker" if smoker == "yes" else "Non-smoker"
                    st.markdown(
                        f"""
                        <div class="profile-card">
                            <div class="profile-row"><span>Age</span><span>{age}</span></div>
                            <div class="profile-row"><span>BMI</span><span>{bmi:.1f}</span></div>
                            <div class="profile-row"><span>Children</span><span>{children}</span></div>
                            <div class="profile-row"><span>Status</span><span class="badge {badge_class}">{badge_text}</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    f"Couldn't reach the backend at `{predict_url}`. "
                    "Make sure your FastAPI server is running."
                )
            except requests.exceptions.HTTPError:
                detail = response.text if response is not None else "no response"
                st.error(f"The server responded with an error: {detail}")
            except Exception as e:
                st.error(f"Something went wrong while calculating the estimate: {e}")


# --------------------------------------------------------------------------
# Tab 2 — About the model
# --------------------------------------------------------------------------
with tab_about:
    st.markdown("#### What this app does")
    st.write(
        "This tool sends a patient's age, sex, BMI, number of children, smoking "
        "status, and region to a deep learning model, which returns an estimated "
        "annual insurance charge."
    )

    st.markdown("#### Input features")
    feature_info = pd.DataFrame(
        [
            ("age", "Age of patient", "18 – 100"),
            ("sex", "Gender of patient", "male, female"),
            ("bmi", "Body Mass Index", "10 – 60"),
            ("children", "Number of children", "0 – 10"),
            ("smoker", "Whether the patient smokes", "yes, no"),
            ("region", "US region", "northeast, northwest, southeast, southwest"),
        ],
        columns=["Field", "Description", "Accepted values"],
    )
    st.dataframe(feature_info, hide_index=True, use_container_width=True)

    st.markdown("#### BMI reference")
    bmi_info = pd.DataFrame(
        [
            ("Underweight", "Below 18.5"),
            ("Normal", "18.5 – 24.9"),
            ("Overweight", "25 – 29.9"),
            ("Obese", "30 and above"),
        ],
        columns=["Category", "BMI range"],
    )
    st.dataframe(bmi_info, hide_index=True, use_container_width=True)

    st.markdown("#### A note on use")
    st.caption(
        "This app is for educational purposes only and does not provide financial, "
        "medical, or insurance advice. Actual policy pricing depends on many factors "
        "beyond what this model considers."
    )


# --------------------------------------------------------------------------
# Footer
# --------------------------------------------------------------------------
st.markdown(
    """
    <div class="app-footer">
        <span class="footer-brand">CareShield</span>
        <span>Educational project — not financial or insurance advice</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-footer">
        <span>Developed by Rafay</span>
    </div>
    """,
    unsafe_allow_html=True,
)