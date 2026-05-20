import streamlit as st
import pandas as pd

st.title("Sales Dashboard")

file = st.file_uploader("Upload CSV File")

if file:
    df = pd.read_csv(file)

    year = st.selectbox("Select Year", df["Year"].unique())

    filtered_df = df[df["Year"] == year]

    sales = filtered_df["Sales"].sum()
    profit = filtered_df["Profit"].sum()

    st.metric("Total Sales", sales)
    st.metric("Total Profit", profit)
