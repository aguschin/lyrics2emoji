from dataclasses import dataclass
from random import choice

import streamlit as st
from pandas import DataFrame
from pandas import read_csv

from text_to_emoji import translate_text

STARTING_LIVES: int = 3
OPTION_COUNT: int = 3
CSV_MAX_ROWS: int = 1000


@dataclass
class Guess:
    chars: str
    emoji: str
    is_correct: bool


class GameState:
    def __init__(self) -> None:
        self.options: list[str] = get_options()
        self.correct_option: str = choice(self.options)
        self.correct_option_emoji: str = translate_text(self.correct_option)
        self.guesses: list[Guess] = []
        self.game_over: bool = False

    def get_lives(self) -> int:
        wrong_guesses: int = len(self.guesses) - self.get_score()
        return STARTING_LIVES - wrong_guesses

    def get_score(self) -> int:
        return len(list(filter(lambda guess: guess.is_correct, self.guesses)))

    def guess(self, option: str) -> None:
        guess: Guess = Guess(option, self.correct_option_emoji,
                             option == self.correct_option)
        self.next_level(guess)

    def next_level(self, guess: Guess) -> None:
        self.guesses.append(guess)

        if not guess.is_correct and self.get_lives() == 0:
            self.game_over = True
            return

        self.options = get_options()
        self.correct_option = choice(self.options)
        self.correct_option_emoji = translate_text(self.correct_option)

    def reset(self) -> None:
        self.game_over = False
        self.options = get_options()
        self.guesses = []
        self.correct_option = choice(self.options)
        self.correct_option_emoji = translate_text(self.correct_option)

    def __repr__(self) -> str:
        result: str = ""
        for attr, attr_val in self.__dict__.items():
            result += f"{attr}: {attr_val}\n"
        return result


@st.cache_data
def get_data() -> DataFrame:
    data = read_csv("data/sample_data/top_10_artists_songs.csv", nrows=CSV_MAX_ROWS)
    return data


def get_options() -> list[str]:
    data: DataFrame = get_data()
    return data.sample(n=OPTION_COUNT).song_name.values
