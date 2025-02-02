import streamlit as st
import pandas as pd

# Load Data
file_path = "dashboard_london_fully_cleaned.csv"
df = pd.read_csv(file_path)

# Clean column names
df.columns = [col.strip() for col in df.columns]

# Sidebar Filters
st.sidebar.header("Filters")
selected_bedrooms = st.sidebar.slider("Select Number of Bedrooms", 1, 4, (1, 4))

# Mapping bedroom selection to column
bedroom_columns = {
    1: "Av. Asking Price 1b",
    2: "Av. Asking Price 2b",
    3: "Av. Asking Price 3b",
    4: "Av. Asking Price 4b"
}

# Get selected columns based on bedroom slider
selected_columns = [bedroom_columns[i] for i in range(selected_bedrooms[0], selected_bedrooms[1] + 1) if i in bedroom_columns and bedroom_columns[i] in df.columns]

# Keep relevant columns in filtered DataFrame
filtered_df = df[['Town', 'Region'] + selected_columns]

# Price Range Slider
if not filtered_df.empty and selected_columns:
    min_price = int(filtered_df[selected_columns].min().min())
    max_price = int(filtered_df[selected_columns].max().max())
    selected_price = st.sidebar.slider("Select Asking Price Range", min_price, max_price, (min_price, max_price))
    
    # Apply price filtering
    filtered_df = filtered_df[(filtered_df[selected_columns] >= selected_price[0]) & (filtered_df[selected_columns] <= selected_price[1])]

# Display number of places
st.title("London Real Estate Data Overview")
if filtered_df.empty:
    st.write("No properties match the selected filters.")
else:
    st.write(f"Number of places in dataset: {filtered_df.shape[0]}")

# Calculate overall average asking price
if not filtered_df.empty and selected_columns:
    overall_avg_price = filtered_df[selected_columns].mean().mean()
    st.subheader("Average Asking Price")
    st.write(f"Overall Average Asking Price: £{overall_avg_price:,.0f}")
