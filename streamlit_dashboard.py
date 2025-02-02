import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
file_path = "dashboard_london.csv"  # Ensure correct path
df = pd.read_csv(file_path)

# Cleaning Data - Fix Non-Numeric Conversion Issues
columns_to_clean = ['Av. House Price (2019)', 'Av. Rental \nPrice 1b']
for col in columns_to_clean:
    df[col] = pd.to_numeric(df[col].replace('[^0-9.]', '', regex=True), errors='coerce')

# Sidebar Filters
st.sidebar.header("Filters")
selected_town = st.sidebar.selectbox("Select a Town", df['Town'].dropna().unique())
selected_region = st.sidebar.selectbox("Select a Region", df['Region'].dropna().unique())

filtered_df = df[(df['Town'] == selected_town) & (df['Region'] == selected_region)]

# Dashboard Title
st.title("London Real Estate Dashboard")

# Key Metrics
st.subheader("Key Metrics")
st.metric(label="Population (2021)", value=filtered_df['Population (1,000s) (2021)'].values[0])
st.metric(label="Average Commute Time (mins)", value=filtered_df['Commute Time 2019 (mins)'].values[0])
st.metric(label="Average House Price (2019)", value=f"\u00a3{filtered_df['Av. House Price (2019)'].values[0]:,.0f}")

# Rental Price Bar Chart
st.subheader("Average Rental Prices by Bedroom Count")
rental_df = filtered_df[['Av. Rental \nPrice 1b', 'Av. Rental \nPrice 2b', 'Av. Rental \nPrice 3b']]
rental_df.columns = ['1 Bedroom', '2 Bedroom', '3 Bedroom']
rental_melted = rental_df.melt(var_name="Bedroom Count", value_name="Price")
fig_rental = px.bar(rental_melted, x='Bedroom Count', y='Price', title="Rental Prices")
st.plotly_chart(fig_rental)

# Scatter Plot: House Price vs. Yield
st.subheader("House Price vs. Yield")
fig_yield = px.scatter(df, x='Av. House Price (2019)', y='Av. UL Yield (2b)', hover_data=['Town'], title="House Price vs Yield")
st.plotly_chart(fig_yield)

# Ranking Table
st.subheader("Ranking Table")
st.dataframe(filtered_df[['Town', 'Rank', 'Rank 2019 (Totallymoney)', 'Rank Green Space\n(Telegr. 2024)']].sort_values(by='Rank'))

# Run with: streamlit run dashboard.py
