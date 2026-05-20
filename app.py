import streamlit as st

st.title("E-Commerce Sales App")

year = st.selectbox("Select Year", [2016, 2017, 2018])

sales = 15000

st.write("Total Sales:", sales)
