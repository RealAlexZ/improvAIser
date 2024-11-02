import streamlit as st
import streamlit.components.v1 as components
import os

# Configure the page layout
st.set_page_config(layout="centered")

# Create an empty sidebar
st.sidebar.empty()

# Create a container for the main content
main_container = st.container()

# Calculate the height for the bottom third
bottom_third_height = 250

with main_container:
    # Determine the path to the index.html file
    html_file_path = os.path.join(os.path.dirname(__file__), 'html/task1-2/index.html')
    
    # Read the HTML content from index.html
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_code = f.read()
    except FileNotFoundError:
        st.error(f"Unable to find the file: {html_file_path}")
        html_code = "<p>Error: HTML file not found.</p>"
    
    # Inject the HTML into the Streamlit app
    components.html(html_code, height=bottom_third_height, scrolling=True)
