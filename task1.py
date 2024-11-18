import streamlit as st
import streamlit.components.v1 as components
import os
import base64

def get_audio_data_url(file_path):
    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        return f"data:audio/mp3;base64,{audio_b64}"

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Unable to find the file: {file_path}")
        return ""

# Configure the page layout
st.set_page_config(layout="wide")

# Create a container for the main content
main_container = st.container()

# Get all audio files and convert them to data URLs
notes_dir = os.path.join(os.path.dirname(__file__), 'html/task3/notes')
audio_data = {}

# Add the background loop first
base_path = os.path.join(os.path.dirname(__file__), 'html/task3')
try:
    audio_data['background'] = get_audio_data_url(os.path.join(base_path, '4-bar-loop.mp3'))
except FileNotFoundError:
    st.error("Missing audio file: 4-bar-loop.mp3")

# Then add piano notes
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

base_path = os.path.join(os.path.dirname(__file__), 'html/task3')

# Add the background loop
try:
    audio_data['background'] = get_audio_data_url(os.path.join(base_path, '4-bar-loop.mp3'))
except FileNotFoundError:
    st.error("Missing audio file: 4-bar-loop.mp3")

with main_container:
    # Read all necessary files
    css_content = read_file_content(os.path.join(base_path, 'styles.css'))
    script_content = read_file_content(os.path.join(base_path, 'script.js'))
    sequencer_content = read_file_content(os.path.join(base_path, 'sequencer-3-1.js'))
    
    try:
        with open(os.path.join(base_path, 'index.html'), 'r', encoding='utf-8') as f:
            task3_html = f.read()
            
            # Create style and script tags
            style_tag = f"<style>{css_content}</style>"
            script_tags = f"""
                {audio_js}
                <script>{script_content}</script>
                <script type="text/babel">{sequencer_content}</script>
            """
            
            # Insert CSS in head
            task3_html = task3_html.replace('</head>', f'{style_tag}</head>', 1)
            # Insert scripts at the end of body
            task3_html = task3_html.replace('</body>', f'{script_tags}</body>', 1)
            
    except FileNotFoundError:
        st.error(f"Unable to find the file: {os.path.join(base_path, 'index.html')}")
        task3_html = "<p>Error: task3 HTML file not found.</p>"
    
    # Inject the component into the Streamlit app
    components.html(task3_html, height=700, scrolling=True)
