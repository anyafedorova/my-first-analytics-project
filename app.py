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

import streamlit as st

st.title("My Streamlit Web App")

# Contents in a sidebar
with st.sidebar:
    st.header("This is a sidebar Section")
    user_input = st.text_input("Enter your name")
    option = st.selectbox("Choose an option", ["Choice A", "Choice B", "Choice C"])

# Contents in the main window
st.header("This is the main section")
# Display user input
st.write(f"Hello, {user_input}! You selected option {option}.")

# Adding Contents in multiple columns
col1, col2 = st.columns(2)
with col1:
    st.subheader("Column 1")
    st.button("Click me!")
    st.write("This is some text in column 1")

with col2:
    st.subheader("Column 2")

    st.line_chart({"data": [1, 5, 2, 6, 2, 1]})

    # Expandable section
with st.expander("See explanation"):
    st.write("This is an expandable section with additional information.")

    import pandas as pd
import numpy as np

st.title("Manipulate Streamlit Chart")

# Generate random data
bar_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.bar_chart(bar_data)

# Generate random data for line chart
line_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(line_data)

# Generate random data for scatter chart
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.scatter_chart(chart_data)



    