import streamlit as st

from game_state import GameState


def init_game_state() -> GameState:
    if "game_state" not in st.session_state:
        st.session_state["game_state"] = GameState()

    return st.session_state.game_state


def guess(option: str) -> None:
    if option == game_state.correct_option:
        game_state.next_level(option)
    else:
        game_state.end_game()


def centered_title(title):
    st.markdown("""
        <style>
        .centered-title {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f"<h1 class='centered-title'>{title}</h1>", unsafe_allow_html=True)


def place_game() -> None:
    centered_title(game_state.get_correct_option_emoji())

    option1_col, option2_col, option3_col = st.columns(3)
    option1, option2, option3 = game_state.options

    with option1_col:
        st.button(label=option1, on_click=lambda: guess(option1))

    with option2_col:
        st.button(label=option2, on_click=lambda: guess(option2))

    with option3_col:
        st.button(label=option3, on_click=lambda: guess(option3))


def place_game_over() -> None:
    centered_title(f"score : {game_state.score}")
    st.button(label="retry", on_click=game_state.reset)


def play_game() -> None:
    centered_title("Lyrics-2-Emoji")

    if game_state.game_over:
        place_game_over()
    else:
        place_game()


game_state: GameState = init_game_state()
play_game()
