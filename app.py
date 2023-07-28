import pandas as pd
import streamlit as st
from fuzzywuzzy import process

# Load your dataset
data = pd.read_excel("bot.xlsx")

# GIF URL from GitHub
gif_url = "original-4591cc3d8ca4a9f6cbe8081f7c6d16e0.gif"  # Replace with the raw URL of your GIF hosted on GitHub

# CSS styling to create zoom-in effect for main app
st.markdown(
    """
    <style>
    /* Hide main app initially */
    .main-app {
        display: none;
    }

    /* Zoom-in animation for main app */
    .main-app.zoom-in {
        animation: zoomInMain 1s ease-in-out;
        animation-fill-mode: forwards;
    }

    @keyframes zoomInMain {
        0% {
            transform: scale(0.8);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to hide the splash screen and display the main app
def hide_splash_screen():
    splash_placeholder.empty()
    main_app_placeholder.markdown(
        """
        <div class="main-app zoom-in">
        """,
        unsafe_allow_html=True,
    )

    # Display the main content of your Streamlit app here

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

    main_app_placeholder.markdown("</div>", unsafe_allow_html=True)


# Display the GIF as a splash screen with a button to hide it
splash_placeholder = st.empty()

# Display the GIF
splash_placeholder.image(gif_url, use_column_width=True)

# Button to hide the splash screen and show the main app
if splash_placeholder.button("Start App"):
    hide_splash_screen()

# Placeholder for the main app content
main_app_placeholder = st.empty()
