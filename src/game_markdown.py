import streamlit as st
from streamlit.components.v1 import html


def centered_title(title: str, color: str = "black", size: int = 45) -> None:
    style: str = "<style>" \
                 ".centered-title {" \
                 "text-align: center;" \
                 "}" \
                 "</style>"
    st.markdown(style, unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: {color}; font-size: {size}px' "
                f"class='centered-title'"
                f">{title}</h1>",
                unsafe_allow_html=True)


def separator() -> None:
    st.markdown("----", unsafe_allow_html=True)


def empty_space() -> None:
    st.markdown("##")


def scroll_text(height: int, text: str) -> None:
    html_text: str = f"""
    <center>
    <p style="font-size:25px; font-family:verdana">
    {text}
    </p>
    </center>
"""
    html(html_text, height=height, scrolling=True)
