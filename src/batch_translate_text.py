import json
from sys import argv

from text_to_emoji import translate_text


def batch_translate_texts(texts):
    """Returns list of texts translated to emojis."""
    return [translate_text(text) for text in texts]


def load_texts_from_file(filename):
    """Returns list of texts from json file."""
    with open(filename, 'r') as f:
        texts = json.load(f)
    return texts


def save_texts_to_file(texts, original_filename: str):
    with open(f'{original_filename.lstrip(".json")}_translated.json', 'w') as f:
        json.dump(texts, f)


def translate_given_json_file(filename):
    texts = load_texts_from_file(filename)
    translated_texts = batch_translate_texts(texts)
    save_texts_to_file(translated_texts, filename)

if __name__ == '__main__':
    translate_given_json_file(argv[1])
