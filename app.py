import pandas as pd
import streamlit as st
from fuzzywuzzy import process

# Load your dataset
data = pd.read_excel("bot.xlsx")

# CSS styling for Meta theme
st.markdown(
    """
    <style>
    /* Container width and alignment */
    .stApp {
        max-width: 960px; /* Adjust to your preference */
        margin: 0 auto;
    }

    /* Main container background and border radius */
    .stApp div[data-testid="stDecoration"] {
        background-color: #f5f6f8;
        border-radius: 12px; /* Adjust to your preference */
        padding: 24px; /* Adjust to your preference */
    }

    /* Header background color */
    .stApp div[data-testid="stSessionInfo"] {
        background-color: #1877f2; /* Meta blue */
    }

    /* Header text color */
    .stApp div[data-testid="stSessionInfo"] span {
        color: #ffffff; /* White text */
    }

    /* Widget styles */
    .stButton {
        background-color: #1877f2; /* Meta blue */
        color: #ffffff; /* White text */
        border-radius: 12px; /* Rounded corners */
        padding: 12px 24px; /* Adjust to your preference */
    }

    .stTextInput {
        border: none; /* Remove border */
        border-radius: 12px; /* Rounded corners */
        background-color: #ffffff; /* White background */
        padding-left: 10px; /* Adjust left padding to align text in the input box */
    }

    /* Suggestions styling */
    .suggestions-container {
        background-color: #ffffff;
        border: 1px solid #dddddd;
        border-radius: 12px;
        padding: 12px;
    }

    .suggestion-link {
        display: block;
        margin-bottom: 8px;
    }

    .suggestion-link a {
        color: #1877f2; /* Meta blue */
        text-decoration: none;
        font-weight: bold;
    }

    .suggestion-link a:hover {
        text-decoration: underline;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Main app
st.title("Get help center Links")

# User input for description
user_input = st.text_input("Enter description:", key="description_input")  # Add key to fix caching issue

# Search suggestions based on the available descriptions
if user_input:
    suggestions = process.extract(user_input, data["description"], limit=5)
    suggestions = [suggestion[0] for suggestion in suggestions if suggestion[1] >= 80]
    st.markdown("<div class='suggestions-container'>", unsafe_allow_html=True)
    st.write("Search Suggestions:")
    for suggestion in suggestions:
        link = data.loc[data["description"] == suggestion, "link"].iloc[0]
        st.markdown(f"<div class='suggestion-link'><a href='{link}'>{suggestion}</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

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
