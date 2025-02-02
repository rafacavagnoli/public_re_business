import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
file_path = "dashboard_london_fully_cleaned.csv"
df = pd.read_csv(file_path)
df.columns = [col.strip() for col in df.columns]

# Sidebar Filters
st.sidebar.header("Filters")
towns = ['All'] + df['Town'].dropna().unique().tolist()
regions = ['All'] + df['Region'].dropna().unique().tolist()
selected_town = st.sidebar.selectbox("Select a Town", towns)
selected_region = st.sidebar.selectbox("Select a Region", regions)

# New Filter: Number of Bedrooms
bedroom_options = ['1 Bedroom', '2 Bedroom', '3 Bedroom', '4 Bedroom']
selected_bedroom = st.sidebar.selectbox("Select Number of Bedrooms", bedroom_options)

# Map Bedroom Selection to House Price Column
bedroom_column_map = {
    '1 Bedroom': 'Av. Asking Price 1b',
    '2 Bedroom': 'Av. Asking Price 2b',
    '3 Bedroom': 'Av. Asking Price 3b',
    '4 Bedroom': 'Av. Asking Price 4b'
}
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

# Filter Data Based on Selection
filtered_df = df.copy()
if selected_town != 'All':
    filtered_df = filtered_df[filtered_df['Town'] == selected_town]
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_price_column in filtered_df.columns:
    filtered_df = filtered_df[(filtered_df[selected_price_column] >= min_price) & (filtered_df[selected_price_column] <= max_price)]

# Dashboard Title
st.title("London Real Estate Dashboard")

# Key Metrics
st.subheader("Key Metrics")
st.metric(label="Population (2021)", value=f"{filtered_df['Population (1,000s) (2021)'].values[0] * 1000:,.0f}" if not filtered_df.empty else "N/A")
st.metric(label="Average House Price (2019)", value=f"£{filtered_df[selected_price_column].values[0]:,.0f}" if (not filtered_df.empty and selected_price_column in filtered_df.columns) else "N/A")

# Rental Price Bar Chart
st.subheader("Average Rental Prices by Bedroom Count")
if all(col in filtered_df.columns for col in ['Av. Asking Price 1b', 'Av. Asking Price 2b', 'Av. Asking Price 3b', 'Av. Asking Price 4b']):
    rental_df = filtered_df[['Av. Asking Price 1b', 'Av. Asking Price 2b', 'Av. Asking Price 3b', 'Av. Asking Price 4b']]
    rental_df.columns = ['1 Bedroom', '2 Bedroom', '3 Bedroom', '4 Bedroom']
    rental_melted = rental_df.melt(var_name="Bedroom Count", value_name="Price")
    fig_rental = px.bar(rental_melted, x='Bedroom Count', y='Price', title="Asking Prices by Bedroom Count")
    st.plotly_chart(fig_rental)
else:
    st.write("Warning: Rental price columns are missing from the dataset.")

# Scatter Plot: House Price vs. Yield
st.subheader("House Price vs. Yield")
fig_yield = px.scatter(df, x='Av. House Price (2019)', y='Av. UL Yield (2b)', hover_data=['Town'], title="House Price vs Yield")
st.plotly_chart(fig_yield)

# Ranking Table
st.subheader("Ranking Table")
st.dataframe(filtered_df[['Town', 'Rank', 'Rank 2019 (Totallymoney)', 'Rank Green Space (Telegr. 2024)']].sort_values(by='Rank'))

# Run with: streamlit run dashboard.py
