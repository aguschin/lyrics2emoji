import pandas as pd
import numpy as np
import sys
import logging

sys.path.append("src")
from song_search import pre_process, find_nearest_song_annoy, lyrics_pre_process
from text_to_emoji import translate_text

emojis = pd.read_csv('data/emoji.csv')
lyrics = pd.read_csv('data/sample_data/top_10_artists_songs.csv')
emojis_vectorized = np.load('data/emoji_name_vectorized.npy')
lyrics_vectorized = np.load('data/sample_data/lyrics_vectorized.npy')
accuracy_threshold = 60

def measure_accuracy(lyrics, n=100, convert2emoji=False):
    matched = 0
    for i in range(n):
        match = lyrics['song_name'].iloc[i]
        text = lyrics_pre_process(lyrics['lyrics'][i])
        if convert2emoji:
            text = translate_text(text)
        guess = find_nearest_song_annoy(text)[0]
        if match == guess:
            matched += 1
    accuracy = matched * 100 / n
    return accuracy

class TestFunctionality:
    def test_file_integrity(self):
        assert emojis.shape[0] == emojis_vectorized.shape[0], "emoji files mismatched"
        assert lyrics.shape[0] == lyrics_vectorized.shape[0], "lyric files mismatched"

    def test_lyrics2emoji(self):
        return
    
    def test_accuracy_lyrics_search(self):
        acc = measure_accuracy(lyrics)
        logging.critical(f'accuracy: {acc}%')
        assert acc >= accuracy_threshold, "accuracy is lower than acceptable value"

    def test_accuracy_lyrics2emoji_search(self):
        acc = measure_accuracy(lyrics,convert2emoji=True)
        logging.critical(f'accuracy: {acc}%')
        assert acc >= accuracy_threshold, "accuracy is lower than acceptable value"
