import numpy as np
import pandas as pd
from annoy import AnnoyIndex
from preprocess import embed, EMBEDDING_DIMENSION


# lyrics source and column of song name
df = pd.read_csv('data/sample_data/top_10_artists_songs.csv')
song_col = 'song_name'
vectorized_lyrics = np.load('data/sample_data/lyrics_vectorized.npy')


# create annoy index for faster search
annoy_index = AnnoyIndex(EMBEDDING_DIMENSION, 'euclidean')
for i, vectorized_lyric in enumerate(vectorized_lyrics):
    annoy_index.add_item(i, vectorized_lyric)
annoy_index.build(10)


def find_nearest_song_annoy(emojis, n=1):
    """
    args:
        emojis : string of lyrics or emojis
    return:
        list of first n songs with closest embeddings to the input
    """
    idx = annoy_index.get_nns_by_vector(embed(emojis).reshape(-1,1), n)
    return list(df[song_col].iloc[idx])