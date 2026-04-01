import streamlit as st
import numpy as np
import pickle

# Load model and scaler using pickle
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

st.set_page_config(page_title="DoS Detection", layout="centered")

st.title("🚨 DoS Attack Detection System")
st.markdown("Detect whether network traffic is **Normal** or a **DoS Attack** using Machine Learning.")

st.markdown("---")

# Input method selection
option = st.radio("Choose Input Method:", ["Use Sample Data", "Paste Full Input"])

# ---- SAMPLE DATA ----
if option == "Use Sample Data":

    sample_data = [
        0,0,0,0,491,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,1,0,0,150,25,0.17,0.03,0.17,0.00,0.00,0.05,0.00,0.00
    ]

    st.write("Click below to test with sample network traffic:")

    if st.button("Run Sample Prediction"):
        data = np.array(sample_data).reshape(1, -1)
        data = scaler.transform(data)

        prediction = model.predict(data)

        st.subheader("Result:")
        if prediction[0] == 0:
            st.success("✅ Normal Traffic")
        else:
            st.error("🚨 DoS Attack Detected")

# ---- USER INPUT ----
elif option == "Paste Full Input":

    user_input = st.text_area("Enter 41 features (comma separated):")

    if st.button("Predict"):
        try:
            values = list(map(float, user_input.split(',')))

            if len(values) != 41:
                st.error("❌ Please enter exactly 41 values")
            else:
                data = np.array(values).reshape(1, -1)
                data = scaler.transform(data)

                prediction = model.predict(data)

                st.subheader("Result:")
                if prediction[0] == 0:
                    st.success("✅ Normal Traffic")
                else:
                    st.error("🚨 DoS Attack Detected")

        except:
            st.error("❌ Invalid input format")

# Footer
st.markdown("---")
st.markdown("💡 Model: Random Forest | Accuracy: ~99%")
