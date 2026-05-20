import streamlit as st
import pandas as pd

file = st.file_uploader("Upload CSV")

if file:
    df = pd.read_csv(file)

    st.write("Columns:", df.columns)

    if "Year" in df.columns:

        year = st.selectbox(
            "Select Year",
            df["Year"].unique()
        )

        filtered_df = df[df["Year"] == year]

        st.write(filtered_df)

    else:
        st.error("Year column not found!")
