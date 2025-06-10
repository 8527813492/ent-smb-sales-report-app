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

st.title("Interactive Order Report")

# Filters
actor_seg = st.multiselect("Select Actor Segment", df['Actor Seg'].unique())
product_name = st.multiselect("Select Product", df['Product_name'].unique())

# Filter data
filtered_df = df.copy()
if actor_seg:
    filtered_df = filtered_df[filtered_df['Actor Seg'].isin(actor_seg)]
if product_name:
    filtered_df = filtered_df[filtered_df['Product'].isin(product_name)]

# Show filtered data table
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Aggregate data for charts
agg_product = filtered_df.groupby('Product')['Distinct Order Count'].sum()
agg_actor = filtered_df.groupby('Actor Seg')['Distinct Order Count'].sum()

# Layout charts side by side
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Orders by Product")
    st.bar_chart(agg_product)

with col3:
    st.subheader("Orders by Actor Segment")
    st.bar_chart(agg_actor)

# Plotly Pie Chart for product distribution
st.subheader("Product Distribution Pie Chart")
fig_pie = px.pie(filtered_df, values='Distinct Order Count', names='Product', title='Product Distribution')
st.plotly_chart(fig_pie)

# Matplotlib chart example: Orders by Delivery (if column exists)
if 'Delivery' in filtered_df.columns:
    st.subheader("Orders by Delivery Type")
    delivery_agg = filtered_df.groupby('Delivery')['Distinct Order Count'].sum()
    fig, ax = plt.subplots()
    ax.bar(delivery_agg.index, delivery_agg.values)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Download filtered data as CSV
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="⬇️ Download Filtered CSV",
    data=csv,
    file_name='filtered_report.csv',
    mime='text/csv'
)
