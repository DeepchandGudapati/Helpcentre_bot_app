import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Load your dataset
data = pd.read_excel("bot.xlsx")

st.title("Bot: Get Links by Description")

# User input for description
user_input = st.text_input("Enter description:")

# Find the link corresponding to the description
if user_input:
    filtered_data = data[data["description"].str.contains(user_input, case=False)]

    if not filtered_data.empty:
        link = filtered_data["link"].iloc[0]
        st.success(f"Link: {link}")

        # Fetch webpage content and extract a preview
        try:
            response = requests.get(link)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                preview_text = soup.get_text()
                st.write("Preview:")
                st.text(preview_text)
            else:
                st.warning("Failed to fetch webpage content.")
        except requests.exceptions.RequestException as e:
            st.warning(f"Error: {e}")
    else:
        st.warning("No link found for the provided description.")
