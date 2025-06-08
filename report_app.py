import streamlit as st
import pandas as pd

# Load the MACD data
df = pd.read_csv(
    "Report.csv",
    encoding='cp1252',
    low_memory=False
)

st.title("Interactive Order Report")

# Filters
actor_seg = st.multiselect("Select Actor Segment", df['Actor Seg'].unique())
status = st.multiselect("Select Order Status", df['Order Status'].unique())
product = st.multiselect("Select Product", df['Product'].unique())

# Filter data
filtered_df = df.copy()
if actor_seg:
    filtered_df = filtered_df[filtered_df['Actor Seg'].isin(actor_seg)]
if status:
    filtered_df = filtered_df[filtered_df['Order Status'].isin(status)]
if product:
    filtered_df = filtered_df[filtered_df['Product'].isin(product)]

# Show table
st.dataframe(filtered_df)

# Show chart
st.bar_chart(filtered_df.groupby('Product')['Distinct Order Count'].sum())
