import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process
import json

# Custom CSS
st.markdown(
    """
    <style>
    /* Body background color */
    body {
        background-color: #f0f2f5;
    }

    /* Container width and alignment */
    .stApp {
        max-width: 960px; /* Adjust to your preference */
        margin: 0 auto;
    }

    /* Main container background and border radius */
    .stApp div[data-testid="stDecoration"] {
        background-color: #ffffff;
        border-radius: 8px; /* Adjust to your preference */
        padding: 16px; /* Adjust to your preference */
    }

    /* Header background color */
    .stApp div[data-testid="stSessionInfo"] {
        background-color: #1877f2; /* Facebook blue */
    }

    /* Header text color */
    .stApp div[data-testid="stSessionInfo"] span {
        color: #ffffff; /* White text */
    }

    /* Widget styles */
    .stButton {
        background-color: #1877f2; /* Facebook blue */
        color: #ffffff; /* White text */
        border-radius: 8px; /* Rounded corners */
        padding: 8px 16px; /* Adjust to your preference */
    }

    .stTextInput {
        border-radius: 8px; /* Rounded corners */
    }

    /* Custom fonts (adjust font URLs if using custom fonts) */
    .stApp {
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Load your dataset
data = pd.read_excel("bot.xlsx")

st.title("Get help center Links")

# User input for description
user_input = st.text_input("Enter description:")

# Search suggestions based on the available descriptions
if user_input:
    suggestions = process.extract(user_input, data["description"], limit=5)
    suggestions = [suggestion[0] for suggestion in suggestions if suggestion[1] >= 80]
    st.write("Search Suggestions:")
    st.markdown("<br>".join(f"[{suggestion}](#{suggestion.lower().replace(' ', '-')})" for suggestion in suggestions),
                unsafe_allow_html=True)

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

# JavaScript to add click event handling for suggestions
if suggestions:
    suggestions_json = json.dumps(suggestions)
    st.markdown(
        f"""
        <script>
        var suggestions = {suggestions_json};
        document.addEventListener("click", function(event) {{
            var target = event.target;
            if (target.tagName === 'A' && suggestions.includes(target.innerText)) {{
                document.querySelector('.stTextInput input').value = target.innerText;
            }}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )
