from datetime import datetime

import streamlit as st

import game_markdown as mark_down
from game_database import GameDB
from game_database import Score
from game_state import GameStage
from game_state import GameState
from game_state import Guess
from game_state import OPTION_COUNT
from game_state import Song

RED_HEART_EMOJI: str = "\u2764\uFE0F"
RETRY_LABEL: str = "Try Again!"
GAME_TITLE: str = "Lyrics-2-Emoji"
GAME_STATE: str = "game_state"
NEXT_LEVEL_LABEL: str = "next level"
COLOR_CORRECT: str = "green"
COLOR_INCORRECT: str = "red"
DATABASE: str = "database"
USERNAME: str = "username"
SCORE: str = "score"
DATETIME: str = "datetime"
CONTINUE: str = "continue"
SCORE_SUBMITTED: str = "score_submitted"
SCROLL_HEIGHT: int = 400
WRONG_GUESS_SIZE: int = 25
SCORE_SIZE: int = 23
TIME_DELAY: int = 2
BARS_SIZE: int = 30
ANSWER_SIZE: int = 20


class Game:

    def __init__(self) -> None:
        if DATABASE not in st.session_state:
            st.session_state[DATABASE] = GameDB()

        else:
            assert st.session_state.database.is_connected()

        if SCORE_SUBMITTED not in st.session_state:
            st.session_state[SCORE_SUBMITTED] = False

        if USERNAME not in st.session_state:
            st.session_state[USERNAME] = USERNAME

        if GAME_STATE not in st.session_state:
            st.session_state[GAME_STATE] = GameState()

        self.title: str = GAME_TITLE
        self.state: GameState = st.session_state.game_state
        self.game_db: GameDB = st.session_state.database

    def play(self) -> None:

        stage: GameStage = self.state.game_stage
        if stage is GameStage.MENU:
            self._place_title()
            self._place_leaderboards()
            self._place_play_game()

        elif stage is GameStage.GUESS:
            self._place_user_stats()
            self._place_bars(emoji=True)
            self._place_options()
            self._place_guesses()

        elif stage is GameStage.RESULT:
            self._place_user_stats()
            self._place_bars(emoji=False)
            self._place_continue()
            self._place_guesses()

        elif stage is GameStage.GAME_OVER:
            self._place_final_score()
            self._place_submit_score()
            col1, col2 = st.columns([1, 1])
            with col1:
                self._place_leaderboards()
            with col2:
                self._place_guesses()

            self._place_retry()
        else:
            raise Exception(f"unsupported game stage {stage}")

    def _place_title(self) -> None:
        mark_down.centered_title(self.title)

    def _place_submit_score(self) -> None:
        if st.session_state.score_submitted:
            return

        col1, col2 = st.columns([1, 1])

        with col1:
            st.text_input(label=USERNAME, key=USERNAME)

        with col2:
            st.button(label="submit score", on_click=self._submit_score)

    def _submit_score(self) -> None:
        # FIXME: can cause duplicated scores
        score: Score = Score(
            **{USERNAME: st.session_state.username, SCORE: self.state.get_score(),
               DATETIME: datetime.now().isoformat()})
        st.session_state.score_submitted = True
        self.game_db.score().insert_one(score)

    def _place_leaderboards(self) -> None:
        scores: list[Score] = list(self.game_db.score().find())
        scores.sort(key=lambda score: score[SCORE], reverse=True)

        for user_score in scores:
            val: int = user_score[SCORE]
            name: str = user_score[USERNAME]
            st.write(f"{val} : {name}")

    def _place_play_game(self) -> None:
        mark_down.separator()
        _, col, __ = st.columns([2, 1, 2])
        col.button(label="play!",
                   on_click=lambda: self.state.set_stage(GameStage.GUESS))
        mark_down.empty_space()

    def _continue(self) -> None:
        if self.state.is_dead():
            self.state.set_stage(GameStage.GAME_OVER)
        else:
            self.state.set_stage(GameStage.GUESS)

        self.state.next_level()

    def _place_continue(self) -> None:
        mark_down.separator()
        _, col, __ = st.columns([2, 1, 2])
        col.button(label=CONTINUE, on_click=self._continue())
        mark_down.empty_space()

    def _place_final_score(self) -> None:
        score: str = f"you got {self.state.get_score()} songs correct!"
        mark_down.centered_title(score, size=SCORE_SIZE)

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

    def _retry(self) -> None:
        self.state.set_stage(GameStage.GUESS)
        self.state.reset()
        st.session_state.score_submitted = False

    def _place_retry(self) -> None:
        mark_down.separator()
        _, col, __ = st.columns([2, 1, 2])
        col.button(label=RETRY_LABEL, on_click=self._retry)
        mark_down.empty_space()


Game().play()
