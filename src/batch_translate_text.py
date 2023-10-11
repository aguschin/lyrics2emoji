import json
from pathlib import Path
from sys import argv
from typing import List

from text_to_emoji import translate_text


def batch_translate_texts(texts):
    """Returns list of texts translated to emojis."""
    return [translate_text(text) for text in texts]


def load_texts_from_file(filename):
    """Returns list of texts from json file."""
    file = Path(filename)
    with open(file, 'r') as f:
        texts = json.load(f)
    return texts


def save_texts_to_file(texts: List[str], original_filename: str):
    filepath = Path(original_filename.replace('.json', '_translated.json'))
    with open(filepath, 'w') as f:
        json.dump(texts, f)


def translate_given_json_file(filename):
    texts = load_texts_from_file(filename)
    translated_texts = batch_translate_texts(texts)
    save_texts_to_file(translated_texts, filename)


if __name__ == '__main__':
    given_file_name = argv[1]
    translate_given_json_file(given_file_name)
