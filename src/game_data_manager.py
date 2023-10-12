from __future__ import annotations

import re
from dataclasses import dataclass
from random import choice
from random import randint

from pandas import DataFrame
from pandas import read_csv

import streamlit as st

INVALID_PATTERN: str = r"\([^)]*\)"
CSV_DATA: str = "data/sample_data/top_10_artists_songs.csv"
CSV_MAX_ROWS: int = 1000


@dataclass(slots=True, init=False)
class Lyrics:
    bars: list[str]

    def __init__(self, lyrics: str) -> None:

        self.bars: list[str] = []
        for bar in lyrics.split("\r\n"):
            if not bar: continue
            self.bars.append(bar)

    def get_random_bars(self, n: int = 1) -> list[str]:
        if n == 0: return []
        index_offset: int = randint(0, len(self.bars) - n)
        return self.bars[index_offset: index_offset + n]


@dataclass(slots=True, init=False, repr=False)
class Song:
    name: str
    artist: str
    lyrics: Lyrics

    def __init__(self, name: str, artist: str, lyrics: str) -> None:
        self.name: str = name
        self.artist: str = artist
        self.lyrics: Lyrics = Lyrics(lyrics)
        self.format_name()

    def format_name(self) -> None:
        result: list[str] = re.split(INVALID_PATTERN, self.name)
        assert len(result) >= 1
        self.name = result[0].strip()

    def __repr__(self) -> str:
        return f"{self.name} : {self.artist}"


class DataManager:
    manager: DataManager | None = None

    @staticmethod
    def get() -> DataManager:
        if DataManager.manager is None:
            DataManager.manager = DataManager()

        return DataManager.manager

    @staticmethod
    @st.cache_data
    def get_data() -> DataFrame:
        return read_csv(CSV_DATA, nrows=CSV_MAX_ROWS)

    def __init__(self) -> None:
        self.data: list[Song] = []
        self.load_data()

    def load_data(self) -> None:
        data: list[Song] = []
        for _, song in DataManager.get_data().iterrows():
            if not all(song): continue
            data.append(Song(*song))

        self.data = data

    def get_songs(self, n=1, played_songs: list[Song] | None = None) -> list[Song]:
        songs: list[Song] = []
        if played_songs is not None and len(played_songs) >= len(self.data):
            raise Exception("ran out of songs :(")
        while len(songs) < n:
            song: Song = choice(self.data)
            if played_songs is not None and song in played_songs:
                continue
            songs.append(song)
        return songs
