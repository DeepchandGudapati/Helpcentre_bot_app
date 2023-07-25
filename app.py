import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process

# Load your dataset
data = pd.read_excel("bot.xlsx")

st.title("Bot: Get Links by Description")

# User input for description
user_input = st.text_input("Enter description:")

# Search suggestions based on the available descriptions
if user_input:
    suggestions = process.extract(user_input, data["description"], limit=5)
    suggestions = [suggestion[0] for suggestion in suggestions if suggestion[1] >= 80]
    st.write("Search Suggestions:")
    st.write(suggestions)

# Find the link corresponding to the description
if user_input:
    filtered_data = data[data["description"].str.contains(user_input, case=False)]

    if not filtered_data.empty:
        link = filtered_data["link"].iloc[0]
        st.success(f"Link: {link}")

        # Fetch webpage content and extract a preview (same as previous implementation)
        # ...

    else:
        st.warning("No link found for the provided description.")
