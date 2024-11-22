import time
import streamlit as st
from openai import OpenAI
import csv
from streamlit_extras.stylable_container import stylable_container
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
import os
import base64
import re
from utils import *
from streamlit_float import *
from streamlit_extras.bottom_container import bottom


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


def sidebar_top(content):
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"]::before {{
                content: "{content}";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                font-weight: bold;
                position: relative;
                # top: 100px;
                # display: block;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


def vertical_alignment():
    # Vertical alignment of columns
    st.write(
        """<style>
        [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background_img(image_path):
    # Get the base64 encoded string of the image
    base64_image = get_base64_of_bin_file(image_path)
    # Custom CSS to set the background image
    st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{base64_image}");
                background-size: cover;
                background-position: center;
            }}
            </style>
            """, unsafe_allow_html=True)


def set_sidebar_img(image_path):
    # Get the base64 encoded string of the image
    base64_image = get_base64_of_bin_file(image_path)
    # Custom CSS to set the background image
    st.markdown(f"""
            <style>
            [data-testid=stSidebar] {{
                background-image: url("data:image/jpg;base64,{base64_image}");
            }}
            </style>
            """, unsafe_allow_html=True)


def stream_msg(feedback):
    def helper_stream_msg():
        for word in feedback.split(" "):
            yield word + " "
            time.sleep(0.03)

    st.write_stream(helper_stream_msg)


def color_button(label, color, container_key, button_key, radius=20, disabled=False):
    with stylable_container(
        key=container_key,
        css_styles=f"""
        button {{
            background-color: {color};
            color: white;
            border-radius: {radius}px;
        }}
    """,
    ):
        return st.button(label, use_container_width=True, key=button_key, disabled=disabled)


def show_instruction_dialog(instructions, stream):
    @st.dialog("Instructions", width="large")
    def helper_show_instruction_dialog():
        if stream:
            for instruction in instructions.split("\n"):
                stream_msg(instruction)
        else:
            st.markdown(instructions, unsafe_allow_html=True)
    helper_show_instruction_dialog()


@st.dialog("🥊 Score Board 🥋", width="large")
def show_scoreboard():
    c = st.columns(3)
    with c[0]:
        st.button("Rank", use_container_width=True)
    with c[1]:
        st.button("Name", use_container_width=True)
    with c[2]:
        st.button("Score", use_container_width=True)

    time.sleep(0.5)
    c = st.columns(3)
    with c[0]:
        color_button("1", "#DAA520", "one", "one", radius=7)
    with c[1]:
        color_button("Alex", "#DAA520", "Alex", "Alex", radius=7)
    with c[2]:
        color_button("99", "#DAA520", "score_a", "score_a", radius=7)

    time.sleep(0.5)
    c = st.columns(3)
    with c[0]:
        color_button("2", "#838996", "two", "two", radius=7)
    with c[1]:
        color_button("Jason", "#838996", "Jason", "Jason", radius=7)
    with c[2]:
        color_button("89", "#838996", "score_b", "score_b", radius=7)

    time.sleep(0.5)
    c = st.columns(3)
    with c[0]:
        color_button("3", "#A97142", "three", "three", radius=7)
    with c[1]:
        color_button("Suliang", "#A97142", "Suliang", "Suliang", radius=7)
    with c[2]:
        color_button("88", "#A97142", "score_c", "score_c", radius=7)

    time.sleep(0.5)
    c = st.columns(3)
    with c[0]:
        color_button("4", "#3A3B3C", "four", "four", radius=7)
    with c[1]:
        color_button("User 1", "#3A3B3C", "user", "user", radius=7)
    with c[2]:
        color_button("75", "#3A3B3C", "score_d", "score_d", radius=7)



def assess_performance(task):
    client = OpenAI()

    system_prompt = """
    You are an encouraging music tutor who teaches novices how to improvise.
    The student is provided with a tutoring system where they are given a virtual keyboard and they can practice skills required for improvisation.
    """
    user_prompt = ""

    if task == 1:
        system_prompt += """
        Now they are doing the "rhythm imitation" task in this tutoring system.
        In this task, the student is asked to follow the rhythm given by the system with a fixed pitch (i.e. they only need to press a single key on the keyboard in this task).
        The system will encode the expected input and the student's input in the following format: X X X X | X X X X | X X X X | X X X X, where "X" can be either "0" or "1".
        "1" means the keyword is struck at that beat while "0" means the opposite.
        Each bar is separated by "|".
        """

        target_pattern_str = ""
        input_pattern_str = ""

        with open("log.csv", "r") as f:
            rows = csv.reader(f)
            next(rows)

            idx = 0
            for row in rows:
                if idx % 4 == 0 and idx != 0:
                    target_pattern_str += "| "
                    input_pattern_str += "| "

                target_pattern_str += row[1] + " "
                input_pattern_str += ("1" if row[0] != "0" else "0") + " "

                idx += 1

        print(target_pattern_str)
        print()
        print(input_pattern_str)

        user_prompt = f"""
        The expected input is {target_pattern_str}.
        The student's input is {input_pattern_str}.
        """

    elif task == 2:
        pass

    elif task == 3:
        pass

    system_prompt += """
    You will be given both the expected input and the student's input and please give them your feedback in less than three sentences.
    If they complete the task correctly, you should praise them with "**Congratulations! 🎉**"
    If they make mistakes, try to encourage them and tell them how they can improve.
    Examples of mistakes include 1) the student struck the keyword when they shouldn't, 2) the student didn't strike the keyword when they should do so.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": system_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            },
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={
            "type": "text"
        }
    )

    return response.choices[0].message.content


if __name__ == '__main__':
    assess_performance(1)
