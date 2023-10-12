from __future__ import annotations
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


@dataclass
class Level:
    options: list[str]
    correct: str
    emoji: str

    @staticmethod
    def new_level() -> Level:
        options: list[str] = get_options()
        correct: str = choice(options)
        return Level(options, correct, translate_text(correct))


class GameState:

    def __init__(self) -> None:
        self.level: Level = Level.new_level()
        self.guesses: list[Guess] = []
        self.game_over: bool = False

    def get_lives(self) -> int:
        wrong_guesses: int = len(self.guesses) - self.get_score()
        return STARTING_LIVES - wrong_guesses

    def get_score(self) -> int:
        return len(list(filter(lambda guess: guess.is_correct, self.guesses)))

    def guess(self, option: str) -> None:
        is_correct: bool = option == self.level.correct
        guess: Guess = Guess(option, self.level.emoji, is_correct)
        self.guesses.append(guess)

        if not guess.is_correct and self.get_lives() == 0:
            self.game_over = True
            return

        self._next_level()

    def reset(self) -> None:
        self.game_over = False
        self.guesses = []
        self._next_level()

    def _next_level(self) -> None:
        self.level = Level.new_level()

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
