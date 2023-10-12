import streamlit as st

import game_markdown as mark_down
from game_state import GameState
from game_state import Song
from game_state import OPTION_COUNT

RED_HEART_EMOJI: str = "\u2764\uFE0F"
RETRY_LABEL: str = "Try Again!"
GAME_TITLE: str = "Lyrics-2-Emoji"
GAME_STATE: str = "game_state"
BEST: str = "best"
SCROLL_HEIGHT: int = 400
WRONG_GUESS_SIZE: int = 25
SCORE_SIZE: int = 23
BEST_SIZE: int = 20
COLOR_CORRECT: str = "green"
COLOR_INCORRECT: str = "red"


class Game:

    def __init__(self) -> None:
        if GAME_STATE not in st.session_state:
            st.session_state[GAME_STATE] = GameState()

        if BEST not in st.session_state:
            st.session_state[BEST] = 0

        self.state: GameState = st.session_state.game_state

    def play(self) -> None:
        mark_down.centered_title(GAME_TITLE)

        if self.state.game_over:
            self._place_final_score()
            self._place_try_again()
            self._place_guesses()
        else:
            self._update_best()
            self._place_user_stats()
            self._place_emoji()
            self._place_options()
            self._place_guesses()

    def _update_best(self) -> None:
        current_best: int = st.session_state[BEST]
        current_score: int = self.state.get_score()
        if current_score > current_best:
            st.session_state[BEST] = current_score

    def _place_final_score(self) -> None:
        best: str = f"best score: {st.session_state[BEST]}"
        score: str = f"you got {self.state.get_score()} songs correct!"
        mark_down.centered_title(score, size=SCORE_SIZE)
        mark_down.centered_title(best, size=BEST_SIZE)

    def _place_guesses(self) -> None:
        guesses: str = ""
        space: str = "<br />" * 3
        for guess in self.state.guesses[::-1]:
            color: str = COLOR_CORRECT if guess.is_correct else COLOR_INCORRECT
            text: str = f"{guess.song.name} : {guess.song.artist}{space}"
            guesses += mark_down.get_colored_text(text, color)
        mark_down.scroll_text(SCROLL_HEIGHT, guesses)

    def _place_user_stats(self) -> None:
        lives_col, score_col = st.columns([1, 1])
        with lives_col:
            mark_down.centered_title(RED_HEART_EMOJI * self.state.get_lives())

        with score_col:
            mark_down.centered_title(str(self.state.get_score()))
        mark_down.separator()

    def _place_emoji(self) -> None:
        for emoji in self.state.level.get_emoji_bars():
            mark_down.centered_title(emoji)
        mark_down.empty_space()
        mark_down.empty_space()

    def _place_options(self) -> None:
        option1_col, option2_col, option3_col = st.columns([1, 1, 1])
        assert len(self.state.level.options) == OPTION_COUNT
        option1, option2, option3 = self.state.level.options

        def place_option(song: Song, col) -> None:
            with col:
                st.button(label=song.__repr__(),
                          on_click=lambda: self.state.guess(song))

        place_option(option1, option1_col)
        place_option(option2, option2_col)
        place_option(option3, option3_col)
        mark_down.empty_space()
        mark_down.empty_space()

    def _place_try_again(self) -> None:
        mark_down.separator()
        _, col, __ = st.columns([2, 1, 2])
        col.button(label=RETRY_LABEL, on_click=self.state.reset)
        mark_down.empty_space()


Game().play()
