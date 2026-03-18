print("Hello from GitHub Codespaces")
print("today is a sunny day")

import streamlit as st
import pandas as pd

st.title("CSV File viewer")

df = pd.read_csv("trips_data_1000.csv")
st.write("Preview Uploaded data")
st.dataframe(df.head())

@st.cache_data
def load_data(): 
    df = pd.read_csv("datasets/trips_data_1000.csv")
    df['pickup_time'] = pd.to_datetime(df['pickup_time'])
    return df


