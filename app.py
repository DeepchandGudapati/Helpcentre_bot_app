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
    }

    .suggestion-link {
        display: block;
        margin: 8px 0; /* Adjust margin to create spacing between suggestions */
    }

    .suggestion-link a {
        color: #1877f2; /* Meta blue */
        text-decoration: none;
        font-weight: bold;
        padding: 8px 16px; /* Add padding to make the suggestion links clickable */
        display: block;
        border-radius: 12px; /* Rounded corners for suggestion links */
    }

    .suggestion-link a:hover {
        background-color: #f0f2f5; /* Add hover effect */
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Load the splash screen GIF from your GitHub repository
splash_screen_gif_url = "https://github.com/DeepchandGudapati/bot_app/blob/384a9807205f8df61c101b279f1917d2799097e5/original-4591cc3d8ca4a9f6cbe8081f7c6d16e0.gif"
st.image(splash_screen_gif_url, use_column_width=True, format="GIF")

# Main app
st.title("Get help center Links")

# User input for description
user_input = st.sidebar.text_input("Enter description:", key="description_input")  # Add key to fix caching issue

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

# Search suggestions based on the available descriptions
if user_input:
    suggestions = process.extract(user_input, data["description"], limit=5)
    st.sidebar.markdown("<div class='suggestions-container'>", unsafe_allow_html=True)
    st.sidebar.write("Search Suggestions:")
    for suggestion in suggestions:
        link = data.loc[data["description"] == suggestion[0], "link"].iloc[0]
        st.sidebar.markdown(
            f"<div class='suggestion-link'><a href='{link}'>{suggestion[0]}</a></div>",
            unsafe_allow_html=True,
        )
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
