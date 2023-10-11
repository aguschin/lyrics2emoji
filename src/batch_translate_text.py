import json
from dataclasses import dataclass
from pathlib import Path
from sys import argv
from typing import List, Dict

from text_to_emoji import translate_text


@dataclass
class Song:
    title: str
    text: str


def batch_translate_texts(songs: List[Song]):
    """Returns list of texts translated to emojis."""
    res = []
    for song in songs:
        res.append({'title': song.title, 'text': translate_text(song.text)})
    return res


def load_texts_from_file(filename):
    """Returns list of texts from json file."""
    file = Path(filename)
    with open(file, 'r') as f:
        items = json.load(f)
    return [Song(text=song['text'], title=song['title']) for song in items if song.get('text')]


def save_texts_to_file(texts: List[Dict], original_filename: str):
    filepath = Path(original_filename.replace('.json', '_translated.json'))
    with open(filepath, 'w') as f:
        json.dump(texts, f)


def translate_given_json_file(filename):
    songs = load_texts_from_file(filename)
    translated_texts = batch_translate_texts(songs)
    save_texts_to_file(translated_texts, filename)


if __name__ == '__main__':
    given_file_name = argv[1]
    translate_given_json_file(given_file_name)
