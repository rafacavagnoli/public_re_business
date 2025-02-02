import streamlit as st
import pandas as pd

# Load Data
file_path = "dashboard_london_fully_cleaned.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Sidebar Filter
st.sidebar.header("Filters")
selected_bedrooms = st.sidebar.multiselect("Select Number of Bedrooms", ["1 Bedroom", "2 Bedroom", "3 Bedroom", "4 Bedroom"], default=["1 Bedroom", "2 Bedroom", "3 Bedroom", "4 Bedroom"])

# Mapping bedroom selection to column
bedroom_columns = {
    "1 Bedroom": "Av. Asking Price 1b",
    "2 Bedroom": "Av. Asking Price 2b",
    "3 Bedroom": "Av. Asking Price 3b",
    "4 Bedroom": "Av. Asking Price 4b"
}

# Filter Data
selected_columns = [bedroom_columns[bedroom] for bedroom in selected_bedrooms if bedroom in bedroom_columns and bedroom_columns[bedroom] in df.columns]
if not selected_columns:
    selected_columns = list(bedroom_columns.values())  # Default to all columns if none are selected
if selected_columns:
    selected_columns = [bedroom_columns[bedroom] for bedroom in selected_bedrooms if bedroom in bedroom_columns]
    df = df.loc[:, ["Town", "Region", "Population (1,000s) (2021)"] + selected_columns] if selected_columns else df

# Display number of places
st.title("London Real Estate Data Overview")
st.write(f"Number of places in dataset: {df.shape[0]}")

# Calculate average asking prices
st.subheader("Average Asking Prices")

# Calculate overall average asking price
all_prices = [df[col].mean() for col in bedroom_columns.values() if col in df.columns]
overall_avg_price = sum(all_prices) / len(all_prices) if all_prices else 0
st.write(f"Overall Average Asking Price: £{overall_avg_price:,.0f}")
for label, column in bedroom_columns.items():
    if column in df.columns:
        avg_price = df[column].mean()
        st.write(f"{label}: £{avg_price:,.0f}")
    else:
        st.write(f"{label}: Data not available")
