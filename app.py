import pandas as pd
import streamlit as st
import openpyxl

# Load your dataset
data = pd.read_excel("bot.xlsx")

st.title("Get HC Links by Description")

# User input for description
user_input = st.text_input("Enter description:")

# Find the link corresponding to the description
if user_input:
    link = data[data["description"].str.contains(user_input, case=False)]["link"].iloc[0]
    if link:
        st.success(f"Link: {link}")
    else:
        st.warning("No link found for the provided description.")
