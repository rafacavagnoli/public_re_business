import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
file_path = "dashboard_london.csv"  # Ensure correct path
df = pd.read_csv(file_path)

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
    '1 Bedroom': 'Av. House Price (2019)',
    '2 Bedroom': 'Av. House Price (2019)',
    '3 Bedroom': 'Av. House Price (2019)'
}
selected_price_column = bedroom_column_map[selected_bedroom]bedroom_column_map = {
    '1 Bedroom': 'Av. Rental \nPrice 1b',
    '2 Bedroom': 'Av. Rental \nPrice 2b',
    '3 Bedroom': 'Av. Rental \nPrice 3b'
}
selected_price_column = bedroom_column_map[selected_bedroom]

# New Filter: House Price Range Based on Bedroom Type
min_price, max_price = st.sidebar.slider("Select House Price Range", int(df[selected_price_column].min()), int(df[selected_price_column].max()), (int(df[selected_price_column].min()), int(df[selected_price_column].max())))

filtered_df = df.copy()
if selected_town != 'All':
    filtered_df = filtered_df[filtered_df['Town'] == selected_town]
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
filtered_df = filtered_df[(filtered_df[selected_price_column] >= min_price) & (filtered_df[selected_price_column] <= max_price)]

# Dashboard Title
st.title("London Real Estate Dashboard")

# Key Metrics
st.subheader("Key Metrics")
st.metric(label="Population (2021)", value=filtered_df['Population (1,000s) (2021)'].values[0] if not filtered_df.empty else "N/A")

# Handle missing Commute Time column
time_column = 'Commute Time 2019 (mins)'
if time_column in filtered_df.columns and not filtered_df.empty:
    commute_time = filtered_df[time_column].values[0]
else:
    commute_time = "N/A"
st.metric(label="Average Commute Time (mins)", value=commute_time)

st.metric(label="Average House Price (2019)", value=f"\u00a3{filtered_df['Av. House Price (2019)'].values[0]:,.0f}" if not filtered_df.empty else "N/A")

# Rental Price Bar Chart
st.subheader("Average Rental Prices by Bedroom Count")
rental_df = filtered_df[['Av. Rental \nPrice 1b', 'Av. Rental \nPrice 2b', 'Av. Rental \nPrice 3b']]
rental_df.columns = ['1 Bedroom', '2 Bedroom', '3 Bedroom']
rental_melted = rental_df.melt(var_name="Bedroom Count", value_name="Price")
fig_rental = px.bar(rental_melted, x='Bedroom Count', y='Price', title="Rental Prices")

# Scatter Plot: House Price vs. Yield
st.subheader("House Price vs. Yield")
fig_yield = px.scatter(df, x='Av. House Price (2019)', y='Av. UL Yield (2b)', hover_data=['Town'], title="House Price vs Yield")

# Display Two Charts Side by Side
col1, col2 = st.columns(2)
col1.plotly_chart(fig_rental, use_container_width=True)
col2.plotly_chart(fig_yield, use_container_width=True)

# Additional Chart: Distribution of House Prices
st.subheader("Distribution of House Prices")
fig_hist = px.histogram(df, x='Av. House Price (2019)', nbins=30, title="House Price Distribution")
st.plotly_chart(fig_hist)

# Additional Chart: Commute Time vs House Price
st.subheader("Commute Time vs House Price")
if 'Commute Time 2019 (mins)' in df.columns and 'Av. House Price (2019)' in df.columns:
    df_filtered = df.dropna(subset=['Commute Time 2019 (mins)', 'Av. House Price (2019)'])
    if not df_filtered.empty:
        fig_commute = px.scatter(df_filtered, x='Commute Time 2019 (mins)', y='Av. House Price (2019)', hover_data=['Town'], title="Commute Time vs House Price")
    else:
        fig_commute = None
else:
    fig_commute = None

if fig_commute:
    st.plotly_chart(fig_commute)
else:
    st.write("Insufficient data available for Commute Time vs House Price chart.")
st.plotly_chart(fig_commute)

# Ranking Table
st.subheader("Ranking Table")
st.dataframe(filtered_df[['Town', 'Rank', 'Rank 2019 (Totallymoney)', 'Rank Green Space\n(Telegr. 2024)']].sort_values(by='Rank'))

# Run with: streamlit run dashboard.py
