import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model and scaler
model = joblib.load("dos_model.pkl")
scaler = joblib.load("scaler.pkl")

st.set_page_config(page_title="DoS Detection", layout="centered")

st.title("🚨 DoS Attack Detection System")
st.markdown("Detect whether network traffic is **Normal** or a **DoS Attack** using Machine Learning.")

# ---- Feature Names (important for clarity) ----
feature_names = [
'duration','protocol_type','service','flag','src_bytes','dst_bytes','land',
'wrong_fragment','urgent','hot','num_failed_logins','logged_in',
'num_compromised','root_shell','su_attempted','num_root','num_file_creations',
'num_shells','num_access_files','num_outbound_cmds','is_host_login',
'is_guest_login','count','srv_count','serror_rate','srv_serror_rate',
'rerror_rate','srv_rerror_rate','same_srv_rate','diff_srv_rate',
'srv_diff_host_rate','dst_host_count','dst_host_srv_count',
'dst_host_same_srv_rate','dst_host_diff_srv_rate',
'dst_host_same_src_port_rate','dst_host_srv_diff_host_rate',
'dst_host_serror_rate','dst_host_srv_serror_rate',
'dst_host_rerror_rate','dst_host_srv_rerror_rate'
]

# ---- Input Option ----
st.subheader("🔢 Input Method")

input_option = st.radio("Choose input method:", ["Manual Input", "Paste Full Input", "Use Sample Data"])

# ---- Manual Input (simplified numeric only) ----
if input_option == "Manual Input":
    st.write("Enter some important features (demo purpose):")

    duration = st.number_input("duration", value=0)
    src_bytes = st.number_input("src_bytes", value=0)
    dst_bytes = st.number_input("dst_bytes", value=0)
    count = st.number_input("count", value=0)

    if st.button("Predict"):
        st.warning("⚠ For full accuracy, use 'Paste Full Input' or 'Sample Data'")

# ---- Paste Full Input ----
elif input_option == "Paste Full Input":
    user_input = st.text_area("Paste 41 features (comma separated):")

    if st.button("Predict"):
        try:
            data = list(map(float, user_input.split(',')))

            if len(data) != 41:
                st.error("❌ Please enter exactly 41 values")
            else:
                data = np.array(data).reshape(1, -1)
                data = scaler.transform(data)

                prediction = model.predict(data)

                if prediction[0] == 0:
                    st.success("✅ Normal Traffic")
                else:
                    st.error("🚨 DoS Attack Detected")

        except:
            st.error("❌ Invalid input format")

# ---- Sample Data ----
elif input_option == "Use Sample Data":

    sample_data = [
        0,0,0,0,491,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,1,0,0,150,25,0.17,0.03,0.17,0.00,0.00,0.05,0.00,0.00
    ]

    st.write("Click below to test with sample data:")

    if st.button("Run Sample Prediction"):
        data = np.array(sample_data).reshape(1, -1)
        data = scaler.transform(data)

        prediction = model.predict(data)

        st.write("### Result:")
        if prediction[0] == 0:
            st.success("✅ Normal Traffic")
        else:
            st.error("🚨 DoS Attack Detected")

# ---- Footer ----
st.markdown("---")
st.markdown("💡 Model: Random Forest | Accuracy: ~99%")