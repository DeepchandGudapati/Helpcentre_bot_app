import pandas as pd
import streamlit as st
from fuzzywuzzy import process
from IPython.display import display, Image

# Load your dataset
data = pd.read_excel("bot.xlsx")

# GIF URL from GitHub
gif_url = "original-4591cc3d8ca4a9f6cbe8081f7c6d16e0.gif"  # Replace with the raw URL of your GIF hosted on GitHub

# CSS styling to create splash screen and zoom-in effect
st.markdown(
    """
    <style>
    /* Hide main app initially */
    .main-app {
        display: none;
    }

    /* Splash screen styling */
    .splash-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 9999;
        background-color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        opacity: 1;
        transition: opacity 1s ease-in-out;
    }

    /* Zoom-in animation for splash screen */
    .splash-screen.zoom-in {
        animation: zoomIn 1s ease-in-out;
        animation-fill-mode: forwards;
    }

    @keyframes zoomIn {
        0% {
            transform: scale(2);
            opacity: 1;
        }
        100% {
            transform: scale(1);
            opacity: 0;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Function to show the main app and hide the splash screen on click
def hide_splash_screen():
    st.markdown(
        """
        <script>
        document.addEventListener("DOMContentLoaded", function() {
            document.querySelector(".main-app").style.display = "block";
            document.querySelector(".splash-screen").classList.add("zoom-in");
        });
        </script>
        """,
        unsafe_allow_html=True,
    )

# Splash screen
st.markdown(
    f"""
    <div class="splash-screen" onclick="hide_splash_screen()">
        <img src="{gif_url}" alt="Splash Screen GIF" style="max-width: 100%; max-height: 100%;">
    </div>
    """,
    unsafe_allow_html=True,
)

# Main app
with st.container():
    st.markdown(
        """
        <style>
        /* Styling for main app */
        .main-app {
            display: block;
            transition: opacity 1s ease-in-out;
        }

        /* Set the opacity of main app to 0 initially */
        .main-app.hidden {
            opacity: 0;
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
        <div class="main-app hidden">
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

    st.markdown("</div>", unsafe_allow_html=True)
