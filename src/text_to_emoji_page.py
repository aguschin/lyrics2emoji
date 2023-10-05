import streamlit as st
from text_to_emoji import translate_text


def centered_title(title: str) -> None:
    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"<h1 class='centered-title'>{title}</h1>", unsafe_allow_html=True)


centered_title("Text 2 Emoji")


def get_emoji_label(text: str | None) -> str:
    if not text: return "empty"
    return translate_text(text)


text_input: str | None = st.text_input(label="")
centered_title(get_emoji_label(text_input))
