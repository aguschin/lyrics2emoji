from __future__ import annotations

import json
import re
from dataclasses import dataclass
from random import choice
from random import randint

import streamlit as st

INVALID_PATTERN: str = r"\([^)]*\)"
JSON_DATA: str = "data/sample_data/top_300_spotify_cleaned_and_translated.json"


@dataclass(slots=True, init=False, repr=False)
class Lyrics:
    bars: list[str]
    translated_bars: list[str]

    def __init__(self, lyrics: str, translated_lyrics: str) -> None:
        self.bars: list[str] = []
        self.translated_bars: list[str] = []
        self._load_lyrics(lyrics, translated_lyrics)

    def _load_lyrics(self, lyrics: str, translated_lyrics: str) -> None:
        for bar in translated_lyrics.split("\n"):
            if not bar: continue
            self.translated_bars.append(bar)

        for bar in lyrics.split("\n"):
            if not bar: continue
            if len(self.bars) == len(self.translated_bars):
                break
            self.bars.append(bar)

        assert len(self.bars) == len(self.translated_bars)

    def get_random_bars(self, n: int = 1) -> list[str]:
        if n == 0: return []
        index_offset: int = randint(0, len(self.bars) - n)
        return self.bars[index_offset: index_offset + n]

    def __repr__(self) -> str:
        return f"{len(self.bars)}: bars, {len(self.translated_bars)}: translated bars"


@dataclass(slots=True, init=False, repr=False)
class Song:
    name: str
    artist: str
    lyrics: Lyrics

    def __init__(self, name: str, artist: str, lyrics: str,
                 translated_lyrics: str) -> None:
        self.name: str = name
        self.artist: str = artist
        self.lyrics: Lyrics = Lyrics(lyrics, translated_lyrics)
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
    def get_json_data() -> list[dict[str, str]]:
        return json.load(open(JSON_DATA))

    def __init__(self) -> None:
        self.data: list[Song] = []
        self.load_json_data()

    def load_json_data(self) -> None:
        for song_dict in DataManager.get_json_data():
            name: str | None = song_dict.get("song_name")
            artist: str | None = song_dict.get("artist_name")
            lyrics: str | None = song_dict.get("lyrics")
            translated_lyrics: str | None = song_dict.get("translated_lyrics")
            if not all([name, artist, lyrics, translated_lyrics]): continue
            self.data.append(Song(name, artist, lyrics, translated_lyrics))

    def get_songs(self, n=1) -> list[Song]:
        songs: list[Song] = []
        if len(self.data) < n:
            raise Exception("ran out of songs :(")

        while len(songs) < n:
            song: Song = choice(self.data)
            songs.append(song)
            self.data.remove(song)

        return songs
