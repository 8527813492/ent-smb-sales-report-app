import streamlit as st
import pandas as pd

# Load the data
final_aggregated = pd.read_csv(r"C:\Users\goutam.yadav\OneDrive - Reliance Corporate IT Park Limited\Desktop\Anaconda\Report.csv")

st.title("Interactive Tabular Report")

# Show interactive dataframe with filtering and sorting
st.dataframe(final_aggregated)
