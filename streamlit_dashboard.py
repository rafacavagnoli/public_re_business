import streamlit as st
import pandas as pd
import plotly.express as px

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
filtered_df = df.copy()

# Price Range Slider
if not filtered_df.empty and selected_columns:
    min_price = int(filtered_df[selected_columns].min().min())
    max_price = int(filtered_df[selected_columns].max().max())
    selected_price = st.sidebar.slider("Select Asking Price Range", min_price, max_price, (min_price, max_price))
    
    # Apply price filtering
    filtered_df = filtered_df.dropna(subset=selected_columns)
    filtered_df = filtered_df[(filtered_df[selected_columns] >= selected_price[0]) & (filtered_df[selected_columns] <= selected_price[1])]
    filtered_df = df.loc[filtered_df.index]

# Display number of places
st.title("London Real Estate Data Overview")
if filtered_df.empty:
    st.write(f"Number of places matching filters: {filtered_df.shape[0]}")
else:
    st.write(f"Number of places in dataset: {filtered_df.shape[0]}")

# Calculate overall average asking price
if not filtered_df.empty and selected_columns:
    overall_avg_price = filtered_df[selected_columns].mean().mean()
    st.subheader("Average Asking Price")
    st.write(f"Overall Average Asking Price: £{overall_avg_price:,.0f}")

# Generate Charts
if not filtered_df.empty:
    st.subheader("Data Visualizations")
    
    # Box plot of asking prices
    melted_df = filtered_df.melt(id_vars=['Town', 'Region'], value_vars=selected_columns, var_name='Bedroom Type', value_name='Asking Price')
    fig_box = px.box(melted_df, x='Bedroom Type', y='Asking Price', title='Asking Price Distribution by Bedroom Type')
    st.plotly_chart(fig_box)
    
    # Pie chart: Distribution of properties by region
    fig_pie = px.pie(df, names='Region', title='Distribution of Properties by Region')
    st.plotly_chart(fig_pie)
    
    # Heatmap: Correlation between asking prices
    price_corr = filtered_df[selected_columns].corr()
    fig_heatmap = px.imshow(price_corr, text_auto=True, title='Correlation Between Asking Prices')
    st.plotly_chart(fig_heatmap)
    
    # Violin plot: Asking price distribution
    fig_violin = px.violin(melted_df, x='Bedroom Type', y='Asking Price', box=True, points='all', title='Asking Price Spread by Bedroom Type')
    st.plotly_chart(fig_violin)
    
    # Bar chart: Count of properties by region
    region_counts = filtered_df['Region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Count']
    fig_bar_region = px.bar(region_counts, x='Region', y='Count', title='Number of Properties by Region')
    st.plotly_chart(fig_bar_region)
    
    # Commute Time Charts (Side by Side)
    if 'Commute Time 2019 (mins)' in filtered_df.columns:
        st.subheader("Commute Time Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            fig_commute_scatter = px.scatter(filtered_df, x='Commute Time 2019 (mins)', y=selected_columns[0], color='Region', title='Commute Time vs Asking Price')
            st.plotly_chart(fig_commute_scatter)
        
        with col2:
            fig_commute_hist = px.histogram(filtered_df, x='Commute Time 2019 (mins)', title='Histogram of Commute Times')
            st.plotly_chart(fig_commute_hist)
        
        # Commute Time vs. Average Asking Price per Location
        commute_avg_price = filtered_df.groupby('Town')[['Commute Time 2019 (mins)'] + selected_columns].mean().reset_index()
        fig_commute_avg_price = px.scatter(commute_avg_price, x='Commute Time 2019 (mins)', y=selected_columns[0], color='Town', title='Commute Time vs. Average Asking Price per Location')
        st.plotly_chart(fig_commute_avg_price)
    
    # Histogram: Asking price distribution
    fig_hist = px.histogram(melted_df, x='Asking Price', title='Histogram of Asking Prices')
    st.plotly_chart(fig_hist)

# Display Table
st.subheader("Filtered Data Table")
st.dataframe(filtered_df.set_index('Town').fillna('N/A').reset_index())
