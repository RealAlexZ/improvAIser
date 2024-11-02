import streamlit as st
import streamlit.components.v1 as components
import os

# Configure the page layout
st.set_page_config(layout="wide")

# Create a container for the main content
main_container = st.container()

with main_container:
    # Load task1/index.html
    task1_html_path = os.path.join(os.path.dirname(__file__), 'html/task1/index.html')
    try:
        with open(task1_html_path, 'r', encoding='utf-8') as f:
            task1_html = f.read()
    except FileNotFoundError:
        st.error(f"Unable to find the file: {task1_html_path}")
        task1_html = "<p>Error: Task1 HTML file not found.</p>"
    
    # Inject the task1/index.html component into the Streamlit app
    components.html(task1_html, height=700, scrolling=True)
