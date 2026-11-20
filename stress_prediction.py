import pandas as pd
import datetime
import joblib
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Student Stress Predictor",
    page_icon="\U0001F338",
    layout="centered"
)

# Custom Pastel Aesthetic CSS (Dark Mode Proof)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif;
    }

    /* Soft pastel gradient background */
    .stApp {
        background: linear-gradient(135deg, #FFF5F7 0%, #F3E8FF 50%, #E0F7FA 100%);
    }

    /* Main glassmorphism card */
    .block-container {
        background-color: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 2.5rem 2.5rem 3rem 2.5rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(186, 156, 217, 0.25);
        border: 1.5px solid #F3E5F5;
    }

    /* Fix all input labels so they are clearly visible in Dark Mode too */
    label, .stSelectbox label, .stNumberInput label, .stSlider label, div[data-testid="stWidgetLabel"] p {
        color: #4A3B5C !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
    }

    /* Make input boxes & selectbox soft pastel instead of black */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    input[type="number"] {
        background-color: #FAF5FF !important;
        color: #3B2D4A !important;
        border: 1.5px solid #E1BEE7 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    /* Style +/- buttons inside number inputs */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background-color: #F3E5F5 !important;
        color: #6A4C93 !important;
        border-radius: 8px !important;
    }

    /* Slider min/max tick labels */
    div[data-testid="stTickBarMin"], div[data-testid="stTickBarMax"] {
        color: #6A4C93 !important;
        font-weight: 600 !important;
    }

    /* Header Banner */
    .pastel-header {
        background: linear-gradient(120deg, #F8BBD0 0%, #E1BEE7 50%, #B2EBF2 100%);
        padding: 1.8rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 18px rgba(225, 190, 231, 0.4);
    }
    .pastel-header h1 {
        color: #4A3B5C;
        font-weight: 700;
        font-size: 2.1rem;
        margin: 0;
    }
    .pastel-header p {
        color: #5E4B73;
        font-size: 1.05rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
        font-weight: 600;
    }

    /* Section subheadings */
    .section-title {
        color: #6A4C93;
        font-weight: 700;
        font-size: 1.15rem;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px dashed #E1BEE7;
    }

    /* Aesthetic Pastel Button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #F48FB1 0%, #CE93D8 100%);
        color: white !important;
        font-weight: 700;
        font-size: 1.15rem;
        border: none;
        border-radius: 16px;
        padding: 0.75rem 1.5rem;
        margin-top: 1.2rem;
        box-shadow: 0 6px 15px rgba(206, 147, 216, 0.45);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(244, 143, 177, 0.6);
        color: #FFF !important;
    }

    /* Custom Result Cards */
    .result-stressed {
        background-color: #FFEBEE;
        border-left: 6px solid #F48FB1;
        color: #880E4F;
        padding: 1.3rem;
        border-radius: 16px;
        margin-top: 1.2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(244, 143, 177, 0.2);
    }
    .result-calm {
        background-color: #E8F5E9;
        border-left: 6px solid #81C784;
        color: #1B5E20;
        padding: 1.3rem;
        border-radius: 16px;
        margin-top: 1.2rem;
        font-size: 1.1rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(129, 199, 132, 0.2);
    }
    </style>
""", unsafe_allow_html=True)


def main():
    # Load saved .pkl model
    model = joblib.load("stress_model.pkl")

    # Aesthetic Pastel Banner
    st.markdown(
        '<div class="pastel-header">'
        '<h1>\U0001F338 Student Stress Predictor</h1>'
        '<p>A gentle wellness check-in based on your daily study & lifestyle habits \u2728</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # 2-Column Clean Layout
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="section-title">\U0001F4DA Daily Routine</div>', unsafe_allow_html=True)
        s1 = st.selectbox("\U0001F393 Student Type", ("School", "College", "Working Student"))

        if s1 == 'School':
            p1 = 0
        elif s1 == 'College':
            p1 = 1
        else:
            p1 = 2

        p2 = st.number_input("\U0001F634 Sleep Hours / Day", 2.0, 10.0, 7.0, step=0.5)
        p3 = st.number_input("\U0001F4D6 Study Hours / Day", 0.0, 16.0, 4.0, step=0.5)
        p4 = st.number_input("\U0001F4F1 Social Media Hours / Day", 0.0, 10.0, 3.0, step=0.5)

    with col2:
        st.markdown('<div class="section-title">\U0001F337 Academic & Support</div>', unsafe_allow_html=True)
        p5 = st.number_input("\U0001F3EB Attendance (%)", 0.0, 100.0, 80.0, step=1.0)
        p6 = st.slider("\U0001F4DD Exam Pressure (1 = Low, 10 = High)", 1, 10, 5)
        p7 = st.slider("\U0001F3E1 Family Support (1 = Low, 10 = High)", 1, 10, 5)

        date_time = datetime.datetime.now()
        p8 = st.number_input("\U0001F5D3 Month (1 - 12)", 1, 12, date_time.month, step=1)

    # Prepare DataFrame for prediction
    data_new = pd.DataFrame({
        'Student_Type': p1,
        'Sleep_Hours': p2,
        'Study_Hours': p3,
        'Social_Media_Hours': p4,
        'Attendance': p5,
        'Exam_Pressure': p6,
        'Family_Support': p7,
        'Month': p8
    }, index=[0])

    # Predict Button
    if st.button("\u2728 Check Stress Level \u2728"):
        pred = model.predict(data_new)
        prob = model.predict_proba(data_new)[0][1] * 100

        if pred[0] == 1:
            st.markdown(
                f'<div class="result-stressed">'
                f'\U0001F497 <b>High Stress Detected ({prob:.1f}% probability)</b><br>'
                f'<span style="font-size:0.95rem; font-weight:500;">'
                f'Take a deep breath! Consider getting extra rest, taking short study breaks, and talking with someone you trust. \U0001F33F'
                f'</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.balloons()
            st.markdown(
                f'<div class="result-calm">'
                f'\U0001F340 <b>Low / No Stress ({prob:.1f}% stress probability)</b><br>'
                f'<span style="font-size:0.95rem; font-weight:500;">'
                f'Your daily routine looks well-balanced! Keep up the healthy sleep and study habits. \u2728'
                f'</span></div>',
                unsafe_allow_html=True
            )


if __name__ == '__main__':
    main()