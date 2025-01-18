import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

st.write("### Towns List")
st.write("Below is the list of towns based on your selection:")
for town in data_filtered["Town"].unique():
    st.write(f"- {town}")
