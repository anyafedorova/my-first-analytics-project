print("Hello from GitHub Codespaces")
print("today is a sunny day")

import streamlit as st
import pandas as pd

st.title("trips_data_1000.csv")
upload_file = st.file_uploader("Upload a CVS file", type=["csv"])

if upload_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Data: ")
    st.dataframe(df.head())

st.sidebar.header("This is sidebar section")
