import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the data
df = pd.read_csv(
    "Report.csv",
    encoding='cp1252',
    low_memory=False
)

st.title("📊 Interactive Order Report")

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Filters for Actor Seg and Final Segment
actor_seg = st.sidebar.multiselect("Select Actor Segment", sorted(df['Actor Seg'].dropna().unique()))
final_seg = st.sidebar.multiselect("Select Final Segment", sorted(df['Final Segment'].dropna().unique()))

# Product filter
product_name = st.sidebar.multiselect("Select Product", sorted(df['Product Name'].dropna().unique()))

# Pickup and Delivery filters
pickup_filter = st.sidebar.multiselect("Select Pickup Type", sorted(df['Pickup'].dropna().unique()))
delivery_filter = st.sidebar.multiselect("Select Delivery Type", sorted(df['Delivery'].dropna().unique()))

# Apply filters
filtered_df = df.copy()

if actor_seg:
    filtered_df = filtered_df[filtered_df['Actor Seg'].isin(actor_seg)]

if final_seg:
    filtered_df = filtered_df[filtered_df['Final Segment'].isin(final_seg)]

if product_name:
    filtered_df = filtered_df[filtered_df['Product Name'].isin(product_name)]

if pickup_filter:
    filtered_df = filtered_df[filtered_df['Pickup'].isin(pickup_filter)]

if delivery_filter:
    filtered_df = filtered_df[filtered_df['Delivery'].isin(delivery_filter)]

# Display filtered data
st.subheader("📄 Filtered Data Table")
st.dataframe(filtered_df)

# Aggregated views
agg_product = filtered_df.groupby('Product Name')['Distinct Order Count'].sum().sort_values(ascending=False)
agg_actor = filtered_df.groupby('Actor Seg')['Distinct Order Count'].sum().sort_values(ascending=False)
agg_final_seg = filtered_df.groupby('Final Segment')['Distinct Order Count'].sum().sort_values(ascending=False)

# Layout charts
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📦 Orders by Product")
    st.bar_chart(agg_product)

with col2:
    st.subheader("🧑 Orders by Actor Segment")
    st.bar_chart(agg_actor)

with col3:
    st.subheader("🏷️ Orders by Final Segment")
    st.bar_chart(agg_final_seg)

# Plotly Pie Chart
st.subheader("🎯 Product Distribution (Pie Chart)")
fig_pie = px.pie(
    filtered_df,
    values='Distinct Order Count',
    names='Product Name',
    title='Product Distribution by Order Count'
)
st.plotly_chart(fig_pie)

# Matplotlib bar chart for Delivery
if 'Delivery' in filtered_df.columns and not filtered_df['Delivery'].isnull().all():
    st.subheader("🚚 Orders by Delivery Type")
    delivery_agg = filtered_df.groupby('Delivery')['Distinct Order Count'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.bar(delivery_agg.index.astype(str), delivery_agg.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Download filtered CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name='filtered_report.csv',
    mime='text/csv'
)
