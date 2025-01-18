import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
data_path = "Extracted_Towns_and_Counties.xlsx"
data = pd.read_excel(data_path)

# Filter the data based on user input
st.title("UK Real Estate Dashboard")
st.sidebar.header("Filter Options")

# Important filters at the top
price_2b_filter = st.sidebar.slider("Max Price for 2-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)
commute_time_filter = st.sidebar.slider("Max Commute Time (mins):", min_value=0, max_value=120, value=120, step=5)
county_filter = st.sidebar.multiselect("Select Counties:", options=data["County"].unique(), default=data["County"].unique())

# Additional filters for other bedroom prices
price_1b_filter = st.sidebar.slider("Max Price for 1-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)
price_3b_filter = st.sidebar.slider("Max Price for 3-Bedroom (£):", min_value=0, max_value=500000, value=500000, step=5000)

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
    # Layout for visual appeal
    col1, col2 = st.columns(2)

    # Town Distribution by County
    with col1:
        st.write("### Town Distribution by County")
        fig = px.bar(
            data_filtered["County"].value_counts().reset_index(name="Number of Towns"),
            x="index", y="Number of Towns",
            labels={"index": "County"},
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
    avg_prices = data_filtered.groupby("County", as_index=False)["Asking Price 2b"].mean()
    fig = px.bar(
        avg_prices,
        x="County", y="Asking Price 2b",
        labels={"Asking Price 2b": "Average Asking Price (£)"},
        title="Average Asking Price by County",
        color_discrete_sequence=["salmon"]
    )
    st.plotly_chart(fig)
