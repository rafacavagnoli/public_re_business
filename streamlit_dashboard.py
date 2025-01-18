import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the data
data_path = "Extracted_Towns_and_Counties.xlsx"
data = pd.read_excel(data_path)

# Filter the data based on user input
st.title("Real Estate Towns Dashboard")
st.sidebar.header("Filter Options")

# Adding filters for counties
county_filter = st.sidebar.multiselect("Select Counties:", options=data["County"].unique(), default=data["County"].unique())

# Adding filters for bedroom prices
price_1b_filter = st.sidebar.slider("Max Price for 1-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)
price_2b_filter = st.sidebar.slider("Max Price for 2-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)
price_3b_filter = st.sidebar.slider("Max Price for 3-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)

# Adding filter for commute time
commute_time_filter = st.sidebar.slider("Max Commute Time (mins):", min_value=0, max_value=120, value=120, step=5)

# Applying filters
data_filtered = data[
    (data["County"].isin(county_filter)) &
    (data["Asking Price 1b"] <= price_1b_filter) &
    (data["Asking Price 2b"] <= price_2b_filter) &
    (data["Asking Price 3b"] <= price_3b_filter) &
    (data["Commute Time (mins)"] <= commute_time_filter)
]

st.write("### Filtered Towns")
st.dataframe(data_filtered)

# Plot Town Distribution by County
st.write("### Town Distribution by County")
fig, ax = plt.subplots()
data_filtered["County"].value_counts().plot(kind="bar", ax=ax, color="skyblue")
ax.set_title("Town Count by County")
ax.set_xlabel("County")
ax.set_ylabel("Number of Towns")
st.pyplot(fig)

# Adding a map visualization if latitude and longitude are available
if "Latitude" in data.columns and "Longitude" in data.columns:
    st.write("### Map of Filtered Towns")
    fig = px.scatter_mapbox(
        data_filtered,
        lat="Latitude",
        lon="Longitude",
        hover_name="Town",
        hover_data={"County": True, "Commute Time (mins)": True},
        color="County",
        size_max=15,
        zoom=8,
        height=500
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)

# Adding a scatter plot for price vs commute time
st.write("### Price vs Commute Time")
fig = px.scatter(
    data_filtered,
    x="Commute Time (mins)",
    y="Asking Price 2b",
    color="County",
    hover_name="Town",
    title="Price vs Commute Time for 2-Bedroom Properties",
    labels={"Commute Time (mins)": "Commute Time (mins)", "Asking Price 2b": "Asking Price (£)"}
)
st.plotly_chart(fig)

# Adding analysis: Average asking price by county
st.write("### Average Asking Price by County")
avg_prices = data_filtered.groupby("County")["Asking Price 2b"].mean().sort_values()
st.bar_chart(avg_prices)

st.write("### Towns List")
st.write("Below is the list of towns based on your selection:")
for town in data_filtered["Town"].unique():
    st.write(f"- {town}")
