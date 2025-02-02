import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
file_path = "dashboard_london.csv"  # Ensure correct path
df = pd.read_csv(file_path)
df.columns = [col.strip() for col in df.columns]

# Cleaning Data - Fix Non-Numeric Conversion Issues
columns_to_clean = ['Av. House Price (2019)', 'Av. Rental \nPrice 1b', 'Av. Rental \nPrice 2b', 'Av. Rental \nPrice 3b']
for col in columns_to_clean:
    df[col] = pd.to_numeric(df[col].replace('[^0-9.]', '', regex=True), errors='coerce')

# Sidebar Filters
st.sidebar.header("Filters")

towns = ['All'] + df['Town'].dropna().unique().tolist()
regions = ['All'] + df['Region'].dropna().unique().tolist()

selected_town = st.sidebar.selectbox("Select a Town", towns)
selected_region = st.sidebar.selectbox("Select a Region", regions)

# New Filter: Number of Bedrooms
bedroom_options = ['1 Bedroom', '2 Bedroom', '3 Bedroom']
selected_bedroom = st.sidebar.selectbox("Select Number of Bedrooms", bedroom_options)

# Map Bedroom Selection to House Price Column
bedroom_column_map = {
    '1 Bedroom': 'Av. Asking Price 1b'.replace('
', ' ').strip(),
    '2 Bedroom': 'Av. Asking Price 2b'.replace('
', ' ').strip(),
    '3 Bedroom': 'Av. Asking Price 3b'.replace('
', ' ').strip()
}
selected_price_column = bedroom_column_map[selected_bedroom]
selected_price_column = bedroom_column_map[selected_bedroom]

# New Filter: House Price Range Based on Bedroom Type
if selected_price_column in df.columns:
    min_price, max_price = st.sidebar.slider(
        "Select House Price Range", 
        int(df[selected_price_column].min()), 
        int(df[selected_price_column].max()), 
        (int(df[selected_price_column].min()), int(df[selected_price_column].max()))
    )
else:
    min_price, max_price = 0, 0
    st.sidebar.write("Warning: Selected price column not found in data.")
