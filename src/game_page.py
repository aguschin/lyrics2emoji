import streamlit as st

import game_markdown as mark_down
from game_state import GameStage
from game_state import Guess
from game_state import GameState
from game_state import OPTION_COUNT
from game_state import Song

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
TIME_DELAY: int = 2
BARS_SIZE: int = 30
NEXT_LEVEL_LABEL: str = "next level"
ANSWER_SIZE: int = 20


class Game:

    def __init__(self) -> None:
        if GAME_STATE not in st.session_state:
            st.session_state[GAME_STATE] = GameState()

        if BEST not in st.session_state:
            st.session_state[BEST] = 0

        self.state: GameState = st.session_state.game_state

    def play(self) -> None:
        mark_down.centered_title(GAME_TITLE)

        stage: GameStage = self.state.game_stage
        if stage is GameStage.GUESS:
            self._update_best()
            self._place_user_stats()
            self._place_bars(emoji=True)
            self._place_options()
            self._place_guesses()

        elif stage is GameStage.RESULT:
            self._place_user_stats()
            self._place_bars(emoji=False)
            self._place_next_level()
            self._place_guesses()

        elif stage is GameStage.GAME_OVER:
            self._place_final_score()
            self._place_try_again()
            self._place_guesses()
        else:
            raise Exception(f"unsupported game stage {stage}")

    def _place_next_level(self) -> None:
        mark_down.separator()
        _, col, __ = st.columns([2, 1, 2])
        label: str = RETRY_LABEL if self.state.get_lives() == 0 else NEXT_LEVEL_LABEL
        col.button(label=label, on_click=self.state.update_stage)
        mark_down.empty_space()

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

    def _place_bars(self, *, emoji: bool) -> None:
        bars: list[str] = self.state.level.correct.lyrics.bars
        emoji_bars: list[str] = self.state.level.correct.lyrics.translated_bars
        if emoji:
            for emoji_bar in emoji_bars:
                mark_down.centered_title(emoji_bar, size=BARS_SIZE)
            mark_down.empty_space()
            mark_down.empty_space()

        else:
            guess: Guess = self.state.get_latest_guess()
            color: str = COLOR_CORRECT if guess.is_correct else COLOR_INCORRECT

            for bar, emoji_bar in zip(bars, emoji_bars):
                bar_col, emoji_col = st.columns([1, 1])
                with bar_col:
                    mark_down.centered_title(bar, color=color, size=ANSWER_SIZE)
                with emoji_col:
                    mark_down.centered_title(emoji_bar, size=ANSWER_SIZE)

            mark_down.empty_space()
            mark_down.centered_title(self.state.level.correct.__repr__(), color=color,
                                     size=ANSWER_SIZE)
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
