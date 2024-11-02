import streamlit as st
import streamlit.components.v1 as components
import os

# Configure the page layout
st.set_page_config(layout="wide")

# Create an empty sidebar
st.sidebar.empty()

# Create a container for the main content
main_container = st.container()

# Calculate the height for the components
rhythm_height = 250
piano_height = 250

with main_container:
    # Load rhythm sequencer
    rhythm_path = os.path.join(os.path.dirname(__file__), 'html/task1-2/index.html')
    try:
        with open(rhythm_path, 'r', encoding='utf-8') as f:
            rhythm_html = f.read()
    except FileNotFoundError:
        st.error(f"Unable to find the file: {rhythm_path}")
        rhythm_html = "<p>Error: Rhythm sequencer HTML file not found.</p>"
    
    # Load piano interface
    piano_path = os.path.join(os.path.dirname(__file__), 'html/piano/index.html')
    try:
        with open(piano_path, 'r', encoding='utf-8') as f:
            piano_html = f.read()
    except FileNotFoundError:
        st.error(f"Unable to find the file: {piano_path}")
        piano_html = "<p>Error: Piano HTML file not found.</p>"
    
    # Inject both components into the Streamlit app
    components.html(rhythm_html, height=rhythm_height, scrolling=True)
    components.html(piano_html, height=piano_height, scrolling=True)
