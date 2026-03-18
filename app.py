print("Hello from GitHub Codespaces")
print("today is a sunny day")

import streamlit as st
import pandas as pd

st.title("CSV File viewer")

df = pd.read_csv("trips_data_1000.csv")
st.write("Preview Uploaded data")
st.dataframe(df.head())

