import streamlit as st
import pandas as pd
import pickle

# Set page config must be the first Streamlit command
st.set_page_config(
    page_title="Cardio Sense",
    page_icon="❤️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background and text colors */
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }

    /* Slider styling */
    .stSlider {
        padding: 1rem 0;
    }
    .stSlider > div > div > div {
        background-color: #ff4b4b !important;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #262730;
        border: 1px solid #464855;
        color: #fafafa;
    }
    .stSelectbox > div > div:hover {
        border: 1px solid #ff4b4b;
    }

    /* Button styling */
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.3);
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background-color: #ff4b4b;
    }

    /* Risk indicators */
    .risk-high {
        color: #ff4b4b;
        font-size: 24px;
        font-weight: bold;
    }
    .risk-low {
        color: #00cf86;
        font-size: 24px;
        font-weight: bold;
    }

    /* Containers and cards */
    .css-1d391kg, .stMarkdown, .stExpander {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #464855;
    }

    /* Headers */
    h1, h2, h3 {
        color: #fafafa !important;
        font-weight: 600;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #262730;
        color: #fafafa;
        border: 1px solid #464855;
    }
    .streamlit-expanderHeader:hover {
        border-color: #ff4b4b;
    }

    /* Disclaimer box */
    .disclaimer {
        background-color: #262730;
        border: 1px solid #464855;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 2rem;
    }

    /* Help text */
    .stMarkdown div.help-text {
        color: #9ca3af;
        font-size: 0.875rem;
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
    # Header with icon and description
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #ff4b4b;'>❤️ Heart Disease Risk Predictor</h1>
        <p style='color: #666; font-size: 18px;'>
            Enter your health information below to assess your heart disease risk
        </p>
    </div>
    """, unsafe_allow_html=True)

    try:
        knn, scaler, feature_names = load_model()
    except FileNotFoundError:
        st.error("Model files not found. Please run heart_disease_knn.py first.")
        return

    # Create three columns for better organization
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("### 👤 Personal Information")
        age = st.slider("Age", 20, 100, 50, help="Enter your age in years")
        sex = st.selectbox("Sex", ["Male", "Female"], help="Select your biological sex")

        st.markdown("### 💓 Heart Health")
        trestbps = st.slider("Resting Blood Pressure (mm Hg)", 90, 200, 120,
                           help="Your resting blood pressure in millimeters of mercury")
        thalach = st.slider("Maximum Heart Rate", 70, 220, 150,
                          help="Maximum heart rate achieved during exercise")

    with col2:
        st.markdown("### 🩸 Blood Work")
        chol = st.slider("Cholesterol (mg/dl)", 100, 600, 250,
                       help="Your serum cholesterol level in mg/dl")

        st.markdown("### 🏃 Exercise Response")
        exang = st.selectbox("Exercise Induced Angina", ["No", "Yes"],
                          help="Do you experience chest pain during exercise?")

    with col3:
        st.markdown("### 😣 Symptoms")
        cp = st.selectbox("Chest Pain Type",
                         ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"],
                         help="Type of chest pain you experience")

        # Add a visual guide for chest pain types
        with st.expander("Chest Pain Type Guide"):
            st.markdown("""
            - **Typical Angina**: Chest pain caused by reduced blood flow to the heart
            - **Atypical Angina**: Chest pain not meeting typical angina criteria
            - **Non-anginal Pain**: Chest pain not related to the heart
            - **Asymptomatic**: No chest pain experienced
            """)

    # Center the predict button
    st.markdown("<div style='text-align: center; margin: 20px 0;'>", unsafe_allow_html=True)
    predict_button = st.button("🔍 Predict Heart Disease Risk")
    st.markdown("</div>", unsafe_allow_html=True)

    if predict_button:
        input_data = {
            'age': age,
            'sex': 1 if sex == "Male" else 0,
            'trestbps': trestbps,
            'chol': chol,
            'thalach': thalach,
            'exang': 1 if exang == "Yes" else 0
        }

        cp_map = {"Typical Angina": 1, "Atypical Angina": 2, "Non-anginal Pain": 3, "Asymptomatic": 4}
        cp_val = cp_map[cp]
        for i in range(1, 5):
            input_data[f'cp_{i}'] = 1 if cp_val == i else 0

        input_df = pd.DataFrame([{name: input_data.get(name, 0) for name in feature_names}])
        input_scaled = scaler.transform(input_df)

        prediction = knn.predict(input_scaled)
        prediction_proba = knn.predict_proba(input_scaled)[0]

        # Results section with better styling
        st.markdown("---")
        st.markdown("## 📊 Prediction Results")

        # Create a container for results
        with st.container():
            col1, col2 = st.columns([1, 2])

            with col1:
                if prediction[0] == 1:
                    st.markdown('<p class="risk-high">⚠️ At Risk of Heart Disease</p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p class="risk-low">✅ Not at Risk of Heart Disease</p>', unsafe_allow_html=True)

            with col2:
                risk_probability = prediction_proba[1]
                st.write(f"Risk Probability: {risk_probability:.2%}")
                st.progress(risk_probability)

                # Add interpretation guide
                with st.expander("What does this mean?"):
                    if prediction[0] == 1:
                        st.markdown("""
                        **You may be at risk of heart disease.** Consider:
                        - Consulting with a healthcare professional
                        - Reviewing your lifestyle choices
                        - Regular health check-ups
                        """)
                    else:
                        st.markdown("""
                        **You appear to be at low risk of heart disease.** Continue to:
                        - Maintain a healthy lifestyle
                        - Exercise regularly
                        - Eat a balanced diet
                        """)

        # Update the disclaimer styling
        st.markdown("""
        <div class='disclaimer'>
            <p style='color: #9ca3af; margin: 0;'>
                ⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only and should not be used as a substitute for professional medical advice.
            </p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
