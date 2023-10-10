from random import choice
import streamlit as st
from pandas import DataFrame
from pandas import read_csv
from text_to_emoji import translate_text


class GameState:
    def __init__(self) -> None:
        self.options: list[str] = get_options()
        self.correct_option: str = choice(self.options)
        self.correct_songs: list[str] = []
        self.score: int = 0
        self.game_over: bool = False

    def next_level(self, option: str) -> None:
        self.score += 1
        self.correct_songs.append(option)
        self.options = get_options()
        self.correct_option = choice(self.options)

    def end_game(self) -> None:
        self.game_over = True

    def reset(self) -> None:
        self.game_over = False
        self.score = 0
        self.options = get_options()
        self.correct_option = choice(self.options)

    def get_correct_option_emoji(self) -> str:
        return translate_text(self.correct_option)

    def __repr__(self) -> str:
        return f"words: {self.options} \ncorrect: {self.correct_option} " \
               f"\ncorrect songs: {self.correct_songs}\nscore:" \
               f" {self.score} \ngame over: {self.game_over}"


@st.cache_data
def get_data() -> DataFrame:
    data = read_csv("data/sample_data/top_10_artists_songs.csv", nrows=1000)
    return data


def get_options() -> list[str]:
    data: DataFrame = get_data()
    return data.sample(n=3).song_name.values
