# import streamlit as st
# import streamlit.components.v1 as components
# from streamlit_extras.stylable_container import stylable_container
# import os
# import base64
# import re
#
# # -------------------------------------------------- Added --------------------------------------------------
# from utils import *
# # -----------------------------------------------------------------------------------------------------------
#
# def get_audio_data_url(file_path):
#     with open(file_path, "rb") as audio_file:
#         audio_bytes = audio_file.read()
#         audio_b64 = base64.b64encode(audio_bytes).decode()
#         return f"data:audio/mp3;base64,{audio_b64}"
#
# # Configure the page layout
# st.set_page_config(layout="wide")
#
# # -------------------------------------------------- Added --------------------------------------------------
# instructions = get_instructions(1)
# if "show_instruction_dialog" not in st.session_state:
#     show_instruction_dialog(instructions)
#     st.session_state["show_instruction_dialog"] = True
# if "generate_message" not in st.session_state:
#     st.session_state["generate_message"] = False
# if "enable_next" not in st.session_state:
#     st.session_state["enable_next"] = False
#
# st.title("1. Imitate Rhythm Blocks")
#
# tabs = st.tabs(["Single Imitation", "Combined Imitation"])
#
# with st.expander("Instructions", expanded=False):
#     st.markdown(instructions, unsafe_allow_html=True)
#
# c = st.columns(2)
#
# feedback = "Congratulations! 🎉"
# if st.session_state["generate_message"]:
#     with st.chat_message("user"):
#         # feedback = assess_performance(1)
#         stream_msg(feedback)
#
#     st.session_state["generate_message"] = False
#     pattern = r"Congratulations! 🎉"
#     if re.search(pattern, feedback):
#         st.session_state["enable_next"] = True
#
# with c[0]:
#     if color_button("⚛︎ Generate Response", "green", "container_gpt", "button_gpt"):
#         st.session_state["generate_message"] = True
#         st.rerun()
#
# with c[1]:
#     if not st.session_state["enable_next"]:
#         color_button("Complete this to go next →", "#3A3B3C", "container_incomplete_next", "button_incomplete_next", disabled=True)
#
#     elif st.session_state["enable_next"]:
#         if color_button("Next subtask →", "green", "container_next", "button_next"):
#             st.session_state["enable_next"] = False
#             st.rerun()
# # -----------------------------------------------------------------------------------------------------------
#
# # Create a container for the main content
# main_container = st.container()
#
# # Get all audio files and convert them to data URLs
# notes_dir = "./html/task1/notes"
# audio_data = {}
# for note in ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5']:
#     audio_path = os.path.join(notes_dir, f"{note}.mp3")
#     try:
#         audio_data[note] = get_audio_data_url(audio_path)
#     except FileNotFoundError:
#         st.error(f"Missing audio file: {note}.mp3")
#
# # Create JavaScript code for audio data
# audio_js = f"""
# <script>
#     const audioData = {str(audio_data)};
# </script>
# """
#
# with (main_container):
#     task1_html_path = "./html/task1/index.html"
#     try:
#         with open(task1_html_path, 'r', encoding='utf-8') as f:
#             task1_html = f.read()
#             # Insert audio data right after the opening <head> tag
#             task1_html = task1_html.replace('<head>', f'<head>{audio_js}', 1)
#     except FileNotFoundError:
#         st.error(f"Unable to find the file: {task1_html_path}")
#         task1_html = "<p>Error: Task1 HTML file not found.</p>"
#
#     # Inject the component into the Streamlit app
#     components.html(task1_html, height=700, scrolling=True)

from page_helper import *

get_page(2)