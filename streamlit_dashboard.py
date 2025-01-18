import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data_path = "Extracted_Towns_and_Counties_with_LatLong.xlsx"
data = pd.read_excel(data_path)

# Filter the data based on user input
st.title("UK Real Estate Dashboard")
st.sidebar.header("Filter Options")

# Important filters at the top
price_2b_filter = st.sidebar.slider("Max Price for 2-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)
commute_time_filter = st.sidebar.slider("Max Commute Time (mins):", min_value=0, max_value=120, value=120, step=5)
price_1b_filter = st.sidebar.slider("Max Price for 1-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)
price_3b_filter = st.sidebar.slider("Max Price for 3-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)
county_filter = st.sidebar.multiselect("Select Counties:", options=data["County"].unique(), default=data["County"].unique())

# Applying filters
data_filtered = data[
    (data["County"].isin(county_filter)) &
    (data["Asking Price 1b"] <= price_1b_filter) &
    (data["Asking Price 2b"] <= price_2b_filter) &
    (data["Asking Price 3b"] <= price_3b_filter) &
    (data["Commute Time (mins)"] <= commute_time_filter)
]

if data_filtered.empty:
    st.write("No data available for the selected filters.")
else:
    # Display the filtered data as a table
    st.write("### Filtered Towns")
    st.dataframe(data_filtered)

    # Layout for visual appeal
    col1, col2 = st.columns(2)

    # Town Distribution by County
    with col1:
        st.write("### Town Distribution by County")
        county_counts = data_filtered["County"].value_counts().reset_index()
        county_counts.columns = ["County", "Number of Towns"]
        fig = px.bar(
            county_counts,
            x="County", y="Number of Towns",
            labels={"County": "County", "Number of Towns": "Number of Towns"},
            title="Town Count by County",
            color_discrete_sequence=["skyblue"]
        )
        st.plotly_chart(fig)

    # Price vs Commute Time
    with col2:
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

    # Average Asking Price by County
    st.write("### Average Asking Price by County")
    avg_prices = data_filtered.groupby("County", as_index=False).agg({"Asking Price 2b": "mean"})
    fig = px.bar(
        avg_prices,
        x="County", y="Asking Price 2b",
        labels={"Asking Price 2b": "Average Asking Price (£)"},
        title="Average Asking Price by County",
        color_discrete_sequence=["salmon"]
    )
    st.plotly_chart(fig)

    # Median Asking Price by County
    st.write("### Median Asking Price by County")
    median_prices = data_filtered.groupby("County", as_index=False).agg({"Asking Price 2b": "median"})
    fig = px.bar(
        median_prices,
        x="County", y="Asking Price 2b",
        labels={"Asking Price 2b": "Median Asking Price (£)"},
        title="Median Asking Price by County",
        color_discrete_sequence=["orange"]
    )
    st.plotly_chart(fig)

    # Rental Yield Distribution
    st.write("### Rental Yield Distribution")
    data_filtered["Yield 2b"] = (data_filtered["Rental Price 2b"] * 12) / data_filtered["Asking Price 2b"] * 100
    fig = px.histogram(
        data_filtered,
        x="Yield 2b",
        nbins=20,
        labels={"Yield 2b": "Rental Yield (%)"},
        title="Rental Yield Distribution for 2-Bedroom Properties",
        color_discrete_sequence=["green"]
    )
    st.plotly_chart(fig)

    # Asking Price Distribution
    st.write("### Asking Price Distribution")
    fig = px.histogram(
        data_filtered,
        x="Asking Price 2b",
        nbins=20,
        labels={"Asking Price 2b": "Asking Price (£)"},
        title="Asking Price Distribution for 2-Bedroom Properties",
        color_discrete_sequence=["blue"]
    )
    st.plotly_chart(fig)

    # Map Visualization
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
            zoom=6,
            height=500
        )
        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
