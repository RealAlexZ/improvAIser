import streamlit as st
import streamlit.components.v1 as components
import os
import base64

def get_audio_data_url(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        return f"data:audio/mp3;base64,{audio_b64}"

# Configure the page layout
st.set_page_config(layout="wide")

# Create a container for the main content
main_container = st.container()

# Get all audio files and convert them to data URLs
notes_dir = os.path.join(os.path.dirname(__file__), 'html/task1/notes')
audio_data = {}
for note in ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5']:
    audio_path = os.path.join(notes_dir, f"{note}.mp3")
    try:
        audio_data[note] = get_audio_data_url(audio_path)
    except FileNotFoundError:
        st.error(f"Missing audio file: {note}.mp3")

# Create JavaScript code for audio data
audio_js = f"""
<script>
    const audioData = {str(audio_data)};
</script>
"""

with main_container:
    task1_html_path = os.path.join(os.path.dirname(__file__), 'html/task1/index.html')
    try:
        with open(task1_html_path, 'r', encoding='utf-8') as f:
            task1_html = f.read()
            # Insert audio data right after the opening <head> tag
            task1_html = task1_html.replace('<head>', f'<head>{audio_js}', 1)
    except FileNotFoundError:
        st.error(f"Unable to find the file: {task1_html_path}")
        task1_html = "<p>Error: Task1 HTML file not found.</p>"
    
    # Inject the component into the Streamlit app
    components.html(task1_html, height=700, scrolling=True)
