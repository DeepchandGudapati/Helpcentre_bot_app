import pandas as pd
import streamlit as st
from fuzzywuzzy import process

# Load your dataset
data = pd.read_excel("bot.xlsx")

# Main app
st.title("Get help center Links")

# User input for description
user_input = st.text_input("Enter description:")

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

# Create an empty space to move suggestions below the link field
suggestions_placeholder = st.empty()

# Search suggestions based on the available descriptions
if user_input:
    suggestions = process.extract(user_input, data["description"], limit=5)
    suggestions = [suggestion[0] for suggestion in suggestions if suggestion[1] >= 80]
    suggestions_placeholder.write("Search Suggestions:")
    # Display suggestions as hyperlinks
    for suggestion in suggestions:
        link = data.loc[data["description"] == suggestion, "link"].iloc[0]
        suggestions_placeholder.markdown(f"[{suggestion}]({link})", unsafe_allow_html=True)
