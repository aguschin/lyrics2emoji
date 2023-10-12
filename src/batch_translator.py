import json
from pathlib import Path
from typing import List

from chatgpt.text_to_emoji import translate_text
from spotify import SongNormalised
from concurrent.futures import ThreadPoolExecutor


DRY_RUN = False

class SongTranslated(SongNormalised):
    translated_lyrics: str

def load_raw_songs(filename) -> List[SongNormalised]:
    """Returns list of texts from json file."""
    file = Path(filename)
    items: List[SongNormalised] = []
    with open(file, 'r') as f:
        items = json.load(f)
    return items


def process_song(song_data: SongNormalised) -> SongTranslated:
    # Replace this with your song processing logic
    lyrics = song_data["lyrics"]
    lyrics = lyrics.split('\n')[0:4]
    lyrics = '\n'.join(lyrics)
    if not DRY_RUN:
        translated_lyrics = translate_text(lyrics)
    else:
        translated_lyrics = lyrics
    return SongTranslated(**song_data, translated_lyrics=translated_lyrics)


def process_songs_multithreaded(songs, num_threads=4):
    songs_translated = []  # List to store processed songs

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit each song for processing and store the future object
        futures = [executor.submit(process_song, song) for song in songs]

        # Retrieve results as they become available
        for future in futures:
            song_result = future.result()
            songs_translated.append(song_result)

    return songs_translated


def write_translated_songs_to_file(songs: List[SongTranslated], raw_filename: str):
    filepath = Path(raw_filename.replace('.json', '_translated.json'))
    with open(filepath, 'w') as f:
        json.dump(songs, f, indent=4, sort_keys=True)
    return filepath


if __name__ == "__main__":
    # Replace this with your list of songs
    songs_raw = load_raw_songs('data/sample_data/top_300_spotify.json')
    songs = songs_raw[:10]
    # Specify the number of threads you want to use
    num_threads = 10

    translated_songs = process_songs_multithreaded(songs, num_threads)
    print(translated_songs)
    fp = write_translated_songs_to_file(translated_songs, 'data/sample_data/top_300_spotify.json')
    print(f'Translated songs saved to: \n\t{fp}')
    for song in translated_songs:
        print(song['translated_lyrics'])
        print('\n'.join(song['lyrics'].split('\n')[0:4]))
        print()
