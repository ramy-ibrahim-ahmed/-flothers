import pandas as pd
import streamlit as st
from joblib import load
from xgboost import XGBClassifier
from feature_extractor import feature_extraction_pipeline, non_binary_columns
from sqlite_db import *

scaler = load(r"scaler_v1.pkl")

xgb_model_loaded = XGBClassifier()
xgb_model_loaded.load_model(r"xgb_model_v1.ubj")

db_name = "urls.db"

st.title("URL Malware Recognizer")

# Add a selectbox for choosing the method
use_ml = st.sidebar.selectbox("Choose method:", ["Machine Learning", "Whitelist"])

# Sidebar for adding URLs to whitelist
if use_ml == "Whitelist":

    # conn = connect_db(db_name)
    # wight_list = retrieve_wight_list(conn=conn)
    # st.sidebar.header("Whitelist")
    # st.sidebar.write("The following URLs are in the whitelist:")
    # st.sidebar.write(f"{url} \n" for url in wight_list)

    st.sidebar.header("Manage Whitelist")
    with st.sidebar.form(key="add_url_form"):
        url_to_add = st.text_input("Add URL to whitelist:")
        submit_button = st.form_submit_button("Add URL")

        if submit_button and url_to_add:
            conn = connect_db(db_name)
            add_url(conn, url_to_add)
            conn.close()
            st.sidebar.success(f'URL "{url_to_add}" added to whitelist.')
            # Refresh the whitelist display
            st.session_state.refresh_whitelist = True

    # Display the whitelist in the sidebar
    if "refresh_whitelist" in st.session_state and st.session_state.refresh_whitelist:
        conn = connect_db(db_name)
        wight_list = retrieve_wight_list(conn=conn)
        conn.close()
        st.session_state.wight_list = wight_list
        st.session_state.refresh_whitelist = False
    else:
        # Fetch from session state if not refreshing
        wight_list = st.session_state.get("wight_list", [])

url_input = st.text_input("Enter URL:", "")

if st.button("Analyze"):
    if url_input:
        if use_ml == "Machine Learning":
            # Extract features
            features = feature_extraction_pipeline(url_input)
            df = pd.DataFrame([features])

            # Scale
            non_binary_numerical_columns = non_binary_columns()
            df[non_binary_numerical_columns] = df[non_binary_numerical_columns].astype(
                float
            )
            df[non_binary_numerical_columns] = scaler.transform(
                df[non_binary_numerical_columns]
            )

            # Predict
            prediction = xgb_model_loaded.predict(df)
            prediction_proba = xgb_model_loaded.predict_proba(df)

            if prediction[0] == 1:
                st.error("This URL is predicted to be malicious.")
            else:
                st.success("This URL is predicted to be benign.")

            # Format and display prediction probabilities
            malware_proba = prediction_proba[0][1] * 100
            benign_proba = prediction_proba[0][0] * 100
            st.write(f"Probability of being malicious: {malware_proba:.2f}%")
            st.write(f"Probability of being benign: {benign_proba:.2f}%")

        elif use_ml == "Whitelist":
            # Check whitelist
            if url_input in wight_list:
                st.success("This URL is in the whitelist and allowed to use.")
            else:
                st.error("This URL is not in the whitelist, it may be dangerous!!")

    else:
        st.error("Please enter a URL.")

# pyinstaller --noconsol --additional-hooks-dir=hooks app.py
