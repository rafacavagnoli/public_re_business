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

# Calculate average asking prices
bedroom_columns = {
    "1 Bedroom": "Av. Asking Price 1b",
    "2 Bedroom": "Av. Asking Price 2b",
    "3 Bedroom": "Av. Asking Price 3b",
    "4 Bedroom": "Av. Asking Price 4b"
}

st.subheader("Average Asking Prices")
for label, column in bedroom_columns.items():
    if column in df.columns:
        avg_price = df[column].mean()
        st.write(f"{label}: £{avg_price:,.0f}")
    else:
        st.write(f"{label}: Data not available")

# Show raw data
st.subheader("Dataset Preview")
st.dataframe(df.head())
