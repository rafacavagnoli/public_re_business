import streamlit as st
import pandas as pd

# Load Data
file_path = "dashboard_london_fully_cleaned.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Display number of places
st.title("London Real Estate Data Overview")
st.write(f"Number of places in dataset: {df.shape[0]}")

# Show raw data
st.subheader("Dataset Preview")
st.dataframe(df.head())
