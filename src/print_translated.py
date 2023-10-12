import json
import sys
from pathlib import Path


def load_songs(filename):
    """Returns list of songs from json file."""
    file = Path(filename)
    with open(file, 'r') as f:
        items = json.load(f)
    return items


def print_songs(filename):
    songs = load_songs(filename)
    print(f'Loaded {len(songs)} songs from {filename}')
    for song in songs:
        print(song['translated_lyrics'])

        len_translated = len(song['translated_lyrics'].split('\n'))
        print('\n'.join(song['lyrics'].split('\n')[0:len_translated]))
        print(song['song_name'])
        print()


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'data/sample_data/top_10_spotify_translated.json'
    print_songs(filename)