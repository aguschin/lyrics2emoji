import pandas as pd
import numpy as np
import sys
import logging
from sklearn.metrics.pairwise import cosine_similarity

sys.path.append("src")
from preprocess import get_lyrics_first_line, embed
from song_search import find_nearest_song_annoy
from text_to_emoji import translate_text

emojis = pd.read_csv('data/emoji.csv')
lyrics = pd.read_csv('data/sample_data/top_10_artists_songs.csv')
emojis_vectorized = np.load('data/emoji_name_vectorized.npy')
lyrics_vectorized = np.load('data/sample_data/lyrics_vectorized.npy')
accuracy_threshold = 60
average_similarity_threshold = 0.5

def measure_accuracy(lyrics, n=100, convert2emoji=False):
    matched = 0
    for i in range(n):
        match = lyrics['song_name'].iloc[i]
        text = get_lyrics_first_line(lyrics['lyrics'][i])
        if convert2emoji:
            text = translate_text(text)
        guess = find_nearest_song_annoy(text)[0]
        if match == guess:
            matched += 1
    accuracy = matched * 100 / n
    return accuracy

def measure_similarity(lyrics, n=100):
    similarity = 0
    for i in range(n):
        text = get_lyrics_first_line(lyrics['lyrics'][i])
        emoji_embed = embed(translate_text(text))
        text_embed = embed(text)
        similarity += cosine_similarity(text_embed, emoji_embed)
    return similarity / n

class TestFunctionality:
    def test_file_integrity(self):
        assert emojis.shape[0] == emojis_vectorized.shape[0], "emoji files mismatched"
        assert lyrics.shape[0] == lyrics_vectorized.shape[0], "lyric files mismatched"

    def test_lyrics2emoji_cosine_similarity(self):
        average_similarity = measure_similarity(lyrics)[0]
        logging.critical(f'average_similarity: {average_similarity}')
        assert average_similarity >= average_similarity_threshold, "average_similarity is lower than acceptable value"
    
    def test_accuracy_lyrics_search(self):
        accuracy = measure_accuracy(lyrics)
        logging.critical(f'accuracy: {accuracy}%')
        assert accuracy >= accuracy_threshold, "accuracy is lower than acceptable value"

    def test_accuracy_lyrics2emoji_search(self):
        accuracy = measure_accuracy(lyrics,convert2emoji=True)
        logging.critical(f'accuracy: {accuracy}%')
        assert accuracy >= accuracy_threshold, "accuracy is lower than acceptable value"



