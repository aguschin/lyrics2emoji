import json
from pathlib import Path
from typing import List, TypedDict, Callable, Optional
import spacy


import decouple
import openai

from song_types import SongTranslated

openai.api_key = decouple.config("OPENAI_API_KEY")


def get_embedding(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


class SongWithEmbedding(SongTranslated):
    lyrics_embedding: List[float]
    translated_lyrics_embedding: List[float]


def load_raw_songs(filename) -> List[SongTranslated]:
    """Returns list of texts from json file."""
    file = Path(filename)
    items: List[SongTranslated] = []
    with open(file, "r") as f:
        items = json.load(f)
    return items


def write_songs_with_embeddings_to_file(
    songs: List[SongWithEmbedding], raw_filename: str
):
    filepath = Path(raw_filename.replace(".json", "_with_embeddings.json"))
    with open(filepath, "w") as f:
        json.dump(songs, f, indent=4, sort_keys=True)
    return filepath


def process_songs(songs, cleaner: Optional[Callable[[str], str]] = None):
    with_embeddings: List[SongWithEmbedding] = []
    songs_processed = 0
    songs_with_error = 0
    for song in songs:
        try:
            lyrics = song["lyrics"]
            if cleaner:
                lyrics = cleaner(lyrics)
            lyrics_embedding = get_embedding(lyrics)
            lyrics_translated_embedding = get_embedding(song["translated_lyrics"])
        except Exception as e:
            songs_with_error += 1
            print(f"Error processing song: {e}")
        else:
            with_embeddings.append(
                SongWithEmbedding(
                    **song,
                    lyrics_embedding=lyrics_embedding,
                    translated_lyrics_embedding=lyrics_translated_embedding,
                )
            )
            songs_processed += 1
            print(f"Processed {songs_processed}/{len(songs)} songs", end="\r")
    print(
        f"Processed {songs_processed}/{len(songs)} songs with {songs_with_error} errors"
    )
    return with_embeddings


nlp = spacy.load("en_core_web_sm")


def clean_text(lyric):
    doc = nlp(lyric)
    pos_tags = ["AUX", "INTJ", "PROPN", "PUNCT", "SCONJ", "SYM", "X"]
    words = [token.text for token in doc if token.pos_ not in pos_tags]  # filter words
    lyric = " ".join(words).split("\n")  # make full string
    lyric = [i.strip() for i in lyric if len(i) > 15]  # clear small lines
    lyric = "\n".join(lyric).split("\n")[:4]  # get the first 4 lines only
    lyric = "\n".join(lyric)  # completed string

    return lyric


if __name__ == "__main__":
    # Replace this with your list of songs
    songs_raw = load_raw_songs("data/sample_data/top_300_spotify_translated.json")
    songs = [s for s in songs_raw if s["lyrics"]]  # Filter out songs with no lyrics

    converted_songs = process_songs(songs, cleaner=clean_text)

    fp = write_songs_with_embeddings_to_file(
        converted_songs, "data/sample_data/top_300_spotify.json"
    )
    print(f"Translated songs saved to: \n\t{fp}")
    for song in converted_songs:
        print(song["translated_lyrics"])
        print("\n".join(song["lyrics"].split("\n")[0:4]))
        print()
