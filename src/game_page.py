import streamlit as st

import game_markdown as mark_down
from game_state import GameState

RED_HEART_EMOJI: str = "\u2764\uFE0F"
RETRY_LABEL: str = "Try Again!"
GAME_TITLE: str = "Lyrics-2-Emoji"
GAME_STATE: str = "game_state"
SCROLL_HEIGHT: int = 400


class Game:

    def __init__(self) -> None:
        if GAME_STATE not in st.session_state:
            st.session_state[GAME_STATE] = GameState()

        self.state: GameState = st.session_state.game_state

    def guess(self, option: str) -> None:
        self.state.next_level(option)

    def play(self) -> None:
        mark_down.centered_title(GAME_TITLE)

        if self.state.game_over:
            self.place_wrong_songs()
            self.place_try_again()
        else:
            self.place_lives_and_score()
            self.place_emoji()
            self.place_options()
            self.place_correct_songs()

    def place_wrong_songs(self) -> None:
        assert len(self.state.incorrect_songs) == 3
        wrong_song1, wrong_song2, wrong_song3 = self.state.incorrect_songs
        wrong_col1, wrong_col2, wrong_col3 = st.columns([1, 1, 1])

        def place_wrong_song(wrong_song, wrong_col) -> None:
            with wrong_col:
                correct_song, wrong_guess, song_emoji = wrong_song
                mark_down.centered_title(song_emoji)
                mark_down.centered_title(correct_song, color="green", size=25)
                mark_down.centered_title(wrong_guess, color="red", size=25)

        place_wrong_song(wrong_song1, wrong_col1)
        place_wrong_song(wrong_song2, wrong_col2)
        place_wrong_song(wrong_song3, wrong_col3)

    def place_correct_songs(self) -> None:
        correct_songs: str = ""
        for song, song_emoji in self.state.correct_songs[::-1]:
            correct_songs += f"{song} : {song_emoji} <br />"

        mark_down.scroll_text(SCROLL_HEIGHT, correct_songs)

    def place_lives_and_score(self) -> None:
        lives_col, score_col = st.columns([1, 1])
        with lives_col:
            mark_down.centered_title(RED_HEART_EMOJI * self.state.get_lives())

        with score_col:
            mark_down.centered_title(str(self.state.get_score()))
        mark_down.separator()

    def place_emoji(self) -> None:
        mark_down.centered_title(self.state.correct_option_emoji)
        mark_down.empty_space()
        mark_down.empty_space()

    def place_options(self) -> None:
        option1_col, option2_col, option3_col = st.columns([1, 1, 1])
        option1, option2, option3 = self.state.options

        def place_option(option, col) -> None:
            with col:
                st.button(label=option, on_click=lambda: self.guess(option))

        place_option(option1, option1_col)
        place_option(option2, option2_col)
        place_option(option3, option3_col)
        mark_down.empty_space()
        mark_down.empty_space()

    def place_try_again(self) -> None:
        mark_down.separator()
        _, col, __ = st.columns([2, 1, 2])
        col.button(label=RETRY_LABEL, on_click=self.state.reset)


Game().play()
