import streamlit as st
import pandas as pd
import pickle

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="CardioSense",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main page styling */
    .main {
        background: linear-gradient(135deg, #1a1f2b 0%, #0e1117 100%);
        padding: 2rem;
    }

    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }

    /* Header styling */
    .title-container {
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.1) 0%, rgba(255, 75, 75, 0.05) 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        text-align: center;
        border: 1px solid rgba(255, 75, 75, 0.2);
        backdrop-filter: blur(10px);
    }
    .title-text {
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8f8f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .subtitle-text {
        color: #fafafa;
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
    }

    /* Section headers */
    .section-header {
        color: #ff4b4b;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Improved Slider Styling */
    .stSlider {
        margin: 2.5rem 0;
        padding: 0 1rem;
        position: relative;
    }

    .stSlider > div > div {
        display: flex;
        flex-direction: column;
    }

    .stSlider > div > div > div:nth-child(1) {
        margin-bottom: 1rem; /* spacing between label and slider */
    }

    .stSlider > div > div > div:nth-child(2) {
        height: 6px !important;
        background: #ffffff30 !important;
        border-radius: 6px !important;
        position: relative;
    }

    /* Slider handle */
    .stSlider > div > div > div:nth-child(3) {
        background: #ff4b4b !important;
        height: 16px !important;
        width: 16px !important;
        border-radius: 50% !important;
        top: -5px !important;
        z-index: 2;
        position: relative;
    }

    /* Display value above the slider handle */
    .stSlider p {
        color: #fff !important;
        font-weight: 500;
        background: rgba(0, 0, 0, 0.5);
        padding: 2px 6px;
        border-radius: 5px;
        position: absolute !important;
        top: -25px !important;
        z-index: 5;
        font-size: 0.9rem;
    }

    /* Avoid overlapping values */
    .stSlider > div > div > div:nth-child(3):hover + p {
        visibility: visible;
        opacity: 1;
    }

    /* Input styling */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stSelectbox > div > div:hover {
        border-color: rgba(255, 255, 255, 0.2);
        background-color: rgba(255, 255, 255, 0.07);
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        background: rgba(255, 255, 255, 0.08);
        color: white;
        padding: 0.8rem 1.5rem;
        font-size: 1.2rem;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
        backdrop-filter: blur(10px);
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border-color: rgba(255, 255, 255, 0.15);
    }
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    /* Risk indicators */
    .risk-container {
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .risk-container:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .high-risk {
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.1) 0%, rgba(255, 75, 75, 0.05) 100%);
        border: 1px solid rgba(255, 75, 75, 0.3);
    }
    .low-risk {
        background: linear-gradient(135deg, rgba(0, 207, 134, 0.1) 0%, rgba(0, 207, 134, 0.05) 100%);
        border: 1px solid rgba(0, 207, 134, 0.3);
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: rgba(255, 255, 255, 0.2);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .streamlit-expanderHeader:hover {
        background-color: rgba(255, 75, 75, 0.1);
        border-color: rgba(255, 75, 75, 0.3);
    }

    /* Help text */
    .help-text {
        color: #9ca3af;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-top: 0.5rem;
    }

    /* Disclaimer */
    .disclaimer {
        background: linear-gradient(135deg, rgba(255, 243, 205, 0.05) 0%, rgba(255, 243, 205, 0.02) 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 243, 205, 0.1);
        margin-top: 2rem;
    }
    .disclaimer p {
        color: #ffd700;
        margin: 0;
        font-size: 0.9rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Load the model, scaler, and feature names
@st.cache_resource
def load_model():
    with open('knn_model.pkl', 'rb') as f:
        knn, scaler = pickle.load(f)
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    return knn, scaler, feature_names

def main():
    # Header
    st.markdown("""
        <div class="title-container">
            <div class="title-text">CardioSense AI</div>
            <div class="subtitle-text">Advanced Heart Disease Risk Assessment</div>
        </div>
    """, unsafe_allow_html=True)

    try:
        knn, scaler, feature_names = load_model()
    except FileNotFoundError:
        st.error("⚠️ Model files not found. Please ensure the model is properly trained.")
        return

    # Create three columns with custom widths
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("""
            <div class="card">
                <div class="section-header">
                    👤 Personal Information
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            age = st.slider("Age", 20, 100, 50,
                          help="Enter your age in years")
            sex = st.selectbox("Biological Sex", ["Male", "Female"],
                             help="Select your biological sex")

        st.markdown("""
            <div class="card">
                <div class="section-header">
                    💓 Heart Health
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            trestbps = st.slider("Resting Blood Pressure (mm Hg)", 90, 200, 120,
                               help="Your resting blood pressure in millimeters of mercury")

    with col2:
        st.markdown("""
            <div class="card">
                <div class="section-header">
                    🩺 Clinical Measurements
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            chol = st.slider("Cholesterol (mg/dl)", 100, 600, 250,
                           help="Your serum cholesterol level in mg/dl")
            thalach = st.slider("Maximum Heart Rate", 70, 220, 150,
                              help="Maximum heart rate achieved during exercise")

    with col3:
        st.markdown("""
            <div class="card">
                <div class="section-header">
                    😣 Symptoms
                </div>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            cp = st.selectbox("Chest Pain Type",
                            ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"],
                            help="Type of chest pain you experience")
            exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"],
                               help="Do you experience chest pain during exercise?")

            with st.expander("ℹ️ Understanding Chest Pain Types"):
                st.markdown("""
                    - **Typical Angina**: Classic heart-related chest pain
                    - **Atypical Angina**: Unusual pattern of chest pain
                    - **Non-anginal Pain**: Not heart-related chest pain
                    - **Asymptomatic**: No chest pain
                """)

    # Center the predict button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🔍 Analyze Risk")

    if predict_button:
        # Create input data
        input_data = {
            'age': age,
            'sex': 1 if sex == "Male" else 0,
            'trestbps': trestbps,
            'chol': chol,
            'thalach': thalach,
            'exang': 1 if exang == "Yes" else 0
        }

        # Add one-hot encoded features for chest pain
        cp_map = {"Typical Angina": 1, "Atypical Angina": 2, "Non-anginal Pain": 3, "Asymptomatic": 4}
        cp_val = cp_map[cp]
        for i in range(1, 5):
            input_data[f'cp_{i}'] = 1 if cp_val == i else 0

        # Prepare and scale input data
        input_df = pd.DataFrame([{name: input_data.get(name, 0) for name in feature_names}])
        input_scaled = scaler.transform(input_df)

        # Make prediction
        prediction = knn.predict(input_scaled)
        prediction_proba = knn.predict_proba(input_scaled)[0]

        # Display results
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="card">
                <div class="section-header">
                    📊 Analysis Results
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Create columns for results
        res_col1, res_col2 = st.columns([1, 2])

        with res_col1:
            if prediction[0] == 1:
                st.markdown("""
                    <div class="risk-container high-risk">
                        <h2 style="color: #ff4b4b; margin: 0;">⚠️ High Risk</h2>
                        <p style="color: #ff4b4b; margin: 0;">Elevated Heart Disease Risk Detected</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="risk-container low-risk">
                        <h2 style="color: #00cf86; margin: 0;">✅ Low Risk</h2>
                        <p style="color: #00cf86; margin: 0;">Normal Heart Disease Risk Level</p>
                    </div>
                """, unsafe_allow_html=True)

        with res_col2:
            risk_probability = prediction_proba[1]
            st.markdown(f"""
                <div style='margin-bottom: 1rem;'>
                    <span style='font-size: 1.2rem; font-weight: 600;'>Risk Probability:</span>
                    <span style='font-size: 1.5rem; font-weight: 700; color: {"#ff4b4b" if risk_probability > 0.5 else "#00cf86"};'>
                        {risk_probability:.1%}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            st.progress(risk_probability)

            with st.expander("📋 Detailed Analysis"):
                if prediction[0] == 1:
                    st.markdown("""
                        ### Key Recommendations:
                        1. 👨‍⚕️ Schedule a consultation with a cardiologist
                        2. 📊 Monitor your vital signs regularly
                        3. ❤️ Consider lifestyle modifications
                        4. 🏃‍♂️ Start a supervised exercise program
                        5. 🥗 Follow a heart-healthy diet plan
                    """)
                else:
                    st.markdown("""
                        ### Maintain Your Heart Health:
                        1. 🏃‍♂️ Regular cardiovascular exercise
                        2. 🥗 Mediterranean or DASH diet
                        3. 😴 7-9 hours of quality sleep
                        4. 🧘‍♂️ Daily stress management
                        5. 🏥 Annual health check-ups
                    """)

    # Disclaimer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="disclaimer">
            <p>
                ⚠️ <strong>Medical Disclaimer:</strong> CardioSense AI is designed for educational and informational purposes only.
                The results should not be considered as medical advice. Always consult qualified healthcare professionals for
                proper medical evaluation and advice.
            </p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
