
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data_path = "Extracted_Towns_and_Counties.xlsx"
data = pd.read_excel(data_path)

# Filter the data based on user input
st.title("Real Estate Towns Dashboard")
st.sidebar.header("Filter Options")

county_filter = st.sidebar.multiselect("Select Counties:", options=data["County"].unique(), default=data["County"].unique())
data_filtered = data[data["County"].isin(county_filter)]

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
