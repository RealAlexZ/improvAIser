import streamlit as st
import streamlit.components.v1 as components
import os
import base64

# Configure the page layout
st.set_page_config(layout="wide")

def get_audio_data_url(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        return f"data:audio/mp3;base64,{audio_b64}"

# Create a container for the main content
main_container = st.container()

# Get all audio files and convert them to data URLs
notes_dir = os.path.join(os.path.dirname(__file__), 'html/piano/notes')
audio_data = {}
for note in ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5']:
    audio_path = os.path.join(notes_dir, f"{note}.mp3")
    audio_data[note] = get_audio_data_url(audio_path)

# Create JavaScript code for audio data
audio_js = f"const audioData = {str(audio_data)};"

with main_container:
    # Load rhythm sequencer
    rhythm_path = os.path.join(os.path.dirname(__file__), 'html/task1-2/index.html')
    try:
        with open(rhythm_path, 'r', encoding='utf-8') as f:
            rhythm_html = f.read()
    except FileNotFoundError:
        st.error(f"Unable to find the file: {rhythm_path}")
        rhythm_html = "<p>Error: Rhythm sequencer HTML file not found.</p>"
    
    # Inject the rhythm sequencer component
    components.html(rhythm_html, height=500, scrolling=True)
    
    # Load piano interface
    piano_path = os.path.join(os.path.dirname(__file__), 'html/piano/index.html')
    try:
        with open(piano_path, 'r', encoding='utf-8') as f:
            piano_html = f.read()
            # Insert audio data before the first script tag
            piano_html = piano_html.replace('<script>', f'<script>{audio_js}', 1)
    except FileNotFoundError:
        st.error(f"Unable to find the file: {piano_path}")
        piano_html = "<p>Error: Piano HTML file not found.</p>"
    
    # Inject the component into the Streamlit app
    components.html(piano_html, height=500, scrolling=True)
